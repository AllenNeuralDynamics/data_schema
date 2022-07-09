from marshmallow import INCLUDE, Schema, fields, validate

from aind_data_schemas import field_definitions as fd


class MouseSchema(Schema):
    class Meta:
        # Allow for unknown fields beyond what's defined below
        unknown = INCLUDE

    version = fd.Version(required=True, description="schema version")
    specimen_id = fd.SpecimenId(required=True)
    sex = fd.Sex(required=True)
    date_of_birth = fd.DateOfBirth(required=True)
    genotype = fields.Str(required=True, data_key="Genotype")
    background_strain = fields.Str(
        required=True,
        data_key="Background Strain",
        validate=validate.OneOf(["C57BL/6J", "BALB/c"]),
    )
    light_cycle = fields.Str(
        required=True,
        data_key="Light cycle",
        validate=validate.OneOf(["regular", "reverse"]),
    )
    source = fields.Str(
        data_key="Source",
        description=(
            "If the mouse was not bred in house, "
            "where was it acquired from."
        ),
    )
    restrictions = fields.Str(
        data_key="Restrictions",
        description="Any restrictions based on specimen source",
    )
    breeding_group = fields.Str(data_key="Breeding Group")
    maternal_id = fields.Number(data_key="Maternal ID")
    maternal_genotype = fields.Str(data_key="Maternal genotype")
    paternal_id = fields.Number(data_key="Paternal ID")
    paternal_genotype = fields.Str(data_key="Paternal genotype")
    home_cage_enrichment = fields.Str(
        data_key="Home cage enrichment",
        validate=validate.OneOf(["none", "running wheel", "other"]),
    )
    water_restriction_protocol = fields.Number(
        data_key="Water restriction protocol"
    )
    training_protocol = fields.Number(data_key="Training protocol")
