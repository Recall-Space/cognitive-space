from cognitive_space.algorithms.cognitive_encode import CognitiveEncode
from cognitive_space.storage.storage_layer import StorageLayer
from langchain_openai import AzureOpenAIEmbeddings
import numpy as np
import hashlib
from datetime import datetime, timezone

class GravitationalEncode(CognitiveEncode):
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
        self.set_system_embeddings()

    def set_system_embeddings(self):
        universe_content = self.storage_layer.read(identifier=str(self.model_name)) or []
        if universe_content!=[]:
            self.embeddings_list_dict = universe_content["content"]
            # each-> DICT: id, timestamp, content, embedding
            #np.array(embeddings)
            self.embeddings = np.array([each["embedding"] for each in self.embeddings_list_dict])
            self.total_embeddings = len(self.embeddings)
        else:
            self.embeddings_list_dict = []
            self.embeddings = np.array([])
            self.total_embeddings = 0
        # Automatically set learning_rate and iterations 
        self.learning_rate = 1.0 / np.sqrt(self.total_embeddings + 1)
        #self.learning_rate = 0.00001
        self.iterations = min(1000, 10 * self.total_embeddings)
        #self.iterations = 0
        print(f"self.learning_rate: {self.learning_rate}")
        print(f"self.iterations: {self.iterations}")

    def encode(self, content):
        embedding = self.embedder.embed_query(content)
        sub_content = {
            "id": self._hash_string(content),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "content":content,
            "embedding": embedding
        }
        self.embeddings_list_dict.append(sub_content)
        self.embeddings = np.array([each["embedding"] for each in self.embeddings_list_dict])
        self.total_embeddings = len(self.embeddings)
        self.minimize_potential_energy()
        self.set_system_embeddings()
        return "encode memory operation was successful "
    
    def gradients(self):
        """
        Calculate the gradients of the potential energy with respect to the embeddings.

        :return: Gradients of the embeddings.
        """
        distances = self.pairwise_distances()
        np.fill_diagonal(distances, np.inf)  # Avoid self-interaction
        inv_distances = 1.0 / distances
        grad = np.zeros_like(self.embeddings)
        for i in range(self.total_embeddings):
            diff = self.embeddings[i] - self.embeddings
            grad[i] = np.sum(diff * (inv_distances[:, i][:, np.newaxis]**2), axis=0)
        return grad
    
    def minimize_potential_energy(self, tolerance=1e-5):
        """
        Use gradient descent to minimize the potential energy of the memory system with early stopping.
        """
        print(f"""
        Minimizing Potential Energy (Encoding).
        Initial Learning rate: {self.learning_rate}
        Max iterations: {self.iterations}
        Tolerance for early stopping: {tolerance}
        ------------------------------------
        """)
        prev_potential_energy = self.potential_energy()
        for i in range(self.iterations):
            grad = self.gradients()
            self.embeddings -= self.learning_rate * grad
            potential_energy = self.potential_energy()
            energy_change = abs(potential_energy - prev_potential_energy)
            if i % 50 == 0 or energy_change < tolerance:
                print(f"Iteration {i}: Potential Energy = {potential_energy}, Energy Change = {energy_change}")
            if energy_change < tolerance:
                print(f"Early stopping at iteration {i} with energy change {energy_change}")
                break
            prev_potential_energy = potential_energy
        # Update the embeddings in the storage layer after optimization
        for idx, each in enumerate(self.embeddings_list_dict):
            each["embedding"] = self.embeddings[idx].tolist()
        data = {
            "id": str(self.model_name),
            "content": self.embeddings_list_dict
        }
        self.storage_layer.create_or_update(data)
        return "Optimization completed with early stopping."
    
    def potential_energy(self):
        """
        Calculate the total potential energy of the memory system.

        :return: Total potential energy.
        """
        distances = self.pairwise_distances()
        np.fill_diagonal(distances, np.inf)  # Avoid self-interaction
        try:
            energy = -self.G * np.sum(1 / distances)
        except:
            energy = 0
        return energy
    
    def pairwise_distances(self):
        """
        Calculate the pairwise distances between all memory embeddings.

        :return: A 2D numpy array of distances.
        """
        distances = np.linalg.norm(self.embeddings[:, np.newaxis] - self.embeddings[np.newaxis, :], axis=2)
        return distances
    
    def _hash_string(self, input_string):
        # Create a new SHA-256 hash object
        hash_object = hashlib.sha256()

        # Update the hash object with the bytes of the input string
        hash_object.update(input_string.encode("utf-8"))

        # Get the hexadecimal representation of the hash
        hex_dig = hash_object.hexdigest()
        return hex_dig