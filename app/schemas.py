""" Marshmallow schemas for the Student and Presence models. """
from marshmallow import Schema, fields, validate, validates_schema, ValidationError

class StudentSchema(Schema):
    """Schema for the Student model."""
    name = fields.Str(required=True)

class PresenceSchema(Schema):
    """Schema for the Presence model."""
    student_id = fields.Int(required=True)
    day = fields.Int(required=True, validate=validate.Range(min=1, max=7))
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)
    room = fields.Str(required=True)

    @validates_schema
    def validate_time_order(self, data, **kwargs):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        if start_time and end_time:
            if start_time >= end_time:
                raise ValidationError("end_time must be after start_time")
