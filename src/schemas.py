from marshmallow import fields, validates, ValidationError
from helpers import ma


class ProfileSetupSchema(ma.Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    password = fields.String(required=True)
    position = fields.String(required=False)
    employee_id = fields.String(required=False)


class PersonalInformationSchema(ma.Schema):

    def validate(s): return s.strip() != ""

    first_name = fields.String(required=True, validate=validate, error_messages={
                               'validator_failed': 'First name is required.'})
    last_name = fields.String(required=True, validate=validate, error_messages={
                              'validator_failed': 'Last name is required.'})
    email = fields.Email(required=True, validate=validate, error_messages={
                         'validator_failed': 'Email is required.', 'invalid': 'Invalid email address.'})
    birthday = fields.Date(required=True, error_messages={
        'invalid': 'Invalid date format.'})
