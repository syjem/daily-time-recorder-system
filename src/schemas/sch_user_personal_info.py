from marshmallow import fields

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
