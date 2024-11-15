# 💾 Recall Space Storages
+ **MongoStorage:** Used mongo client to serve as interface to key value pair storage.

```python
from cognitive_space.storage.mongo.mongo_storage import MongoStorage
import os

mongo_storage = MongoStorage(
    db_name="gravity-db", 
    collection_name="gravity-test-collection", 
    uri=os.getenv("MONGO_DB_CONNECTION_STRING"))

# store a document in your collection e.g. gravity-test-collection
mongo_storage.create_or_update(data={
    "id":"some_id",
    "content":"this is an example"})

# get the content and timestamp
mongo_storage.read(identifier="some_id")

# search for words
mongo_storage.search(search_text="example")

# delete the document
mongo_storage.delete(identifier="some_id")

# delete the entire collection
mongo_storage.delete_collection()
```