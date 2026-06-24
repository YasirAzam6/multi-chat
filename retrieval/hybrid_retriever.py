from retrieval.vector_retriever import VectorRetriever
from retrieval.bm25_retriever import BM25Retriever
from langchain_core.documents import Document

class HybridRetriever:
    """
    Hybrid Retriever that combines Vector and BM25 retrieval methods.
    """
    
    def __init__(self, tenant, top_k=5, vector_weight=0.6, bm25_weight=0.4):
        self.tenant = tenant
        self.top_k = top_k
        self.vector_weight = vector_weight
        self.bm25_weight = bm25_weight

        self.vector_retriever = VectorRetriever(tenant, top_k)
        self.bm25_retriever = BM25Retriever(tenant, top_k*2)  # Retrieve more for better merging


    def retrieve(self, query: str):
        """
        Retrieves top_k relevant documents by combining vector and BM25 results.
        """
        vector_docs = self.vector_retriever.retrieve(query)
        bm25_docs = self.bm25_retriever.retrieve(query)

        # Create a score dictionary
        scored = {}

        for i, doc in enumerate(vector_docs):
            scored[doc.page_content] = scored.get(doc.page_content, 0) + (self.vector_weight * (self.top_k - i))
        
        for i, doc in enumerate(bm25_docs):
            scored[doc.page_content] = scored.get(doc.page_content, 0) + (self.bm25_weight * (self.top_k*2 - i))
        
        # Sort documents by combined score
        sorted_docs = sorted(scored.items(), key=lambda item: item[1], reverse=True)

        # Return top_k documents
        final_docs = []
        seen = set()

        for content, _ in sorted_docs:
            for d in vector_docs + bm25_docs:
                if d.page_content == content and content not in seen:
                    final_docs.append(d)
                    seen.add(content)
                    break
            if len(final_docs) >= self.top_k:
                break
        return final_docs