from flask import request
from flask_restx import Resource, Namespace
from api.extensions import db
from flask_restx import fields

hms_ns = Namespace("hms", description="User Authentications")

verification_pin = hms_ns.model(
    "Verification Pin",
    {
        "pin": fields.Integer(),
    }
)

@hms_ns.route('/verification')
class HelloResource(Resource):
    @hms_ns.expect(verification_pin)
    def post(self):
        """Unique verificaton code"""
        data = request.get_json()
        
        if data.get('pin') == 1234:
            return{'access': 'granted'}
        return{'access': 'declined'}

