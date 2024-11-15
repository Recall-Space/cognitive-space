# cognitive_synthesis.py

from cognitive_space.storage.storage_layer import StorageLayer

class CognitiveSynthesis:
    def __init__(self, storage_layer: StorageLayer):
        self.storage_layer = storage_layer

    def synthesize(self, encoded_data1, encoded_data2):
        return self.storage_layer.synthesize(encoded_data1, encoded_data2)