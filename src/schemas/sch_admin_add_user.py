from marshmallow import fields, validates, ValidationError
from helpers import ma


class AdminAddUserSchema(ma.Schema):
    def validate_non_empty(s):
        return s.strip() != ""

    first_name = fields.String(
        required=True,
        validate=validate_non_empty,
        error_messages={'validator_failed': 'First name is required.'}
    )
    last_name = fields.String(
        required=True,
        validate=validate_non_empty,
        error_messages={'validator_failed': 'Last name is required.'}
    )
    email = fields.Email(
        required=True,
        validate=validate_non_empty,
        error_messages={
            'validator_failed': 'Email is required.',
            'invalid': 'Invalid email address.'
        }
    )
    birthday = fields.Date(
        error_messages={'invalid': 'Invalid date format.'}
    )
    position = fields.String(
        required=True,
        validate=validate_non_empty,
        error_messages={'validator_failed': 'Position is required.'}
    )
    password = fields.String(
        required=True,
        validate=validate_non_empty,
        error_messages={'validator_failed': 'Password is required.'}
    )

    @validates("password")
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError(
                "Password must be at least 8 characters long.")
