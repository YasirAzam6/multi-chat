import requests
from typing import List, Dict, Any
from core.config import config
import logging

logger = logging.getLogger(__name__)

class SupabaseVectorDB:
    """
    Wrapper around Supabase Vector Store using the stable 'requests' library
    to bypass Vercel/httpx threading OS limitations.
    """
    def __init__(self):
        self.table = "documents"
        self.base_url = config.SUPABASE_URL
        
        # Standard headers required by the Supabase REST API
        self.headers = {
            "apikey": config.SUPABASE_API_KEY,
            "Authorization": f"Bearer {config.SUPABASE_API_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation" # Ensures the inserted rows are returned
        }
    
    def add_embedding(self, user_id: str, organization_id: str, document_name: str,
                      chunks: list[str], embeddings: list[List[float]],
                      metadata: List[Dict[str, Any]] = None):
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
        
        # Direct REST API POST for Insert
        url = f"{self.base_url}/rest/v1/{self.table}"
        response = requests.post(url, headers=self.headers, json=rows)
        response.raise_for_status() # Raises an exception if the HTTP request failed
        return response.json()
    
    def search(self, organization_id: str, user_id: str, query_embedding: List[float], top_k: int = 5):
        """
        Calls the Supabase RPC directly to perform a vector similarity search.
        """
        url = f"{self.base_url}/rest/v1/rpc/match_documents"
        payload = {
            "p_org_id": organization_id,
            "p_user_id": user_id,
            "query_embedding": query_embedding,
            "match_count": top_k
        }
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def get_all_documents(self, organization_id: str, user_id: str):
        """
        Retrieve all documents for a given tenant via standard GET request.
        """
        url = f"{self.base_url}/rest/v1/{self.table}?organization_id=eq.{organization_id}&user_id=eq.{user_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
supa_base_vector_db = SupabaseVectorDB()