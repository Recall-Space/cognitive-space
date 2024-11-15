from cognitive_space.algorithms.cognitive_recall import CognitiveRecall
from cognitive_space.storage.storage_layer import StorageLayer
from langchain_openai import AzureOpenAIEmbeddings
import numpy as np
from datetime import datetime, timezone

class GravitationalRecall(CognitiveRecall):
    def __init__(self, 
                 storage_layer: StorageLayer, 
                 model_name=None,
                 base_url=None, 
                 api_key=None, 
                 embedder=None,
                 #learning_rate=None,
                 #iterations=None,
                 **kwargs):
        super().__init__(storage_layer)
        self.model_name = model_name or "GravitationalEmbeddings"
        if embedder is None:
            self.embedder = AzureOpenAIEmbeddings(
                base_url=base_url, 
                api_key=api_key)
        else:
            self.embedder = embedder(**kwargs)
        self.G = 1.0  # Gravitational constant (can be adjusted for scaling)
        #self.learning_rate = learning_rate
        #self.iterations = iterations

    def set_system_embeddings(self):
        universe_content = self.storage_layer.read(identifier=str(self.model_name)) or []
        if universe_content != []:
            self.embeddings_list_dict = universe_content["content"]
            # Convert embeddings to a numpy array
            self.embeddings = np.array([each["embedding"] for each in self.embeddings_list_dict]).astype(float)
            self.total_embeddings = len(self.embeddings)
        else:
            self.embeddings_list_dict = []
            self.embeddings = np.array([])
            self.total_embeddings = 0
        # Automatically set learning_rate and iterations if not provided
        self.learning_rate = 1.0 / np.sqrt(self.total_embeddings + 1)
        self.iterations = min(1000, 10 * self.total_embeddings)

    def recall(self, content: str, top_n=4):
        """
        Recall the top N memories closest to the gravitational attraction of the query embedding
        using cosine similarity.

        :param content: Input text to recall similar memories.
        :param top_n: Number of closest memories to retrieve.
        :return: List of dictionaries containing properties of the top N recalled memories.
        """
        self.set_system_embeddings()
        # Compute the embedding of the input content
        query_embedding = self.embedder.embed_query(content)
        query_embedding = np.array(query_embedding).astype(float)

        # Ensure we have embeddings to compare against
        if self.total_embeddings == 0:
            print("No embeddings available to recall.")
            return []

        # Iteratively adjust the query embedding under gravitational influence
        for _ in range(self.iterations):
            differences = self.embeddings - query_embedding  # Shape: (total_embeddings, embedding_dim)
            distances = np.linalg.norm(differences, axis=1)
            # Avoid division by zero
            distances[distances == 0] = np.inf
            # Compute the force components
            forces = differences / distances[:, np.newaxis] ** 3  # Shape: (total_embeddings, embedding_dim)
            # Sum the forces to get the gradient
            grad = np.sum(forces, axis=0)
            # Update the query embedding
            query_embedding += self.learning_rate * grad

        # Compute distances between adjusted query embedding and stored embeddings
        distances = np.linalg.norm(self.embeddings - query_embedding, axis=1)

        # Get indices of the top N closest memories
        recalled_indices = np.argsort(distances)[:top_n]

        # Retrieve the properties of the top N memories
        recalled_memories = [{
            "content": self.embeddings_list_dict[idx]["content"],
            "timestamp": self.embeddings_list_dict[idx]["timestamp"],
            "euclidian_distance": round(distances[idx], 4)
        } for idx in recalled_indices]
        return recalled_memories