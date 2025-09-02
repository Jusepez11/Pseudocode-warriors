import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("secrets/testspreadsheet-257500-firebase-adminsdk-8dlsm-1288dc11ca.json")
firebase_admin.initialize_app(cred)