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
