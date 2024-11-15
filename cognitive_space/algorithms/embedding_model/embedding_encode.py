

from cognitive_space.algorithms.cognitive_encode import CognitiveEncode
from cognitive_space.storage.storage_layer import StorageLayer
from langchain_openai import AzureOpenAIEmbeddings
import hashlib

class EmbeddingEncode(CognitiveEncode):
    def __init__(self, storage_layer:StorageLayer, base_url=None, api_key=None, embedder=None, **kwargs):
        super().__init__(storage_layer)
        if embedder is None:
            self.embedder = AzureOpenAIEmbeddings(
                base_url=base_url, 
                api_key=api_key)
        else:
            self.embedder = embedder(**kwargs)

    def encode(self, content):
        content_embedding = self.embedder.embed_query(content)
        data = {
            "id": self._hash_string(content),
            "content": content,
            "embedding": content_embedding
        }
        self.storage_layer.create_or_update(data)
        return "encode memory operation was successful "
    
    def _hash_string(self, input_string):
        # Create a new SHA-256 hash object
        hash_object = hashlib.sha256()

        # Update the hash object with the bytes of the input string
        hash_object.update(input_string.encode("utf-8"))

        # Get the hexadecimal representation of the hash
        hex_dig = hash_object.hexdigest()
        return hex_dig