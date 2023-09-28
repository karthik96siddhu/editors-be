from flask_restful import Resource
from config.db import admin_collection
from flask import request
import os
from dotenv import load_dotenv
from werkzeug.security import check_password_hash
import datetime
import jwt

load_dotenv()

class LoginApi(Resource):

    def post(self):
        try:
            data =  request.get_json()
            username = data.get("username")
            password = data.get("password")
            super_admin = admin_collection.find_one({'username': username})
            if not super_admin:
                return {"message": "User not found"}, 404
            if check_password_hash(super_admin["password"], password):
                # Create a JWT token with user's username and an expiration time
                token = jwt.encode(
                    {
                        'username': username,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=int(os.environ.get('LOGIN_EXPIRATION_TIME')))  # Adjust the expiration time as needed
                    },
                    os.environ.get('SECRET_KEY'),
                    algorithm='HS256'
                )
                return {"token": token, "message": 'Login success'}, 200
            else:
                return {"message": "Invalid credentials"}, 401
        except Exception as e:
            return {"message": "Error while login super-admin", "error": str(e)}, 500
        