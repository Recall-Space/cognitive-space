from pymongo import MongoClient
from cognitive_space.storage import StorageLayer
from datetime import datetime, timezone

class MongoStorage(StorageLayer):
    def __init__(
        self, db_name, collection_name, uri
    ):
        """
        Initializes the MongoDBHandler with the specified database and collection.

        Args:
            db_name (str): The name of the database.
            collection_name (str): The name of the collection.
            uri (str): The MongoDB connection string.
        """
        self.client = MongoClient(uri)
        self.db_name = db_name
        self.collection_name = collection_name
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]
        self.signature = ["id", "content", "timestamp"]

    def delete_collection(self):
        """Deletes the entire collection."""
        self.collection.drop()

    def create_or_update(self, data):
        # data only has 'content' key.
        query = {"id": data["id"]}
        update = {
            "$set": {
                "content": data["content"],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        }
        result = self.collection.update_one(query, update, upsert=True)
        return result

    def read(self, identifier):
        query = {"id": identifier}
        result = self.collection.find_one(query)
        return result

    def delete(self, identifier):
        """Deletes a document by its identifier."""
        query = {"id": identifier}
        result = self.collection.delete_one(query)
        return result

    def search(self, search_text):
        """Searches for documents containing the search_text in the content."""
        query = {"content": {"$regex": search_text, "$options": "i"}}
        results = self.collection.find(query)
        return list(results)
    
    def recall(self, identifier):
        pass