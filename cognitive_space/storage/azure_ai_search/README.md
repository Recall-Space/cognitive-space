# 💾 Recall Space Storages
+ **AzureAISearchStorage:** Used Azure AI search client to serve as interface to azure vector indexes.

```python
import os
azure_ai_search_storage = AzureAISearchStorage(
    endpoint=os.getenv("AZURE_AI_SEARCH_BASE_URL"),
    api_key=os.getenv("AZURE_AI_SEARCH_API_KEY"),
    index_name="simple_embedings_2")

# create index on azure
azure_ai_search_storage.create_or_update_index()

# use text search
azure_ai_search_storage.search("last night drinks!", score_threshold=0.0, top_n=5)
```