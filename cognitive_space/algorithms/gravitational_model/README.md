# ✖️➕ Recall Space algorithms: Gravitational Model

+ The Embedding Model is composed  of the `GravitationalEncode` and `GravitationalRecall` algorithms.
+ It is the craziest `CognitiveEncode` and `CognitiveRecall` algorithms that we provide, and it's perfect for having fun.

### 💾Setup the storage.
```python
from cognitive_space.storage.mongo.mongo_storage import MongoStorage
import os

mongo_storage = MongoStorage(
    db_name="gravity-db", 
    collection_name="gravity-test-collection", 
    uri=os.getenv("MONGO_DB_CONNECTION_STRING"))

```

### Check 🧠GravitationalEncode.
```python
from cognitive_space.algorithms.gravitational_model import GravitationalEncode

gravitational_encode = GravitationalEncode(
    storage_layer=mongo_storage,
    base_url=os.getenv("EMBEDDINGS_BASE_URL"),
    api_key=os.getenv("EMBEDDINGS_KEY"),
    )
# This process will run gradient descent to optimize the potential gravitational
# energy of your system of memories.
gravitational_encode.encode(content="i am Gari, i like the color white")
```

### Check 🦉Gravitational Recall.
```python
from cognitive_space.algorithms.gravitational_model import GravitationalRecall

gravitational_recall = GravitationalRecall(
    storage_layer=mongo_storage,
    base_url=os.getenv("EMBEDDINGS_BASE_URL"),
    api_key=os.getenv("EMBEDDINGS_KEY")
    )

gravitational_recall.recall(
    content="what do you know about Developer G", top_n=4)
```