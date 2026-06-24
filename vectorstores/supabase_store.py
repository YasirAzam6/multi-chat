from typing import List, Dict, Any
from supabase import create_client
# from langchain_community.vectorstores import SupabaseVectorStore
# from langchain_openai import OpenAIEmbeddings
from core.config import config
import logging
logger = logging.getLogger(__name__)

class SupabaseVectorDB:
    """
    Wrapper around Supabase Vector Store for storing and retrieving embeddings.
    """
    def __init__(self):
        self.client = create_client(
            supabase_url=config.SUPABASE_URL,
            supabase_key=config.SUPABASE_API_KEY
        )
        self.table = "documents"

    
    def add_embedding(self,user_id: str, organization_id: str, document_name: str,
                      chunks: list[str], embeddings: list[List[float]],
                      metadata: List[Dict[str, Any]] = None,
                      ):
        if metadata is None:
            metadata = [{} for _ in chunks]
        rows = []
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            row = {
                "user_id": user_id,
                "organization_id": organization_id,
                "document_name": document_name,
                "chunk_index": idx,
                "embedding": embedding,
                "metadata": metadata[idx],
                "document_type": "organization",
                "content": chunk
            }
            rows.append(row)    
        logger.info(f"Adding {len(rows)} embeddings to Supabase for tenant_id: {organization_id}")
        result = self.client.table(self.table).insert(rows).execute()
        return result
    
    def search(self, organization_id: str, user_id: str, query_embedding: List[float], top_k: int = 5):
        """
        Calls Supabase to perform a vector similarity search.
        """
        response = self.client.rpc(
            "match_documents",
            {   "p_org_id": organization_id,
                "p_user_id": user_id,
                "query_embedding": query_embedding,
                "match_count": top_k,
            }
        ).execute()
        return response.data

    def get_all_documents(self, organization_id: str, user_id: str):
        """
        Retrieve all documents for a given tenant.
        """
        response = self.client.table(self.table).select("*").eq("organization_id", organization_id).eq("user_id", user_id).execute()
        return response.data
    
    # def load_tenant_config(self, tenant_id: str) -> dict:
    #     """
    #     Load tenant configuration from a local JSON file.
    #     This function will later be replaced with a Supabase fetch.
    #     """
    #     # config_path = os.path.join(CONFIG_ROOT, f"{tenant_id}.json")
    #     config_path = tenant_id + ".json"

    #     if not os.path.exists(config_path):
    #         raise FileNotFoundError(f"Missing tenant config file: {config_path}")

    #     with open(config_path, "r") as f:
    #         data = json.load(f)

    #     return data
    
supa_base_vector_db = SupabaseVectorDB()
# data = supa_base_vector_db.load_tenant_config("tenant_1")
# print(data)


        