from marshmallow import Schema, fields, validate

from aind_data_schemas import field_definitions as fd
from aind_data_schemas.validators import validate_unique_items


class LaserSchema(Schema):
    _laser_names = ["Laser A", "Laser B"]

    name = fields.Str(
        data_key="Name", required=True, validate=validate.OneOf(_laser_names)
    )
    manufacturer = fields.Str(required=True, data_key="Manufacturer")
    model = fields.Str(required=True, data_key="Model")
    serial_number = fields.Str(required=True, data_key="Serial number")
    wavelength_nm = fields.Int(data_key="Wavelength (nm)")
    maximum_power = fields.Number(data_key="Maximum power")
    coupling_efficiency = fields.Number(data_key="Coupling efficiency")
    calibration_data = fields.Str(
        data_key="Calibration data", description="path to calibration data"
    )
    calibration_date = fields.DateTime(data_key="Calibration date")


class CameraSchema(Schema):
    _camera_names = ["Body Camera", "Eye Camera", "Face Camera"]

    name = fields.Str(
        data_key="Name", required=True, validate=validate.OneOf(_camera_names)
    )
    manufacturer = fields.Str(required=True, data_key="Manufacturer")
    model = fields.Str(required=True, data_key="Model")
    serial_number = fields.Str(required=True, data_key="Serial number")
    position_x = fields.Number(required=True, data_key="Position x")
    position_y = fields.Number(required=True, data_key="Position y")
    position_z = fields.Number(required=True, data_key="Position z")
    angle_pitch_deg = fields.Number(data_key="Angle pitch (deg)")
    angle_yaw_deg = fields.Number(data_key="Angle yaw (deg)")
    angle_roll_deg = fields.Number(data_key="Angle roll (deg)")
    recording_software = fields.Str(data_key="Recording software")
    recording_software_version = fd.Version(
        data_key="Recording software version"
    )


class ProbeSchema(Schema):
    _probe_names = [
        "Probe A",
        "Probe B",
        "Probe C",
        "Probe D",
        "Probe E",
        "Probe F",
        "Probe G",
        "Probe H",
        "Probe I",
        "Probe J",
    ]

    name = fields.Str(
        data_key="Name", required=True, validate=validate.OneOf(_probe_names)
    )
    type = fields.Str(required=True, data_key="Type")
    serial_number = fields.Str(required=True, data_key="Serial number")


class MonitorSchema(Schema):

    refresh_rate_hz = fields.Number(
        required=True, data_key="Refresh rate (Hz)"
    )
    width_pixels = fields.Number(required=True, data_key="Width (pixels)")
    height_pixels = fields.Number(required=True, data_key="Height (pixels)")
    distance_cm = fields.Number(required=True, data_key="Distance (cm)")
    position_x = fields.Number(required=True, data_key="Position x")
    position_y = fields.Number(required=True, data_key="Position y")
    angle_deg = fields.Number(required=True, data_key="Angle (deg)")
    contrast_percent = fields.Int(required=True, data_key="Contrast (percent)")
    brightness = fields.Int(required=True, data_key="Brightness")
    manufacturer = fields.Str(data_key="Manufacturer")
    model = fields.Str(data_key="Model")
    serial_number = fields.Str(data_key="Serial number")


class DiskSchema(Schema):

    _surfaces = ["none", "foam"]

    radius_cm = fields.Number(required=True, data_key="Radius (cm)")
    surface = fields.Str(
        data_key="Surface", validate=validate.OneOf(_surfaces)
    )
    date_surface_replaced = fields.DateTime(data_key="Date surface replaced")


class DevicesSchema(Schema):
    probes = fields.List(
        fields.Nested(ProbeSchema),
        data_key="Probes",
        validate=validate_unique_items,
    )
    cameras = fields.List(
        fields.Nested(CameraSchema),
        data_key="Cameras",
        validate=validate_unique_items,
    )
    lasers = fields.List(
        fields.Nested(LaserSchema),
        data_key="Lasers",
        validate=validate_unique_items,
    )
    visual_monitor = fields.List(
        fields.Nested(MonitorSchema),
        data_key="Visual Monitor",
        validate=validate_unique_items,
    )
    running_disk = fields.List(
        fields.Nested(DiskSchema),
        data_key="Running Disk",
        validate=validate.Length(max=1),
    )
