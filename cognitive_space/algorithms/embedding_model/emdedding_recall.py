
from cognitive_space.algorithms.cognitive_recall import CognitiveRecall
from cognitive_space.storage.storage_layer import StorageLayer
from langchain_openai import AzureOpenAIEmbeddings

class EmbeddingRecall(CognitiveRecall):
    def __init__(self, storage_layer: StorageLayer, base_url=None, api_key=None, embedder=None, **kwargs):
        super().__init__(storage_layer)
        self.top_n = 5
        if embedder is None:
            self.embedder = AzureOpenAIEmbeddings(
                base_url=base_url, 
                api_key=api_key)
        else:
            self.embedder = embedder(**kwargs)

    def recall(self, content, **kwargs):
        content_embedding = self.embedder.embed_query(content)
        result = self.storage_layer.recall(embedding_vector=content_embedding, **kwargs)
        return result