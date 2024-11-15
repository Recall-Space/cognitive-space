# ✖️➕ Recall Space algorithms: Embedding Model

+ The Embedding Model is composed  of the `EmbeddingEncode` and `EmbeddingRecall` algorithms.
+ It is the simplest `CognitiveEncode` and `CognitiveRecall` algorithms that we provide, and it's perfect for simple cases.

### 💾Setup the storage.
```python
import os
azure_ai_search_storage = AzureAISearchStorage(
    endpoint=os.getenv("AZURE_AI_SEARCH_BASE_URL"),
    api_key=os.getenv("AZURE_AI_SEARCH_API_KEY"),
    index_name="simple_embedings_2")

# create index on azure
#azure_ai_search_storage.create_or_update_index()

# use text search
azure_ai_search_storage.search("last night drinks!", score_threshold=0.0, top_n=5)
```

### Check 🧠EmbeddingEncode.
```python
from cognitive_space.algorithms.embedding_model import EmbeddingEncode

embedding_encode = EmbeddingEncode(
    storage_layer= azure_ai_search_storage,
    base_url=os.getenv("EMBEDDINGS_BASE_URL"),
    api_key=os.getenv("EMBEDDINGS_KEY")
)
# This will store the embedding and the content on azure_ai_search_storage
# EmbeddingEncode accepts kwargs arguments. content is mandatory.
stored_embeded = embedding_encode.encode("hi, I am Developer G.")
```

### Check 🦉EmbeddingRecall.
```python
from cognitive_space.algorithms.embedding_model import EmbeddingRecall

embedding_recall = EmbeddingRecall(
    storage_layer=azure_ai_search_storage,
    base_url=os.getenv("EMBEDDINGS_BASE_URL"),
    api_key=os.getenv("EMBEDDINGS_KEY"),
)
# EmbeddingRecall accepts kwargs arguments. content is mandatory.
# score_threshold and top_n will passed as kwargs
response = embedding_recall.recall(
    content="what do you know about Developer G", score_threshold=0.0, top_n=10)
```