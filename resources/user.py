from flask_restful import Resource
from flask import request
from bson import ObjectId
from pymongo import ReturnDocument
import pymongo
from config.db import collection
from datetime import datetime
from utilities.send_mail import send_mail
from utilities.generate_doc import convert_json_to_docx_table
from wrapper.jwt_required import jwt_required

class UserListApi(Resource):

    @jwt_required
    def get(self):
        try:
            users = []
            for doc in collection.find().sort('created_at', pymongo.DESCENDING):
                document = {
                "_id": str(doc["_id"]),
                "studio_name" : doc['studio_name'],
                "email" : doc['email'],
                "contact_number" : doc['contact_number'],
                "couple_name" : doc['couple_name'],
                "wedding_date" : doc['wedding_date'],
                "source_link" : doc['source_link'],
                "file_size" : doc['file_size'],
                "highlight" : doc['highlight'],
                "music_option" : doc['music_option'],
                "order_date" : doc['order_date'],
                "description" : doc['description'],
                "created_at" : str(doc['created_at']) 
                }
                users.append(document)
            return {"data": users, "message": "documents fetched successfully"},200
        except Exception as e:
            return {"message": "Error while fetching documents", "error": str(e)}, 500

    def post(self):
        try:
            user = request.get_json()
            new_document = {
                "studio_name" : user['studio_name'],
                "email" : user['email'],
                "contact_number" : user['contact_number'],
                "couple_name" : user['couple_name'],
                "wedding_date" : user['wedding_date'],
                "source_link" : user['source_link'],
                "file_size" : user['file_size'],
                "highlight" : user['highlight'],
                "music_option" : user['music_option'],
                "order_date" : user['order_date'],
                "description" : user['description'],
                "created_at" : datetime.utcnow()
            }
            result = collection.insert_one(new_document)
            if result.inserted_id:
                send_mail(new_document)
                return {"message": "Document created successfully", "document_id": str(result.inserted_id)}, 201
            else:
                return {"message": "Document creation failed"}, 500
        except Exception as e:
            return {"message": "Error while adding document", "error": str(e)}, 500
        

class UserApi(Resource):

    @jwt_required
    def get(self, id):
        try:
            user = {}
            document = collection.find_one({"_id": ObjectId(id)})
            if document:
                user = {
                "_id": str(document["_id"]),
                "studio_name" : document['studio_name'],
                "email" : document['email'],
                "contact_number" : document['contact_number'],
                "couple_name" : document['couple_name'],
                "wedding_date" : document['wedding_date'],
                "source_link" : document['source_link'],
                "file_size" : document['file_size'],
                "highlight" : document['highlight'],
                "music_option" : document['music_option'],
                "order_date" : document['order_date'],
                "description" : document['description'],
                "created_at" : str(document['created_at']) 
                }
                # resp = convert_json_to_docx_table(user)
                # print(resp)
                return {"user": user, "message": "success"}, 200
            else:
                return {"message": "document not found!"}, 404
        except Exception as e:
            return {"message": "Error while fetching document", "error": str(e)}, 500
    
    def put(self, id):
        try:
            document = request.get_json()
            user = {
                    "studio_name" : document['studio_name'],
                    "email" : document['email'],
                    "contact_number" : document['contact_number'],
                    "couple_name" : document['couple_name'],
                    "wedding_date" : document['wedding_date'],
                    "source_link" : document['source_link'],
                    "file_size" : document['file_size'],
                    "highlight" : document['highlight'],
                    "music_option" : document['music_option'],
                    "order_date" : document['order_date'],
                    "description" : document['description'],
                    }
            query = {"_id": ObjectId(id)}
            update = {"$set": {**user}}
            updated_document = collection.find_one_and_update(
                filter=query,
                update=update,
                return_document=ReturnDocument.AFTER
            )
            if updated_document:
                updated_user = {
                    "_id": str(updated_document["_id"]),
                    "studio_name" : updated_document['studio_name'],
                    "email" : updated_document['email'],
                    "contact_number" : updated_document['contact_number'],
                    "couple_name" : updated_document['couple_name'],
                    "wedding_date" : updated_document['wedding_date'],
                    "source_link" : updated_document['source_link'],
                    "file_size" : updated_document['file_size'],
                    "highlight" : updated_document['highlight'],
                    "music_option" : updated_document['music_option'],
                    "order_date" : updated_document['order_date'],
                    "description" : updated_document['description'],
                    "created_at" : str(updated_document['created_at']) 
                }
                return {"data": updated_user, "message": "updated document successfully"},200
            else:
                return {"message": "Failed to update document"}, 404
        except Exception as e:
            return {"message": "Error while updating document", "error": str(e)}, 500
    
    @jwt_required
    def delete(self, id):
        try:
            document = collection.find_one_and_delete({"_id": ObjectId(id)})
            if document:
                return {"message": "Document deleted successfully"}, 200
            else:
                return {"message": "Failed to delete document"}, 404
        except Exception as e:
            return {"message": "Error while deleting document", "error": str(e)}, 500
        