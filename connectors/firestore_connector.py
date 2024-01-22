import os
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

class FirestoreConnector:
    def __init__(self):
        # Set the path to your service account key file
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestore_key\serviceAccountKey.json"

        # Initialize Firestore client
        self.db = firestore.Client()

        # Specify the collection or path
        self.collection_path = "pirkey_avot"

    def get_mishna(self, chapter: str, mishna: str):
        results = []  # To store the document data

        try:
            collection_ref = self.db.collection(self.collection_path)

            # Prepare query
            query = (
                collection_ref
                .where(filter=FieldFilter('chapter', '==', chapter))
                .where(filter=FieldFilter('mishna', '==', mishna))
            )

            # Get documents from the query
            documents = query.stream()
            
            # Check if there are any documents
            if documents:
                for doc in documents:
                    results.append(doc.to_dict())
                    print(f'{doc.id} => {doc.to_dict()}')
            else:
                print(f"No documents found with the specified conditions.")

        except Exception as e:
            print(f"An error occurred: {e}")

        return results
