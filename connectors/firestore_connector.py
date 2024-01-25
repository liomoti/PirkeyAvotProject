import os
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from models.mishna import Mishna

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
        print(f"results number: {len(documents_list)}")
        return {"results_number": len(documents_list), "results_data": [doc.to_dict() for doc in documents_list]}

# ~~~~~~~~~~~~~ Get methods ~~~~~~~~~~~~~
    
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

    def get_all_tags(self):
        try:
            all_tags = self.collection_ref.document("all_tags") # Get all tags
            all_tags_data = all_tags.get().to_dict()
            return all_tags_data

        except Exception as e:
            print(f"An error occurred: {e}")
# ~~~~~~~~~~~~~ Add methods ~~~~~~~~~~~~~
    def add_mishna(self, mishna: Mishna):
        try:
            mishna_dict = mishna.dict()
            # add mishna
            self.collection_ref.add(mishna_dict)
            print (f"added mishna => {mishna_dict}")
            # get all tags dict
            all_tags_dict = self.get_all_tags()
            # update all_tags dict
            for tag in mishna.tags:
                if tag in all_tags_dict:
                    all_tags_dict[tag] += 1
                else:
                    all_tags_dict[tag] = 1
            # Update all_tags document with the modified/new tags in Firestore
            self.collection_ref.document("all_tags").set(all_tags_dict)
            print (f"updated all_tags dict => {all_tags_dict}")
            return "OK"
        except Exception as e:
            print(f"An error occurred: {e}")
            return "Error"