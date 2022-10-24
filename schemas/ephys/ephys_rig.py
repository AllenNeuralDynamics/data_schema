from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class HarpDevice(Enum):
    Behavior = 'Behavior'
    WEAR_basestation = 'WEAR basestation'
    Camera_trigger_control = 'Camera trigger control'
    LED_array_interface = 'LED array interface'
    Analog_input = 'Analog input'
    Multi_PWM_generator = 'Multi PWM generator'
    Clock_synchronizer = 'Clock synchronizer'


class CameraName(Enum):
    Body_Camera = 'Body Camera'
    Eye_Camera = 'Eye Camera'
    Face_Camera = 'Face Camera'


class Camera(BaseModel):
    name: CameraName = Field(..., title='Name')
    manufacturer: str = Field(..., title='Manufacturer')
    model: str = Field(..., title='Model')
    serial_number: str = Field(..., title='Serial number')
    position_x: float = Field(..., title='Position X')
    position_y: float = Field(..., title='Position Y')
    position_z: float = Field(..., title='Position Z')
    angle_pitch: float = Field(..., title='Angle pitch (deg)', units="deg")
    angle_yaw: float = Field(..., title='Angle yaw (deg)', units="deg")
    angle_roll: float = Field(..., title='Angle roll (deg)', units="deg")
    recording_software: Optional[str] = Field(None, title='Recording software')
    recording_software_version: Optional[str] = Field(
        None, title='Recording software version'
    )


class Surface(Enum):
    none = 'none'
    foam = 'foam'


class Disc(BaseModel):
    radius: float = Field(..., title='Radius (cm)', units="cm")
    surface: Optional[Surface] = Field(None, title='Surface')
    date_surface_replaced: Optional[datetime] = Field(
        None, title='Date surface replaced'
    )


class LaserName(Enum):
    Laser_A = 'Laser A'
    Laser_B = 'Laser B'


class Laser(BaseModel):
    name: LaserName = Field(..., title='Name')
    manufacturer: str = Field(..., title='Manufacturer')
    model: str = Field(..., title='Model')
    serial_number: str = Field(..., title='Serial number')
    wavelength: Optional[int] = Field(None, title='Wavelength (nm)', units="nm")
    maximum_power: Optional[float] = Field(None, title='Maximum power (mW)', units="mW")
    coupling_efficiency: Optional[float] = Field(
        None, title='Coupling efficiency (percent)', units="percent"
    )
    calibration_data: Optional[str] = Field(
        None, description='path to calibration data', title='Calibration data'
    )
    calibration_date: Optional[datetime] = Field(None, title='Calibration date')


class Monitor(BaseModel):
    manufacturer: str = Field(..., title='Manufacturer')
    model: str = Field(..., title='Model')
    serial_number: str = Field(..., title='Serial number')
    refresh_rate: int = Field(..., title='Refresh rate (Hz)', units="Hz")
    width: int = Field(..., title='Width (pixels)', units="pixels")
    height: int = Field(..., title='Height (pixels)', units="pixels")
    viewing_distance: float = Field(..., title='Viewing distance (cm)', units="cm")
    position_x: float = Field(..., title='Position X')
    position_y: float = Field(..., title='Position Y')
    position_z: float = Field(..., title='Position Z')
    angle_pitch: float = Field(..., title='Angle pitch (deg)', units="deg")
    angle_yaw: float = Field(..., title='Angle yaw (deg)', units="deg")
    angle_roll: float = Field(..., title='Angle roll (deg)', units="deg")
    contrast: int = Field(
        ..., description="Monitor's contrast setting", title='Contrast (percent)', units="percent"
    )
    brightness: int = Field(
        ..., description="Monitor's brightness setting", title='Brightness'
    )


class ProbeName(Enum):
    Probe_A = 'Probe A'
    Probe_B = 'Probe B'
    Probe_C = 'Probe C'
    Probe_D = 'Probe D'
    Probe_E = 'Probe E'
    Probe_F = 'Probe F'
    Probe_G = 'Probe G'
    Probe_H = 'Probe H'
    Probe_I = 'Probe I'
    Probe_J = 'Probe J'


class Probe(BaseModel):
    name: ProbeName = Field(..., title='Name')
    type: str = Field(..., title='Type')
    serial_number: str = Field(..., title='Serial number')


class Devices(BaseModel):
    probes: Optional[List[Probe]] = Field(None, title='Probes', unique_items=True)
    cameras: Optional[List[Camera]] = Field(None, title='Cameras', unique_items=True)
    lasers: Optional[List[Laser]] = Field(None, title='Lasers', unique_items=True)
    visual_monitors: Optional[List[Monitor]] = Field(
        None, title='Visual monitor', unique_items=True
    )
    running_disc: Optional[Disc] = Field(None, title='Running disc')
    harp_devices: Optional[List[HarpDevice]] = None


class EphysRig(BaseModel):
    describedBy: str = Field(
        'https://github.com/AllenNeuralDynamics/data_schema/blob/main/schemas/ephys/ephys_rig.py', description='The URL reference to the schema.', title='Described by', const=True
    )
    schema_version: str = Field("0.2.0", description='schema version', title='Version', const=True)
    rig_id: str = Field(..., description='room_stim apparatus_version', title='Rig ID')
    devices: Devices