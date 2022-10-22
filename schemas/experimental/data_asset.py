from __future__ import annotations

from datetime import datetime, date, time
from enum import Enum
from typing import List, Optional
import re

from pydantic import BaseModel, Field, ValidationError, validator, root_validator

# this one is awfully similar to data_description. 
# we should probably merge them together.
class DataAsset(BaseModel):
    prefix: str 
    acquisition_time: time
    acquisition_date: date
    
    name: Optional[str]
    location: Optional[str] = Field(regex='^(s3|file|gs)://.+$')

    @root_validator(pre=True)
    def construct(cls, values):
        values['name'] = f"{values['prefix']}_{values['acquisition_date']}_{values['acquisition_time']}"

        return values

    @classmethod
    def from_name(cls, name):
        m = re.match('^(.+)_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})$', name)

        if m is None:
            raise ValueError(f"name({name}) does not match pattern")
    
        prefix = m.group(1)
        d = datetime.strptime(m.group(2), '%Y-%m-%d').date()
        t = datetime.strptime(m.group(3), '%H-%M-%S').time()

        return cls(name=name, prefix=prefix, acquisition_date=d, acquisition_time=t)

class AcquisitionData(DataAsset):
    modality: str = Field(regex='^[^_]+$', description="modality name, cannot contain underscores")
    subject_id: str = Field(regex='^[^_]+$', description="subject identifier, cannot contain underscores")

    @root_validator(pre=True)
    def construct(cls, values):
        prefix = f"{values['modality']}_{values['subject_id']}"
        values['prefix'] = prefix
        values['name'] = f"{prefix}_{values['acquisition_date']}_{values['acquisition_time']}"

        return values

    @classmethod
    def from_name(cls, name):
        da = DataAsset.from_name(name)

        m = re.match('^(\S+?)_(\S+?)$', da.prefix)

        if m is None:
            raise ValueError(f"name({name}) does not match pattern")
    
        modality = m.group(1)
        subject_id = m.group(2)

        return cls(name=name,
                   prefix=da.prefix,
                   modality=modality, 
                   subject_id=subject_id, 
                   acquisition_date=da.acquisition_date, 
                   acquisition_time=da.acquisition_time)

class ResultData(DataAsset):
    data_asset_name: str  
    label: str = Field(regex='^[^_]+$', description="name of process, cannot contain underscores")

    @root_validator(pre=True)
    def construct(cls, values):
        da = DataAsset.from_name(values['data_asset_name'])
        
        d = values['acquisition_date'].strftime('%Y-%m-%d')
        t = values['acquisition_time'].strftime('%H-%M-%S')
        prefix = f"{values['data_asset_name']}_{values['label']}"

        values['prefix'] = prefix
        values['name'] = f"{prefix}_{d}_{t}"

        return values

    @classmethod
    def from_name(cls, name):
        da = DataAsset.from_name(name)
        
        m = re.match('^(\S+)_(\S+)$', da.prefix)
        
        if m is None:
            raise ValueError(f"name({name}) does not match pattern")
    
        da_name = m.group(1)
        label = m.group(2)

        return cls(data_asset_name=da_name,
                   label=label,
                   acquisition_date=da.acquisition_date, 
                   acquisition_time=da.acquisition_time)

    
if __name__ == "__main__":
    da = DataAsset.from_name("ecephys_1234_3033-12-21_04-22-11")
    print(da)

    ad = AcquisitionData.from_name("ecephys_1234_3033-12-21_04-22-11")
    print(ad)
    
    rd = ResultData.from_name("ecephys_1234_3033-12-21_04-22-11_spikesorted-ks25_2022-10-12_23-23-11")
    print(rd)

    dt = datetime.now()

    rd = ResultData(data_asset_name="ecephys_1234_3033-12-21_04-22-11", label="bob", acquisition_date=dt.date(), acquisition_time=dt.time())
    print(rd)

    ad = AcquisitionData(modality='ecephys', subject_id='1234', acquisition_date=dt.date(), acquisition_time=dt.time())
    print(ad)