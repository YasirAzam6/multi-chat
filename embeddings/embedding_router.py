from embeddings.embed_openai import OpenAIEmbedder
from core.config import config

class EmbeddingRouter:

    """
    Routes embedding requests to the appropriate embedder based on configuration.
    """

    def __init__(self, tenant):
        self.tenant = tenant
        self.model_name = tenant.get("embedding_model", config.EMBEDDING_MODEL)

    
    def get_embedder(self):
        """
        Return the appropraite embedder.
        """

        if self.model_name.startswith("text-embedding"):
            print("Using Embedding model: ", self.model_name)
            return OpenAIEmbedder(model_name=self.model_name)
        

        return OpenAIEmbedder(model_name=self.model_name)