from marshmallow import ValidationError


def validate_unique_items(value):
    if value and type(value[0]) is dict:
        unique_items = [
            dict(s) for s in set(frozenset(d.items()) for d in value)
        ]
    else:
        unique_items = set(value)
    if len(value) != len(unique_items):
        raise ValidationError("Must not contain duplicate elements")
