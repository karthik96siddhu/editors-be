from datetime import datetime

from flask import request
from flask_restful import Resource

from config.db import customer_contact_collection
from utilities.send_mail import send_customer_contact_mail


class CustomerContactApi(Resource):
    def post(self):
        data = request.get_json(silent=True) or {}
        email = data.get('email')

        if not isinstance(email, str) or not email.strip():
            return {'message': 'email is required'}, 400

        contact = {
            'email': email.strip(),
            'phone': data.get('phone'),
            'website': data.get('website'),
            'created_at': datetime.utcnow()
        }

        try:
            result = customer_contact_collection.insert_one(contact)
            send_customer_contact_mail(contact)
            return {
                'message': 'Customer contact submitted successfully',
                'contact_id': str(result.inserted_id)
            }, 201
        except Exception as error:
            return {
                'message': 'Error while submitting customer contact',
                'error': str(error)
            }, 500