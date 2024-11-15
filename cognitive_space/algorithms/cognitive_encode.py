# cognitive_encode.py

from cognitive_space.storage.storage_layer import StorageLayer

class CognitiveEncode:
    def __init__(self, storage_layer: StorageLayer):
        self.storage_layer = storage_layer

    def encode(self, content):
        return self.storage_layer.encode(content)