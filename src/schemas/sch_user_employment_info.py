from helpers import ma
from marshmallow import fields
from marshmallow.validate import Length, Regexp


class EmploymentInformationSchema(ma.Schema):

    company = fields.String(required=True, validate=Length(max=100), error_messages={
        'required': 'Company is required.',
    })
    employee_id = fields.String(
        validate=[Length(max=32),
                  Regexp(r'^[a-zA-Z0-9]*$', error='Special characters are not allowed.')])
    position = fields.String(validate=Length(max=100))
    hired_date = fields.Date()
