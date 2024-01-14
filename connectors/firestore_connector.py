import os
from google.cloud import firestore

# Set the path to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestore_key\serviceAccountKey.json"

# Initialize Firestore client
db = firestore.Client()


# Specify the collection or path
collection_path = '1-1'


# Read data from Firebase
def get_mishna(perek: str, mishna:str):
    print("getting into firestore_connector")
    # Get data from the specified collection
    try:
        # Query example
        collection_ref = db.collection('pirkey_avot')

        # Simple query
        query = collection_ref.where('chapter', '==', perek)

        # Get documents from the query
        documents = query.stream()

        for doc in documents:
            print(f'{doc.id} => {doc.to_dict()}')

        else:
            print(f"The collection '{collection_path}' is empty.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return documents
