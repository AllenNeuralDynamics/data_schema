from __future__ import annotations

from datetime import datetime, date, time
from enum import Enum
from typing import List, Optional
import re

from pydantic import BaseModel, Field, ValidationError, validator, root_validator

class RegexParts(Enum):
    DATE = '\d{4}-\d{2}-\d{2}'
    TIME = '\d{2}-\d{2}-\d{2}'

class DataRegex(Enum):
    DATA_ASSET = f'^(?P<label>.+?)_(?P<acq_date>{RegexParts.DATE.value})_(?P<acq_time>{RegexParts.TIME.value})$'
    ACQUISITION = f'^(?P<modality>.+?)_(?P<subject_id>.+?)_(?P<acq_date>{RegexParts.DATE.value})_(?P<acq_time>{RegexParts.TIME.value})$'
    RESULT = f'^(?P<input>.+?_{RegexParts.DATE.value}_{RegexParts.TIME.value})_(?P<label>.+?)_(?P<acq_date>{RegexParts.DATE.value})_(?P<acq_time>{RegexParts.TIME.value})'
    LOCATION = '^(s3|file|gs)://.+$'
    NO_UNDERSCORES = '^[^_]+$'

def datetime_tostring(d, t):
    ds = d.strftime('%Y-%m-%d')
    ts = t.strftime('%H-%M-%S')
    return f'{ds}_{ts}'

def datetime_fromstring(d, t):
    return datetime.strptime(d, '%Y-%m-%d').date(), datetime.strptime(t, '%H-%M-%S').time()

# this one is awfully similar to data_description. 
# we should probably merge them together.
class DataAsset(BaseModel):
    acquisition_time: time
    acquisition_date: date
    label: str

    name: Optional[str]
    location: Optional[str] = Field(regex=DataRegex.LOCATION.value)

    @root_validator(pre=True)
    def build_fields(cls, values):
        dt_str = datetime_tostring(values['acquisition_date'], values['acquisition_time'])
        values['name'] = f'{values["label"]}_{dt_str}'
        return values
    

    @classmethod
    def from_name(cls, name):
        m = re.match(f'{DataRegex.DATA_ASSET.value}', name)
        
        if m is None:
            raise ValueError(f"name({name}) does not match pattern")

        label = m.group(1)
        acquisition_date, acquisition_time = datetime_fromstring(m.group('acq_date'), m.group('acq_time'))
        
        return cls(label=m.group('label'), acquisition_date=acquisition_date, acquisition_time=acquisition_time)

class Result(DataAsset):
    input_data: DataAsset

    short_name: Optional[str]

    @root_validator(pre=True)
    def build_fields(cls, values):
        dt_str = datetime_tostring(values['acquisition_date'], values['acquisition_time'])
        values['name'] = f'{values["input_data"].name}_{values["label"]}_{dt_str}'
        values['short_name'] = f'{values["label"]}_{dt_str}'
        return values

    @classmethod
    def from_name(cls, name):
        # look for input data name
        m = re.match(f'{DataRegex.RESULT.value}', name)

        # data asset with inputs
        input_data = DataAsset.from_name(m.group('input'))

        label = m.group('label')
        acquisition_date, acquisition_time = datetime_fromstring(m.group('acq_date'), m.group('acq_time'))

        return cls(label=label, acquisition_date=acquisition_date, acquisition_time=acquisition_time, input_data=input_data)

class Acquisition(DataAsset):
    modality: str = Field(..., regex=DataRegex.NO_UNDERSCORES.value)
    subject_id: str = Field(..., regex=DataRegex.NO_UNDERSCORES.value)

    @root_validator(pre=True)
    def build_fields(cls, values):
        dt_str = datetime_tostring(values['acquisition_date'], values['acquisition_time'])
        values['label'] = f'{values["modality"]}_{values["subject_id"]}'
        values['name'] = f'{values["label"]}_{dt_str}'
        return values

    @classmethod
    def from_name(cls, name):
        m = re.match(f'{DataRegex.ACQUISITION.value}', name)

        if m is None:
            raise ValueError(f"name({name}) does not match pattern")

        acquisition_date, acquisition_time = datetime_fromstring(m.group('acq_date'), m.group('acq_time'))

        return cls(modality=m.group('modality'), 
                   subject_id=m.group('subject_id'), 
                   acquisition_date=acquisition_date, 
                   acquisition_time=acquisition_time)

    
def main():
    print("data asset from name -------------------------------------")
    da = DataAsset.from_name("ecephys_1234_3033-12-21_04-22-11")
    print(da)

    print("acquisition from name -------------------------------------")
    ad = Acquisition.from_name("ecephys_1234_3033-12-21_04-22-11")
    print(ad)

    print("result from name -------------------------------------")
    ra = Result.from_name("ecephys_1234_3033-12-21_04-22-11_spikesorted-ks25_2022-10-12_23-23-11")
    print(ra)

    dt = datetime.now()

    print("data asset from parts ----------------")
    da = DataAsset(label='ecephys_1234', acquisition_date=dt.date(), acquisition_time=dt.time())
    print(da)
    
    print("result from acquisition -------------------------------------"),
    r1 = Result(input_data=ad, label="spikesort-ks25", acquisition_date=dt.date(), acquisition_time=dt.time())
    print(r1)
    print(r1.input_data)

    print("result from result -------------------------------------")
    r2 = Result(input_data=r1, label="some-model", acquisition_date=dt.date(), acquisition_time=dt.time())
    print(r2)

    print("result from result from result -------------------------------------")
    r3 = Result(input_data=r2, label="a-paper", acquisition_date=dt.date(), acquisition_time=dt.time())
    print(r3)

    print("acquisition data from parts -------------------------------------")
    ad = Acquisition(modality='ecephys', subject_id='1234', acquisition_date=dt.date(), acquisition_time=dt.time())
    print(ad)

if __name__ == "__main__": main()