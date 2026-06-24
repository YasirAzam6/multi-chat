from pydantic import BaseModel

class IngestResponse(BaseModel):
    tenant_id: str
    document_name: str
    chunks: int
    status: str
