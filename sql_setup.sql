-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create documents table with vector support
CREATE TABLE IF NOT EXISTS documents (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id TEXT NOT NULL,
    organization_id TEXT NOT NULL,
    document_name TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(1536),
    metadata JSONB DEFAULT '{}',
    document_type TEXT DEFAULT 'organization'
);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_documents_organization_id ON documents(organization_id);
CREATE INDEX IF NOT EXISTS idx_documents_user_id ON documents(user_id);
CREATE INDEX IF NOT EXISTS idx_documents_document_name ON documents(document_name);
CREATE INDEX IF NOT EXISTS idx_documents_embedding ON documents USING ivfflat (embedding vector_cosine_ops);

-- Enable RLS if needed
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Create a function for vector similarity search
CREATE OR REPLACE FUNCTION match_documents(
    p_org_id text,
    p_user_id text,
    query_embedding vector,
    match_count int DEFAULT 5
)
RETURNS TABLE(
    id bigint,
    user_id text,
    organization_id text,
    document_name text,
    chunk_index int,
    content text,
    metadata jsonb,
    similarity float4
) LANGUAGE sql STABLE AS $$
    SELECT
        documents.id,
        documents.user_id,
        documents.organization_id,
        documents.document_name,
        documents.chunk_index,
        documents.content,
        documents.metadata,
        (1 - (documents.embedding <=> query_embedding)) as similarity
    FROM documents
    WHERE documents.organization_id = p_org_id
    AND documents.user_id = p_user_id
    ORDER BY documents.embedding <=> query_embedding
    LIMIT match_count;
$$;
