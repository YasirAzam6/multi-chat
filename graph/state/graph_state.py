from typing import List, Optional, Any
from langchain_core.documents import Document
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage

class RAGState(BaseModel):
    """
    Represents the state of a RAG (Retrieval-Augmented Generation) process.
    Contains the question, retrieved documents, and re-ranked documents.
    """

    messages: List[BaseMessage] = Field(default_factory=list)

    query: str
    tenant_id: str

    tenant: Optional[str] = None

    retrieved_docs: Optional[List[Document]] = None
    re_ranked_docs: Optional[List[Document]] = None

    final_prompt: Optional[str] = None
    answer: Optional[str] = None

    router: Optional[str] = None