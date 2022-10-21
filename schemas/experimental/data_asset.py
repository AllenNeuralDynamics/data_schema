from __future__ import annotations

from datetime import datetime, date, time
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, ValidationError, validator, root_validator

# this one is awfully similar to data_description. 
# we should probably merge them together.
class DataAsset(BaseModel):    
    modality: str = Field(regex='^[^_]+$', description="modality name, cannot contain underscores")
    subject_id: str = Field(regex='^[^_]+$', description="subject identifier, cannot contain underscores")
    acquisition_time: time
    acquisition_date: date
    
    name: Optional[str]
    location: Optional[str] = Field(regex='^(s3|file|gs)://.+$')

    # slight misuse of the root_validator, but it's a way to do computed fields
    @root_validator(skip_on_failure=True)
    def compute_name(cls, values):
        
        acq_date = values['acquisition_date'].strftime('%Y-%m-%d')
        acq_time = values['acquisition_time'].strftime('%H-%M-%S')
        
        values['name'] = f"{values['modality']}_{values['subject_id']}_{acq_date}_{acq_time}"
        
        return values

    @classmethod
    def from_name(cls, name):
        m = re.match('(\S+?)_(\S+?)_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})', name)

        if m is None:
            raise ValueError(f"name({name}) does not match pattern")
    
        modality = m.group(1)
        subject_id = m.group(2)
        d = datetime.strptime(m.group(3), '%Y-%m-%d').date()
        t = datetime.strptime(m.group(4), '%H-%M-%S').time()

        return cls(modality=modality, subject_id=subject_id, acquisition_date=d, acquisition_time=t)
