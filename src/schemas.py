from marshmallow import fields, validates, ValidationError
from marshmallow.validate import Length, Regexp
from helpers import ma


class PersonalInformationSchema(ma.Schema):

    def validate(s): return s.strip() != ""

    first_name = fields.String(validate=validate, error_messages={
                               'validator_failed': 'First name is required.'})
    last_name = fields.String(validate=validate, error_messages={
                              'validator_failed': 'Last name is required.'})
    email = fields.Email(validate=validate, error_messages={
                         'validator_failed': 'Email is required.', 'invalid': 'Invalid email address.'})
    birthday = fields.Date(error_messages={
        'invalid': 'Invalid date format.'})


class EmploymentInformationSchema(ma.Schema):

    company = fields.String(required=True, validate=Length(max=100), error_messages={
        'required': 'Company is required.',
    })
    employee_id = fields.String(
        validate=[Length(max=32),
                  Regexp(r'^[a-zA-Z0-9]*$', error='Special characters are not allowed.')])
    position = fields.String(validate=Length(max=100))
    hired_date = fields.Date()


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
