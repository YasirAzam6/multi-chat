import os
import tempfile
from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException

from api.dependencies.tenant import get_tenant
from api.schemas.ingestion import IngestResponse
from core.tenant_manager import TenantContext

from ingestion.loaders.generic_loader import GenericLoader
from ingestion.cleaners.text_cleaner import TextCleaner
from ingestion.chunking.recursive_chunker import RecursiveChunker
from embeddings.embedding_router import EmbeddingRouter
from vectorstores.supabase_store import supa_base_vector_db

router = APIRouter(prefix="/v1/ingest", tags=["ingestion"])

@router.post("/file", response_model=IngestResponse)
async def ingest_file(
    file: UploadFile = File(...),
    document_name: str | None = Form(default=None),
    tenant: TenantContext = Depends(get_tenant),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="File name is missing")

    doc_name = document_name or file.filename
    suffix = os.path.splitext(file.filename)[1] or ".txt"

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        docs = GenericLoader().load(tmp_path)
        clean_docs = TextCleaner().clean(docs)
        chunked_docs = RecursiveChunker().chunk(clean_docs)

        embedder = EmbeddingRouter(tenant.config).get_embedder()
        embeddings = embedder.embed_docs(chunked_docs)

        supa_base_vector_db.add_embedding(
            user_id = tenant.tenant_id,
            organization_id = tenant.config["organization_id"],
            document_name=doc_name,
            chunks=[c.page_content for c in chunked_docs],
            embeddings=embeddings,
            metadata=[getattr(c, "metadata", {}) or {} for c in chunked_docs],
        )

        return IngestResponse(
            tenant_id=tenant.tenant_id,
            document_name=doc_name,
            chunks=len(chunked_docs),
            status="ok",
        )
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass
