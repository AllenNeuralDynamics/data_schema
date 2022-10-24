from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ProcessName(Enum):
    Ephys_preprocessing = 'Ephys preprocessing'
    Spike_sorting = 'Spike sorting'
    Ephys_postprocessing = 'Ephys postprocessing'
    Image_import = 'Image import'
    Image_align = 'Image align'
    Merge_volume = 'Merge volume'
    OME_zarr = 'OME zarr'
    Pystripe = 'Pystripe'
    Displthresh = 'Displthresh'
    Other = 'Other'


class DataProcess(BaseModel):
    name: ProcessName = Field(..., title='Name')
    version: str = Field(
        ..., description='Version of the software used', title='Version'
    )
    start_date_time: datetime = Field(..., title='Start date time')
    end_date_time: datetime = Field(..., title='End date time')
    input_location: str = Field(
        ..., description='Path to data inputs', title='Input location'
    )
    output_location: str = Field(
        ..., description='Path to data outputs', title='Output location'
    )
    code_url: str = Field(..., description='Path to code respository', title='Code URL')
    parameters: Dict[str, Any]
    notes: Optional[str] = None


class Processing(BaseModel):
    describedBy: str = Field(
        'https://github.com/AllenNeuralDynamics/data_schema/blob/main/schemas/processing.py', description='The URL reference to the schema.', title='Described by', const=True
    )
    schema_version: str = Field(
        '0.0.1', description='Schema version', title='Schema version', const=True
    )
    pipeline_version: Optional[str] = Field(
        None, description='Version of the pipeline', title='Pipeline version'
    )
    pipeline_url: Optional[str] = Field(
        None, description='URL to the pipeline code', title='Pipeline URL'
    )
    data_processes: List[DataProcess] = Field(
        ..., title='Data processing', unique_items=True
    )