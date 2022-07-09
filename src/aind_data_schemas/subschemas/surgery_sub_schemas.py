from marshmallow import (Schema, ValidationError, fields, validate,
                         validates_schema)


class HeadPlateCraniotomySchema(Schema):

    hpc_coordinates_ml = fields.Number(data_key="HPC Coordinates ML")
    hpc_coordinates_ap = fields.Number(data_key="HPC Coordinates AP")
    hpc_size_mm = fields.Number(data_key="HPC Size (mm)")
    hpc_angle_roll_deg = fields.Number(data_key="HPC Angle roll (deg)")
    hpc_angle_pitch_deg = fields.Number(data_key="HPC Angle pitch (deg)")


class _IontophoresisSchema(Schema):
    injection_current_ua = fields.Number(data_key="Injection Current (uA)")
    alternating_current = fields.Str(data_key="Alternating Current")


class _NanojectSchema(Schema):
    injection_volume_nl = fields.Number(data_key="Injection Volume (nL)")


class InjectionSchema(_IontophoresisSchema, _NanojectSchema):

    injection_iontophoresis = "Iontophoresis"
    injection_nanoject = "Nanoject"
    injection_types = [injection_iontophoresis, injection_nanoject]

    injection_coordinates_ml = fields.Number(
        required=True, data_key="Injection Coordinates ML"
    )
    injection_coordinates_ap = fields.Number(
        required=True, data_key="Injection Coordinates AP"
    )
    injection_coordinates_depth = fields.Number(
        required=True, data_key="Injection Coordinates depth"
    )
    injection_type = fields.Str(
        required=True,
        data_key="Injection Type",
        validate=validate.OneOf(injection_types),
    )
    injection_duration = fields.Time(
        required=True, data_key="Injection Duration"
    )
    injection_angle = fields.Number(data_key="Injection Angle")
    injection_virus = fields.Str(data_key="Injection Virus")

    @validates_schema
    def validate_injection(self, data, **kwargs):
        if data["injection_type"] == self.injection_iontophoresis:
            for field in _IontophoresisSchema().fields.keys():
                if field not in data:
                    raise ValidationError(
                        f"{field} is required when injection_type is "
                        f"{self.injection_iontophoresis}"
                    )
        if data["injection_type"] == self.injection_nanoject:
            for field in _NanojectSchema().fields.keys():
                if field not in data:
                    raise ValidationError(
                        f"{field} is required when injection_type is "
                        f"{self.injection_nanoject}"
                    )
