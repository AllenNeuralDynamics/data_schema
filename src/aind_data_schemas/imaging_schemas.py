from marshmallow import Schema, fields, validate


class InstrumentSchema(Schema):

    _obj_immersion_air = "air"
    _obj_immersion_oil = "oil"
    _obj_immersion_water = "water"
    _obj_immersion_glycerol = "glycerol"
    _obj_immersions = [
        _obj_immersion_air,
        _obj_immersion_oil,
        _obj_immersion_water,
        _obj_immersion_glycerol,
    ]

    _detector_type_ccd = "CCD"
    _detector_type_pmt = "PMT"
    _detector_type_cmos = "CMOS"
    _detector_types = [
        _detector_type_ccd,
        _detector_type_pmt,
        _detector_type_cmos,
    ]

    microscope_type = fields.Str(required=True, data_key="Microscope Type")
    microscope_manufacturer = fields.Str(
        required=True, data_key="Microscope Manufacturer"
    )
    microscope_model = fields.Number(
        required=True, data_key="Microscope Model"
    )
    microscope_serial_number = fields.Str(
        required=True, data_key="Microscope Serial Number"
    )
    objective_manufacturer = fields.Str(
        required=True, data_key="Objective Manufacturer"
    )
    objective_model = fields.Number(required=True, data_key="Objective Model")
    objective_serial_number = fields.Str(
        required=True, data_key="Objective Serial Number"
    )
    objective_immersion = fields.Str(
        required=True,
        data_key="Session Type",
        validate=validate.OneOf(_obj_immersions),
    )
    objective_numerical_aperture = fields.Number(
        required=True, data_key=("Objective " "Numerical " "Aperture")
    )
    objective_magnification = fields.Number(
        required=True, data_key="Objective Magnification"
    )
    detector_type = fields.Str(
        required=True,
        data_key="Detector Type",
        validate=validate.OneOf(_detector_types),
    )
    detector_manufacturer = fields.Str(
        required=True, data_key="Detector Manufacturer"
    )
    detector_model = fields.Number(required=True, data_key="Detector Model")
    detector_serial_number = fields.Str(
        required=True, data_key="Detector Serial Number"
    )
    illumination_type = fields.Str(required=True, data_key="Illumination Type")
    illumination_wavelength_nm = fields.Int(
        required=True, data_key=("Illumination Wavelength" " (nm)")
    )
    detection_wavelength_nm = fields.Int(
        required=True, data_key="Detection Wavelength (nm)"
    )
