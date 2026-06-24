from retrieval.vector_retriever import VectorRetriever
from retrieval.bm25_retriever import BM25Retriever
from retrieval.hybrid_retriever import HybridRetriever

class RetrievalRouter:
    """
    Routes retrieval requests to the appropriate retriever based on tenant configuration.
    """
    
    def __init__(self, tenant):
        self.tenant = tenant
        cfg = tenant.config
        self.retriever_type = cfg.get("retriever", "vector")
        self.top_k = cfg.get("top_k", 5)

    
    def get_retriever(self):
        """
        Returns the appropriate retriever instance based on tenant configuration.
        """
        if self.retriever_type == "vector":
            return VectorRetriever(tenant=self.tenant, top_k=self.top_k)
        elif self.retriever_type == "bm25":
            return BM25Retriever(tenant=self.tenant, top_k=self.top_k)
        elif self.retriever_type == "hybrid":
            return HybridRetriever(tenant=self.tenant, top_k=self.top_k)
        else:
            return VectorRetriever(tenant=self.tenant, top_k=self.top_k)
        
        


        