import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate("secrets/secret.json")

app = firebase_admin.initialize_app(cred)

db = firestore.client(database_id="cooking-db")


# The below is just to test that the code works on everyone else's computers
users_ref = db.collection("users")
docs = users_ref.stream()

for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")