from marshmallow import Schema, fields, validate

from aind_data_schemas import field_definitions as fd
from aind_data_schemas.subschemas import ephys_session_subschemas
from aind_data_schemas.subschemas.ephys_rig_subschemas import DevicesSchema
from aind_data_schemas.validators import validate_unique_items


class EphysRigSchema(Schema):
    version = fd.Version()
    rig_id = fields.Str(data_key="Rig ID")
    devices = fields.Nested(DevicesSchema, data_key="Devices")


class EphysSessionSchema(Schema):

    _institution_aind = "AIND"
    _institution_msp = "MSP"
    _institutions = [_institution_aind, _institution_msp]

    _session_test = "Test"
    _session_foraging_a = "Foraging A"
    _session_spontaneous = "Spontaneous"
    _session_foraging_b = "Foraging B"
    _session_types = [
        _session_test,
        _session_foraging_a,
        _session_spontaneous,
        _session_foraging_b,
    ]

    institution = fields.Str(
        required=True,
        data_key="Institution",
        validate=validate.OneOf(_institutions),
    )
    experimenter_first_name = fd.ExperimenterFirstName(required=True)
    experimenter_last_name = fd.ExperimenterLastName(required=True)
    session_start_time = fields.DateTime(data_key="Session start time")
    specimen_id = fd.SpecimenId(required=True)
    project_id = fields.Int(data_key="Project ID")
    session_type = fields.Str(
        required=True,
        data_key="Session Type",
        validate=validate.OneOf(_session_types),
    )
    stimulus_protocol_id = fields.Int(data_key="Stimulus Protocol ID")
    rig_id = fields.Str(data_key="Rig ID")
    session_end_time = fields.DateTime(data_key="Session end time")
    probes = fields.List(
        fields.Nested(ephys_session_subschemas.ProbeSchema),
        required=True,
        data_key="Probes",
        validate=validate_unique_items,
    )
    lasers = fields.List(
        fields.Nested(ephys_session_subschemas.LaserSchema),
        data_key="Lasers",
        validate=validate_unique_items,
    )
