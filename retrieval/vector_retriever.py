from langchain_core.documents import Document
from embeddings.embedding_router import EmbeddingRouter
from vectorstores.supabase_store import supa_base_vector_db
import logging

logger = logging.getLogger(__name__)

class VectorRetriever:
    """
    Handles retrieval of relevant documents based on vector similarity search.
    """
    
    def __init__(self, tenant, top_k=5):
        self.tenant = tenant
        self.top_k = top_k
        self.embedding_router = EmbeddingRouter(tenant.config)
        self.embedder = self.embedding_router.get_embedder()
        
    def retrieve(self, query:str) -> list[Document]:
        """
        Retrieves top_k relevant documents for the given query.
        """
        query_embedding = self.embedder.embed_question(query)
        logger.info(f"Query is : {query}")
        # logger.info(f"Query embedding is: {query_embedding}")
        org_id = self.tenant.config["organization_id"]
        user_id = self.tenant.tenant_id
        matches = supa_base_vector_db.search(
            organization_id= org_id,
            user_id=user_id,
            query_embedding=query_embedding,
            top_k=self.top_k
        )
        print("=" * 50)
        print("MATCH COUNT:", len(matches))

        if matches:
            print("FIRST MATCH:")
            print(matches[0])

        print("=" * 50)
        docs = []
        for match in matches:
            docs.append(Document(
                page_content=match['content'],
                metadata={
                    "similarity": match['similarity'],
                    "document_name": match['document_name'],
                    "chunk_index": match['chunk_index'],
                    "metadata": match['metadata']
                }
            )
            )
        return docs