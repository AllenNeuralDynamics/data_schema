from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class DataLevel(Enum):
    raw_data = 'raw data'
    derived_data = 'derived data'


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


class DataDescription(BaseModel):
    describedBy: str = Field(
        "https://github.com/AllenNeuralDynamics/data_schema/blob/main/schemas/data_description.py", description='The URL reference to the schema.', title='Described by', const=True
    )
    schema_version: str = Field('0.0.1', description='schema version', title='Version', const=True)
    license: str = Field('CC-BY-4.0', title='License', const=True)
    data_level: DataLevel = Field(
        ...,
        description='level of processing that data has undergone',
        title='Data Level',
    )
    name: Optional[str] = Field(
        None,
        description='name of data, conventionally also the name of the directory containing all data and metadata',
        title='Name',
    )
    institution: Institution = Field(
        ...,
        description='An established society, corporation, foundation or other organization that collected this data',
        title='Institution',
    )
    group: Optional[Group] = Field(
        None,
        description='A short name for the group of individuals that collected this data',
        title='Group',
    )
    modality: Optional[Modality] = Field(
        None,
        description='A short name for the specific manner, characteristic, pattern of application, or the employment of any technology or formal procedure to generate data for a study',
        title='Modality',
    )
    project_name: Optional[str] = Field(
        None,
        description='A name for a set of coordinated activities intended to achieve one or more objectives',
        title='Project Name',
    )
    project_id: Optional[str] = Field(
        None,
        description='A database or other identifier for a project',
        title='Project ID',
    )