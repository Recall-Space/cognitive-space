from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchFieldDataType,
    VectorSearch,
    SearchField,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    SearchableField,
)
from azure.search.documents.models import VectorizedQuery
from cognitive_space.storage import StorageLayer
from datetime import datetime, timezone


class AzureAISearchStorage(StorageLayer):
    def __init__(self, endpoint, api_key, index_name):
        self.endpoint = endpoint
        self.api_key = api_key
        self.index_name = index_name
        self.index_client = SearchIndexClient(
            endpoint=endpoint, credential=AzureKeyCredential(api_key)
        )
        self.search_client = SearchClient(
            endpoint=endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(api_key),
        )

    def create_or_update_index(self, dimensions=1536):
        fields = [
            SimpleField(
                name="id",
                type=SearchFieldDataType.String,
                key=True,
                sortable=True,
                filterable=True,
                facetable=True,
            ),
            SearchableField(name="content", type=SearchFieldDataType.String),
            SearchField(
                name="embedding",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True,
                vector_search_dimensions=dimensions,
                vector_search_profile_name="RecallProfile",
            ),
            SimpleField(
                name="timestamp",
                type=SearchFieldDataType.DateTimeOffset,
                filterable=True,
                sortable=True
            )
        ]

        # Configure the vector search configuration
        vector_search = VectorSearch(
            algorithms=[HnswAlgorithmConfiguration(name="recallHnsw")],
            profiles=[
                VectorSearchProfile(
                    name="RecallProfile", algorithm_configuration_name="recallHnsw"
                )
            ],
        )

        index = SearchIndex(
            name=self.index_name, fields=fields, vector_search=vector_search
        )

        result = self.index_client.create_or_update_index(index)
        return result

    def delete_index(self):
        result = self.index_client.delete_index(self.index_name)
        return result

    def create_or_update(self, data):
        #data["id"] = self._hash_string(data["content"].strip())
        data["timestamp"] = datetime.now(timezone.utc).isoformat()
        result = self.search_client.upload_documents(documents=[data])
        return result

    def read(self, identifier):
        result = self.search_client.get_document(key=identifier)
        return result

    def delete(self, identifier):
        result = self.search_client.delete_documents(documents=[{"id": identifier}])
        return result

    def recall(self, embedding_vector, top_n=5, score_threshold=0.9):
        vector_query = VectorizedQuery(
            vector=embedding_vector, k_nearest_neighbors=top_n, fields="embedding"
        )
        result = self.search_client.search(
            search_text=None, vector_queries=[vector_query], order_by=["timestamp"]
        )
        return [
            {
                #"id": item["id"],
                "content": item["content"],
                "timestamp": item["timestamp"],
                "@search.score": item["@search.score"],
            }
            for item in result
            if item["@search.score"] >= score_threshold
        ]

    def search(self, search_text, top_n=10, score_threshold=0.9):
        result = self.search_client.search(search_text=search_text, top=top_n, order_by=["timestamp"])
        return [
            {
                #"id": item["id"],
                "content": item["content"],
                "timestamp": item["timestamp"],
                "@search.score": item["@search.score"],
            }
            for item in result
            if item["@search.score"] >= score_threshold
        ]

