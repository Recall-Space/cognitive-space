# brain.py

from cognitive_space.algorithms.cognitive_encode import CognitiveEncode
from cognitive_space.algorithms.cognitive_recall import CognitiveRecall
from cognitive_space.algorithms.cognitive_synthesis import CognitiveSynthesis

class Brain:
    def __init__(self, cognitive_encoder: CognitiveEncode= None, cognitive_recall:CognitiveRecall= None, cognitive_systhesis: CognitiveSynthesis = None):
        self.cognitive_encoder = cognitive_encoder
        self.cognitive_recall = cognitive_recall
        self.cognitive_systhesis = cognitive_systhesis

    def encode(self, content, **kwargs):
        return self.cognitive_encoder.encode(content,**kwargs)

    def recall(self, content, **kwargs):
        return self.cognitive_recall.recall(content, **kwargs)

    def synthesize(self, **kwargs):
        return self.cognitive_systhesis.synthesize(**kwargs)