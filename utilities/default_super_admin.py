from config.db import admin_collection
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
import os

load_dotenv()

def insert_default_super_admin():
    super_admin = []
    for admin in admin_collection.find():
        super_admin.append(admin)
    if len(super_admin) == 0:
        # To insert super-admin user
        default_super_admin = {
            "username": os.getenv('SUPER_ADMIN_USERNAME'),
            "password": generate_password_hash(os.getenv('SUPER_ADMIN_PASSWORD')) 
        }
        admin_collection.insert_one(default_super_admin)
    return 