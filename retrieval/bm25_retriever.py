from rank_bm25 import BM25Okapi
from vectorstores.supabase_store import supa_base_vector_db
from langchain_core.documents import Document
import re

class BM25Retriever:
    """
    BM25 Retriever for document retrieval using BM25 algorithm.
    """

    def __init__(self, tenant, top_k=5):
        self.tenant = tenant
        self.top_k = top_k
        
        self.documents = self._load_documents()
        self.bm25 = BM25Okapi([self._tokenize(doc.page_content) for doc in self.documents])

    def _load_documents(self):
        """
        Load documents from the Supabase vector store for the tenant.
        """
        org_id = self.tenant.config["organization_id"]
        docs_data = supa_base_vector_db.get_all_documents(
            organization_id=org_id,
            user_id=self.tenant.tenant_id
        )
        documents = [Document(page_content=data['content'], metadata=data['metadata']) for data in docs_data]
        return documents

    def _tokenize(self, text):
        """
        Tokenizes the input text into words.
        """
        text = re.sub(r'\W+', ' ', text.lower())
        return text.split()

    def retrieve(self, query):
        """
        Retrieve top_k documents relevant to the query using BM25.
        """
        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        top_n_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:self.top_k]
        return [self.documents[i] for i in top_n_indices]
