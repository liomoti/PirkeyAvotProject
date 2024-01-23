import os
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

class FirestoreConnector:

    COLLECTION_PATH = "pirkey_avot"

    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestore_key\serviceAccountKey.json" # Set the path to service account key file
        self.db = firestore.Client() # Initialize Firestore client
        self.collection_ref = self.db.collection(self.COLLECTION_PATH) # Get Collection


    def __execute_query(self, query) -> dict:
        print(f"executing query: {query}")
        documents = query.stream()
        documents_list = list(documents)
        print(f"results: {documents_list}")
        return {"results_number": len(documents_list), "results_data": [doc.to_dict() for doc in documents_list]}


    def get_mishna(self, chapter: str, mishna: str):
        try:
            # Making Query
            query = (
                self.collection_ref
                .where(filter=FieldFilter('chapter', '==', chapter))
                .where(filter=FieldFilter('mishna', '==', mishna))
            )
            return self.__execute_query(query=query)
        except Exception as e:
            print(f"An error occurred: {e}")
    

    def get_mishna_by_tags(self, tags):
        try:
            # Making Query
            query = (
                self.collection_ref
                .where(filter=FieldFilter('tags', 'array_contains_any', tags))
            )
            return self.__execute_query(query=query)
        except Exception as e:
            print(f"An error occurred: {e}")
            
    def get_mishna_by_text(self, text):
        try:
            documents_list = list(self.collection_ref.stream()) # Get all data
            matching_documents = [doc.to_dict() for doc in documents_list if text in doc.to_dict().get("text", "")]
            return {"results_number": len(matching_documents), "results_data": matching_documents}
        except Exception as e:
            print(f"An error occurred: {e}")
