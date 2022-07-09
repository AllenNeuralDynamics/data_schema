from marshmallow import Schema, fields


class ProbeSchema(Schema):

    name = fields.Str(required=True, data_key="Name")
    targeted_structure = fields.Str(
        required=True, data_key="Targeted Structure"
    )
    ccf_coordinate_ml = fields.Number(
        required=True, data_key="CCF coordinate ML"
    )
    ccf_coordinate_ap = fields.Number(
        required=True, data_key="CCF coordinate AP"
    )
    ccf_coordinate_dv = fields.Number(
        required=True, data_key="CCF coordinate DV"
    )
    mri_coordinate_ml = fields.Number(
        required=True, data_key="MRI coordinate ML"
    )
    mri_coordinate_ap = fields.Number(
        required=True, data_key="MRI coordinate AP"
    )
    mri_coordinate_dv = fields.Number(
        required=True, data_key="MRI coordinate DV"
    )
    coordinate_ml = fields.Number(required=True, data_key="Coordinate ML")
    coordinate_ap = fields.Number(required=True, data_key="Coordinate AP")
    coordinate_depth = fields.Number(
        required=True, data_key="Coordinate depth"
    )
    angle_ml = fields.Number(required=True, data_key="Angle ML")
    angle_ap = fields.Number(required=True, data_key="Angle AP")


class LaserSchema(Schema):

    name = fields.Str(required=True, data_key="Name")
    wavelength_nm = fields.Int(required=True, data_key="Wavelength (nm)")
    power = fields.Number(required=True, data_key="Power")
    targeted_structure = fields.Str(
        required=True, data_key="Targeted Structure"
    )
    ccf_coordinate_ml = fields.Number(
        required=True, data_key="CCF coordinate ML"
    )
    ccf_coordinate_ap = fields.Number(
        required=True, data_key="CCF coordinate AP"
    )
    ccf_coordinate_dv = fields.Number(
        required=True, data_key="CCF coordinate DV"
    )
    mri_coordinate_ml = fields.Number(
        required=True, data_key="MRI coordinate ML"
    )
    mri_coordinate_ap = fields.Number(
        required=True, data_key="MRI coordinate AP"
    )
    mri_coordinate_dv = fields.Number(
        required=True, data_key="MRI coordinate DV"
    )
    coordinate_ml = fields.Number(required=True, data_key="Coordinate ML")
    coordinate_ap = fields.Number(required=True, data_key="Coordinate AP")
    coordinate_depth = fields.Number(
        required=True, data_key="Coordinate depth"
    )
    angle_ml = fields.Number(required=True, data_key="Angle ML")
    angle_ap = fields.Number(required=True, data_key="Angle AP")
