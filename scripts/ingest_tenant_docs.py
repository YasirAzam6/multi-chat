from ingestion.loaders.generic_loader import GenericLoader
from ingestion.cleaners.text_cleaner import TextCleaner
from ingestion.chunking.recursive_chunker import RecursiveChunker

loader = GenericLoader()
cleaner = TextCleaner()
chunker = RecursiveChunker()

def ingest_tenant_docs(file_path:str) -> list:
    """
    Ingests tenant documents by loading, cleaning, and chunking them.
    
    Args:
        file_path (str): The path to the tenant document file."""
    
    # Load documents
    documents = loader.load(file_path=file_path)

    # Clean documents
    cleaned_docs = cleaner.clean(documents)

    # Chunk documents
    chunked_docs = chunker.chunk(cleaned_docs)

    return chunked_docs