from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class RAGChatRequest(BaseModel):
    query: str = Field(..., min_length=1)
    thread_id: Optional[str] = None
    include_context: bool = False

class ContextChunk(BaseModel):
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class RAGChatResponse(BaseModel):
    tenant_id: str
    router: Optional[str] = None
    answer: str
    context: Optional[List[ContextChunk]] = None
