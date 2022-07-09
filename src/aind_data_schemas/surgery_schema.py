from marshmallow import ValidationError, fields, validates_schema

from aind_data_schemas import field_definitions as fd
from aind_data_schemas.subschemas.surgery_sub_schemas import (
    HeadPlateCraniotomySchema, InjectionSchema)
from aind_data_schemas.validators import validate_unique_items


class SurgerySchema(HeadPlateCraniotomySchema):
    specimen_id = fd.SpecimenId(required=True)
    procedure_date = fd.ProcedureDate(required=True)
    experimenter_first_name = fd.ExperimenterFirstName(required=True)
    experimenter_last_name = fd.ExperimenterLastName(required=True)
    protocol_id = fd.ProtocolID(required=True)
    surgery = fd.Surgery(required=True)
    injections = fields.List(
        fields.Nested(InjectionSchema),
        data_key="Injections",
        validate=validate_unique_items,
    )

    @validates_schema
    def validate_surgery(self, data, **kwargs):
        if data["surgery"] == fd.Surgery._head_plate_craniotomy:
            if "injections" in data:
                raise ValidationError(
                    f"injections should not be set when surgery is "
                    f"{fd.Surgery._head_plate_craniotomy}"
                )
            for hpc_field in HeadPlateCraniotomySchema().fields.keys():
                if hpc_field not in data:
                    raise ValidationError(
                        f"{hpc_field} is required when surgery is "
                        f"{fd.Surgery._head_plate_craniotomy}"
                    )
        if data["surgery"] == fd.Surgery._injection:
            if "injections" not in data:
                raise ValidationError(
                    f"injections should be set when surgery is "
                    f"{fd.Surgery._injection}"
                )
