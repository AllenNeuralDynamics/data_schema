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
    DATA = f'^(?P<label>.+?)_(?P<acq_date>{RegexParts.DATE.value})_(?P<acq_time>{RegexParts.TIME.value})$'
    RAW_DATA = f'^(?P<modality>.+?)_(?P<subject_id>.+?)_(?P<acq_date>{RegexParts.DATE.value})_(?P<acq_time>{RegexParts.TIME.value})$'
    DERIVED_DATA = f'^(?P<input>.+?_{RegexParts.DATE.value}_{RegexParts.TIME.value})_(?P<label>.+?)_(?P<acq_date>{RegexParts.DATE.value})_(?P<acq_time>{RegexParts.TIME.value})'
    LOCATION = '^(s3|file|gs)://.+$'
    NO_UNDERSCORES = '^[^_]+$'


class DataLevel(Enum):
    raw_data = 'raw data'
    derived_data = 'derived data'
    analysis_data = 'analysis data'


class Institution(Enum):
    AIND = 'AIND'
    AIBS = 'AIBS'


class Group(Enum):
    ephys = 'ephys'
    ophys = 'ophys'
    MSMA = 'MSMA'
    behavior = 'behavior'


class Modality(Enum):
    ecephys = 'ecephys'
    ExASPIM = 'ExASPIM'
    SmartSPIM = 'SmartSPIM'
    mesoSPIM = 'mesoSPIM'
    ophys = 'ophys'


def datetime_tostring(d, t):
    ds = d.strftime('%Y-%m-%d')
    ts = t.strftime('%H-%M-%S')
    return f'{ds}_{ts}'


def datetime_fromstring(d, t):
    return datetime.strptime(d, '%Y-%m-%d').date(), datetime.strptime(t, '%H-%M-%S').time()


class DataDescription(BaseModel):
    schema_version: str = Field('0.1.0', title='Schema Version', const=True)
    license: str = Field('CC-BY-4.0', title='License', const=True)

    acquisition_time: time = Field(..., description='Time of day that data acquisition started', title='Acquisition Time')
    acquisition_date: date = Field(..., description='Day that data acquisition started', title='Acquisition Date')
    label: str = Field(..., description='Generic label for method of acquisition', title='Label')
    name: str = Field(..., description='Name of data, conventionally also the name of the directory containing all data and metadata', title='Name')

    location: Optional[str] = Field(None, regex=DataRegex.LOCATION.value, description="Storage location of data", title='Location')
    data_level: Optional[DataLevel] = Field(None, description='level of processing that data has undergone', title='Data Level')
    institution: Institution = Field(None, description='An established society, corporation, foundation or other organization that collected this data', title='Institution')
    group: Optional[Group] = Field(None, description='A short name for the group of individuals that collected this data', title='Group')    
    project_name: Optional[str] = Field(None, description='A name for a set of coordinated activities intended to achieve one or more objectives', title='Project Name')
    project_id: Optional[str] = Field(None, description='A database or other identifier for a project', title='Project ID')

    @root_validator(pre=True)
    def build_fields(cls, values):
        dt_str = datetime_tostring(values['acquisition_date'], values['acquisition_time'])
        values['name'] = f'{values["label"]}_{dt_str}'
        return values
    

    @classmethod
    def from_name(cls, name):
        m = re.match(f'{DataRegex.DATA.value}', name)
        
        if m is None:
            raise ValueError(f"name({name}) does not match pattern")

        label = m.group(1)
        acquisition_date, acquisition_time = datetime_fromstring(m.group('acq_date'), m.group('acq_time'))
        
        return cls(label=m.group('label'), acquisition_date=acquisition_date, acquisition_time=acquisition_time)

class DerivedDataDescription(DataDescription):
    input_data: DataDescription

    short_name: Optional[str]

    @root_validator(pre=True)
    def build_fields(cls, values):
        dt_str = datetime_tostring(values['acquisition_date'], values['acquisition_time'])
        d = values['input_data']
        name = d.short_name if isinstance(d, DerivedDataDescription) else d.name
        values['name'] = f'{name}_{values["label"]}_{dt_str}'
        values['short_name'] = f'{values["label"]}_{dt_str}'
        return values

    @classmethod
    def from_name(cls, name):
        # look for input data name
        m = re.match(f'{DataRegex.DERIVED_DATA.value}', name)

        # data asset with inputs
        input_data = DataDescription.from_name(m.group('input'))

        label = m.group('label')
        acquisition_date, acquisition_time = datetime_fromstring(m.group('acq_date'), m.group('acq_time'))

        return cls(label=label, acquisition_date=acquisition_date, acquisition_time=acquisition_time, input_data=input_data)

class RawDataDescription(DataDescription):
    modality: str = Field(..., regex=DataRegex.NO_UNDERSCORES.value, description='A short name for the specific manner, characteristic, pattern of application, or the employment of any technology or formal procedure to generate data for a study', title='Modality')
    subject_id: str = Field(..., regex=DataRegex.NO_UNDERSCORES.value, description='Unique identifier for the subject of data acquisition')

    @root_validator(pre=True)
    def build_fields(cls, values):
        dt_str = datetime_tostring(values['acquisition_date'], values['acquisition_time'])
        values['label'] = f'{values["modality"]}_{values["subject_id"]}'
        values['name'] = f'{values["label"]}_{dt_str}'
        return values

    @classmethod
    def from_name(cls, name):
        m = re.match(f'{DataRegex.RAW_DATA.value}', name)

        if m is None:
            raise ValueError(f"name({name}) does not match pattern")

        acquisition_date, acquisition_time = datetime_fromstring(m.group('acq_date'), m.group('acq_time'))

        return cls(modality=m.group('modality'), 
                   subject_id=m.group('subject_id'), 
                   acquisition_date=acquisition_date, 
                   acquisition_time=acquisition_time)

    
def main():
    print("data description from name -------------------------------------")
    da = DataDescription.from_name("ecephys_1234_3033-12-21_04-22-11")
    print(da)

    print("raw description from name -------------------------------------")
    ad = RawDataDescription.from_name("ecephys_1234_3033-12-21_04-22-11")
    print(ad)

    print("derived description from name -------------------------------------")
    ra = DerivedDataDescription.from_name("ecephys_1234_3033-12-21_04-22-11_spikesorted-ks25_2022-10-12_23-23-11")
    print(ra)

    dt = datetime.now()

    print("data description from parts ----------------")
    da = DataDescription(label='ecephys_1234', acquisition_date=dt.date(), acquisition_time=dt.time())
    print(da)
    
    print("derived description from raw description -------------------------------------"),
    r1 = DerivedDataDescription(input_data=ad, label="spikesort-ks25", acquisition_date=dt.date(), acquisition_time=dt.time())
    print(r1)
    print(r1.input_data)

    print("derived description from derived description -------------------------------------")
    r2 = DerivedDataDescription(input_data=r1, label="some-model", acquisition_date=dt.date(), acquisition_time=dt.time())
    print(r2)

    print("result from result from result -------------------------------------")
    r3 = DerivedDataDescription(input_data=r2, label="a-paper", acquisition_date=dt.date(), acquisition_time=dt.time())
    print(r3)

    print("acquisition data from parts -------------------------------------")
    ad = RawDataDescription(modality='ecephys', subject_id='1234', acquisition_date=dt.date(), acquisition_time=dt.time())
    print(ad)

if __name__ == "__main__": main()