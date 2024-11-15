# 🧠 Suggested AI Brain configurations.
+ Here are some suggestion of AI brain configurations.

## 🗺️Embedding Based Brain

```python
import os
from cognitive_space.brain import Brain
from cognitive_space.storage import AzureAISearchStorage
from cognitive_space.algorithms.embedding_model import EmbeddingEncode
from cognitive_space.algorithms.embedding_model import EmbeddingRecall

index_name = "simple_embedings"
azure_ai_search_storage = AzureAISearchStorage(
    endpoint=os.getenv("AZURE_AI_SEARCH_BASE_URL"),
    api_key=os.getenv("AZURE_AI_SEARCH_API_KEY"),
    index_name=index_name)

embedding_encode = EmbeddingEncode(
    storage_layer= azure_ai_search_storage,
    base_url=os.getenv("EMBEDDINGS_BASE_URL"),
    api_key=os.getenv("EMBEDDINGS_KEY")
)

embedding_recall = EmbeddingRecall(
    storage_layer=azure_ai_search_storage,
    base_url=os.getenv("EMBEDDINGS_BASE_URL"),
    api_key=os.getenv("EMBEDDINGS_KEY"),
)
brain_with_embeddings = Brain(
    cognitive_encoder=embedding_encode,
    cognitive_recall=embedding_recall)

# Encode with embeddings. response_encode is an embedding vector which
# it is already stored on the azure index  
response_encode = brain_with_embeddings.encode("a test for the brain")

# get top 5 results by cosine similarity where threshold
# is bigger than 90%
response_recall = brain_with_embedings.recall(
    "do you know anything about a test for a brain?",
    top_n=5, 
    score_threshold=0.90)
```


## 🌐Gravity Based Brain
```python
import os
from cognitive_space.brain import Brain
from cognitive_space.storage.mongo.mongo_storage import MongoStorage
from cognitive_space.algorithms.gravitational_model import GravitationalRecall
from cognitive_space.algorithms.gravitational_model import GravitationalEncode

collection_name = "gravity-collection"
mongo_storage_gravity = MongoStorage(
    db_name="gravity-db", 
    collection_name=collection_name, 
    uri=os.getenv("MONGO_DB_CONNECTION_STRING"))

mongo_storage_gravity.delete_collection()

gravity_encode = GravitationalEncode(
    storage_layer= mongo_storage_gravity,
    base_url=os.getenv("EMBEDDINGS_BASE_URL"),
    api_key=os.getenv("EMBEDDINGS_KEY")
)

gravity_recall = GravitationalRecall(
    storage_layer=mongo_storage_gravity,
    base_url=os.getenv("EMBEDDINGS_BASE_URL"),
    api_key=os.getenv("EMBEDDINGS_KEY"),
)
brain_with_gravity = Brain(
    cognitive_encoder=gravity_encode,
    cognitive_recall=gravity_recall)
```