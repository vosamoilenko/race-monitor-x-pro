# firebase/Firebase.py
# -*- coding: utf-8 -*-

import logging
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import ArrayUnion

FIREBASE_ADMIN_CRED_JSON_PATH = '/home/pi/Developer/py/race-monitor-pro-x-firebase-adminsdk-ttnud-d12cb67075.json'
class Firebase:
    def __init__(self):
        try:
            # Initialize Firebase Admin SDK
            self.cred = credentials.Certificate(FIREBASE_ADMIN_CRED_JSON_PATH)
            firebase_admin.initialize_app(self.cred)
            self.db = firestore.client()
            logging.info("Firebase Admin SDK initialized successfully.")
        except Exception as e:
            logging.error("Failed to initialize Firebase with error: {}".format(e))
            raise e  # Re-raise the exception if critical error during initialization

    def push(self, user, data):
        try:
            doc_ref = self.db.collection('data').document(user)
            # Perform the update on Firestore document
            doc_ref.update({
                'history': ArrayUnion([data])
            })
        except Exception as e:
            logging.error(f"Failed to update document for user: {user} with error: {e}")

    def get_all_document_ids(self):
        try:
            # Retrieve all documents from the 'data' collection
            documents = self.db.collection('data').stream()
            document_ids = [doc.id for doc in documents]  # Extract document IDs
            return document_ids
        except Exception as e:
            logging.error(f"Failed to fetch document IDs with error: {e}")
            raise e  # Optionally re-raise the exception

    def get_settings(self):
        try:
            doc_ref = self.db.collection('settings').document('settings')
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()  # Return the settings as a dictionary if the document exists
            else:
                logging.info("No settings document found.")
                return None  # Return None if no settings document exists
        except Exception as e:
            logging.error(f"Failed to get settings with error: {e}")
            raise e  # Re-raise the exception if there's a critical error

    def update_racer(self, racer_id):
        try:
            doc_ref = self.db.collection('settings').document('settings')
            # Update only the currentRacerId field in the settings document
            doc_ref.update({'currentRacerId': racer_id})
            logging.info(f"Updated currentRacerId to {racer_id}")
        except Exception as e:
            logging.error(f"Failed to update currentRacerId with error: {e}")
            raise e  # Re-raise the exception if there's a critical error
