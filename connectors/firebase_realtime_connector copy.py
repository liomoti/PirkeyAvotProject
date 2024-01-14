import firebase_admin
from firebase_admin import credentials, db, exceptions

cred = credentials.Certificate("firebase_key\serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://pirkeyavot-34185-default-rtdb.firebaseio.com/'})

# Get a reference to the database
ref = db.reference()

# Specify the collection or path
collection_path = '1-1'



# Write data to Firebase
# def add_mishna():
#     data = {"name": "John", "age": 30}
#     db.child("users").push(data)

# Read data from Firebase
def get_mishna(perek: str, mishna:str):
    # Get data from the specified collection
    try:
        data = ref.child(collection_path).get()
        if data:
            for key, value in data.items():
                print(f"Document ID: {key}, Data: {value}")
        else:
            print(f"The collection '{collection_path}' is empty.")
    except exceptions.NotFoundError:
        print(f"The collection '{collection_path}' was not found in the Firebase Realtime Database.")
    except Exception as e:
        print(f"An error occurred: {e}")
