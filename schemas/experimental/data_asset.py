from __future__ import annotations

from datetime import datetime, date, time
from enum import Enum
from typing import List, Optional
import re

from pydantic import BaseModel, Field, ValidationError, validator, root_validator

class DataRegex(Enum):
    NAME = '(.+?)_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})'
    LOCATION = '^(s3|file|gs)://.+$'
    ACQUISITION = '(.+?)_(.+?)_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})'
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
    def build_name(cls, values):
        dt_str = datetime_tostring(values['acquisition_date'], values['acquisition_time'])
        label = values['label']

        values['name'] = f'{label}_{dt_str}'

        return values
        

    @classmethod
    def from_name(cls, name):
        m = re.match(f'^{DataRegex.NAME.value}$', name)

        if m is None:
            raise ValueError(f"name({name}) does not match pattern")

        label = m.group(1)
        acquisition_date, acquisition_time = datetime_fromstring(m.group(2), m.group(3))
        
        return cls(label=label, acquisition_date=acquisition_date, acquisition_time=acquisition_time)

class Result(DataAsset):
    input_data: DataAsset

    short_name: Optional[str]

    @root_validator(pre=True)
    def build_name(cls, values):
        dt_str = datetime_tostring(values['acquisition_date'], values['acquisition_time'])

        label = values['label']
        input_data = values['input_data']
        input_name = input_data.short_name if isinstance(input_data, Result) else input_data.name

        short_name = f'{label}_{dt_str}'

        values['short_name'] = short_name
        values['name'] = f'{input_name}_{short_name}'

        return values
        

    @classmethod
    def from_name(cls, name):
        # look for input data name
        m = re.match(f'^({DataRegex.NAME.value})_({DataRegex.NAME.value})$', name)

        # data asset with inputs
        input_data = DataAsset.from_name(m.group(1))

        label = m.group(6)
        acquisition_date, acquisition_time = datetime_fromstring(m.group(7), m.group(8))

        return cls(label=label, acquisition_date=acquisition_date, acquisition_time=acquisition_time, input_data=input_data)

class Acquisition(DataAsset):
    modality: str = Field(..., regex=DataRegex.NO_UNDERSCORES.value)
    subject_id: str = Field(..., regex=DataRegex.NO_UNDERSCORES.value)

    @root_validator(pre=True)
    def build_name(cls, values):
        modality = values['modality']
        subject_id = values['subject_id']
        dt_str = datetime_tostring(values['acquisition_date'], values['acquisition_time'])

        label = f'{modality}_{subject_id}'
        values['label'] = label
        values['name'] = f'{label}_{dt_str}'

        return values

    @classmethod
    def from_name(cls, name):
        m = re.match(f'^{DataRegex.ACQUISITION.value}$', name)

        if m is None:
            raise ValueError(f"name({name}) does not match pattern")
    
        modality = m.group(1)
        subject_id = m.group(2)

        return cls(modality=modality, 
                   subject_id=subject_id, 
                   acquisition_date=da.acquisition_date, 
                   acquisition_time=da.acquisition_time)

    
if __name__ == "__main__":
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

    print("result from data asset -------------------------------------"),
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