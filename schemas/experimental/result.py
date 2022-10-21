from __future__ import annotations

from datetime import datetime, date, time
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, ValidationError, validator, root_validator

class Result(BaseModel):
    data_asset_name: str  
    label: str = Field(regex='^[^_]+$', description="name of process, cannot contain underscores")
    process_date: date
    process_time: time

    name: Optional[str]
    location: Optional[str] = Field(regex='^(s3|file|gs)://.+$')

    # slight abuse of root_validator to compute a field
    @root_validator(skip_on_failure=True)
    def compute_name(cls, values):  
        p_date = values['process_date'].strftime('%Y-%m-%d')
        p_time = values['process_time'].strftime('%H-%M-%S')
        values['name'] = f"{values['data_asset_name']}_{values['label']}_{p_date}_{p_time}"
        
        return values

    @classmethod
    def from_name(cls, name):
        m = re.match('((\S+?)_(\S+?)_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2}))_(\S+?)_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})', name)
        if m is None:
            raise ValueError(f"invalid result name: {namef}")
    
        data_asset_name = m.group(1)
        label = m.group(6)
        d = datetime.strptime(m.group(7), '%Y-%m-%d').date()
        t = datetime.strptime(m.group(8), '%H-%M-%S').time()
        
        return cls(data_asset_name=data_asset_name, label=label, process_date=d, process_time=t)