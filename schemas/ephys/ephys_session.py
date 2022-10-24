from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Institution(Enum):
    AIND = 'AIND'
    MSP = 'MSP'


class SessionType(Enum):
    Test = 'Test'
    Foraging_A = 'Foraging A'
    Spontaneous = 'Spontaneous'
    Foraging_B = 'Foraging B'


class ExpectedDataStream(Enum):
    Neuropixels_probes = 'Neuropixels probes'
    Body_camera = 'Body camera'
    Face_camera = 'Face camera'
    Eye_camera = 'Eye camera'
    Bonsai_file = 'Bonsai file'
    Harp_bin_file = 'Harp bin file'
    Other = 'Other'


class CcfVersion(Enum):
    CCFv3 = 'CCFv3'


class Direction(Enum):
    X = 'X'
    Y = 'Y'
    Z = 'Z'


class Field3dCoordinatesMm(BaseModel):
    direction: Direction = Field(..., title='Direction')
    value: float = Field(..., title='Value (mm)', units="mm")


class AnatomicalDirection(Enum):
    ML = 'ML'
    AP = 'AP'
    DV = 'DV'


class CcfCoords(BaseModel):
    direction: AnatomicalDirection = Field(..., title='AnatomicalDirection')
    value: float = Field(..., title='Value (um)', units="mm")


class AngleName(Enum):
    XY = 'XY'
    XZ = 'XZ'
    YZ = 'YZ'


class ManipulatorAngles(BaseModel):
    name: AngleName = Field(..., title='AngleName')
    value: float = Field(..., title='Value (deg)', units="deg")


class Laser(BaseModel):
    name: str = Field(..., title='Name')
    wavelength: int = Field(..., title='Wavelength (nm)', units="nm")
    power: float = Field(..., title='Power (mW)', units="mW")
    targeted_structure: str = Field(..., title='Targeted structure')
    targeted_ccf_coordinates: List[CcfCoords] = Field(
        ...,
        max_items=3,
        min_items=3,
        title='Targeted CCF coordinates',
        unique_items=True,
    )
    targeted_lab_coordinates: List[Field3dCoordinatesMm] = Field(
        ...,
        description='Targeted coordinates relative to the headframe',
        max_items=3,
        min_items=3,
        title='Targeted lab coordinates',
        unique_items=True,
    )
    manipulator_coordinates: List[Field3dCoordinatesMm] = Field(
        ...,
        max_items=3,
        min_items=3,
        title='Manipulator coordinates',
        unique_items=True,
    )
    manipulator_angles: List[ManipulatorAngles] = Field(
        ..., title='Manipulator angles', unique_items=True
    )


class Probe(BaseModel):
    name: str = Field(..., title='Name')
    tip_targeted_structure: str
    other_targeted_structures: Optional[str] = None
    targeted_ccf_coordinates: List[CcfCoords] = Field(
        ...,
        max_items=3,
        min_items=3,
        title='Targeted CCF coordinates',
        unique_items=True,
    )
    targeted_lab_coordinates: List[Field3dCoordinatesMm] = Field(
        ...,
        description='Targeted coordinates relative to the headframe',
        max_items=3,
        min_items=3,
        title='Targeted lab coordinates',
        unique_items=True,
    )
    manipulator_coordinates: List[Field3dCoordinatesMm] = Field(
        ...,
        max_items=3,
        min_items=3,
        title='Manipulator coordinates',
        unique_items=True,
    )
    manipulator_angles: List[ManipulatorAngles] = Field(
        ..., title='Manipulator angles', unique_items=True
    )


class Stream(BaseModel):
    stream_start_time: datetime = Field(..., title='Stream start time')
    stream_stop_time: datetime = Field(..., title='Stream stop time')
    probes: List[Probe] = Field(..., title='Probes', unique_items=True)
    lasers: List[Laser] = Field(..., title='Lasers', unique_items=True)


class EphysSession(BaseModel):
    schema_version: str = Field("0.2.0", description='schema version', title='Version', const=True)
    describedBy: str = Field(
        'https://github.com/AllenNeuralDynamics/data_schema/blob/main/schemas/ephys/ephys_session.py', description='The URL reference to the schema.', title='Described by', const=True
    )
    institution: Institution = Field(..., title='Institution')
    experimenter_full_name: str = Field(
        ...,
        description='First and last name of the experimenter.',
        title='Experimenter full name',
    )
    session_start_time: datetime = Field(..., title='Session start time')
    session_end_time: datetime = Field(..., title='Session end time')
    specimen_id: int = Field(..., title='Specimen ID')
    project_name: Optional[str] = Field(None, title='Project name')
    project_id: str = Field(..., title='Project ID')
    session_type: SessionType = Field(..., title='Session type')
    stimulus_protocol_id: Optional[str] = Field(None, title='Stimulus protocol ID')
    rig_id: str = Field(..., title='Rig ID')
    expected_data_streams: Optional[List[ExpectedDataStream]] = None
    probe_streams: List[Stream] = Field(..., title='Probe streams', unique_items=True)
    ccf_version: CcfVersion = Field(..., title='CCF version')
    coordinate_transform: Optional[str] = Field(
        None,
        description='Path to file that details the coordinate transform.',
        title='Coordinate transform',
    )
    notes: Optional[str] = None