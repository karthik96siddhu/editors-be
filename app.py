from flask import Flask, render_template
from flask_restful import Api
from flask_cors import CORS
from dotenv import load_dotenv
from flask_mail import Mail
import os
from resources.user import UserListApi, UserApi
from utilities.send_mail import send_mail

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
app = Flask(__name__)

# configuration of mail
app.config['MAIL_SERVER']=os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

CORS(app)
mail =  Mail(app)
api = Api(app)

api.add_resource(UserListApi, '/api/v1/users', methods=["GET", "POST"])
api.add_resource(UserApi, '/api/v1/user/<string:id>', methods=["GET", "PUT", "DELETE"])

@app.route("/")
def home():
    return 'Hello worl!'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)