from marshmallow import Schema, fields


class ProfileSetupSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    password = fields.String(required=True)
    position = fields.String(required=False)
    employee_id = fields.String(required=False)
