# storage_layer.py

from abc import ABC, abstractmethod

class StorageLayer(ABC):

    @abstractmethod
    def create_or_update(self, data):
        pass

    @abstractmethod
    def read(self, identifier):
        pass

    @abstractmethod
    def delete(self, identifier):
        pass

    @abstractmethod
    def recall(self, identifier):
        pass

    @abstractmethod
    def search(self, identifier):
        pass