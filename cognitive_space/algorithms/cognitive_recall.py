# cognitive_recall.py

from cognitive_space.storage.storage_layer import StorageLayer

class CognitiveRecall:
    def __init__(self, storage_layer: StorageLayer):
        self.storage_layer = storage_layer

    def recall(self, content, **kwagrs):
        return self.storage_layer.recall(content=content, **kwagrs)