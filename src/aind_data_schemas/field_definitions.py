from marshmallow import ValidationError, fields, validate
from packaging import version


class DateOfBirth(fields.Date):
    def __init__(self, required: bool = False):
        super().__init__(required=required, data_key="Date of Birth")


class ExperimenterFirstName(fields.String):
    def __init__(self, required: bool = False):
        super().__init__(required=required, data_key="Experimenter first name")


class ExperimenterLastName(fields.String):
    def __init__(self, required: bool = False):
        super().__init__(required=required, data_key="Experimenter last name")


class ProcedureDate(fields.Date):
    def __init__(self, required: bool = False):
        super().__init__(required=required, data_key="Procedure Date")


class ProtocolID(fields.Integer):
    def __init__(self, required: bool = False):
        super().__init__(required=required, data_key="Protocol ID")


class Sex(fields.String):

    # TODO: Should we allow for Unknown?
    sexes = ["Female", "Male"]

    def __init__(self, required: bool = False):
        super().__init__(
            required=required,
            data_key="Sex",
            validate=validate.OneOf(self.sexes),
        )


class SpecimenId(fields.Integer):
    def __init__(self, required: bool = False):
        super().__init__(required=required, data_key="Specimen ID")


class Surgery(fields.String):
    _head_plate_craniotomy = "Head Plate Craniotomy"
    _injection = "Injection"
    _surgeries = [_head_plate_craniotomy, _injection]

    def __init__(self, required: bool = False):
        super().__init__(
            required=required,
            data_key="Surgery",
            validate=validate.OneOf(self._surgeries),
        )


class Version(fields.Field):
    """Version field that deserializes to a Version object."""

    def _deserialize(self, value, *args, **kwargs):
        try:
            return version.Version(value)
        except version.InvalidVersion as e:
            raise ValidationError("Not a valid version.") from e

    def _serialize(self, value, *args, **kwargs):
        return str(value)
