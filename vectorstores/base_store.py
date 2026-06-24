class BaseVectorStore:

    def add_embeddings(self, tenant_id, texts, embeddings, metadata):
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def query(self, tenant_id, query_embedding, top_k=5):
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def delete_embeddings(self, tenant_id):
        raise NotImplementedError("This method should be overridden by subclasses.")