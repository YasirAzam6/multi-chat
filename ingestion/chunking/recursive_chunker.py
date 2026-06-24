from langchain_text_splitters import RecursiveCharacterTextSplitter
from core.constants import DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP
from langchain_core.documents import Document


class RecursiveChunker:
    """
    Splits text into smaller chunks using a recursive character-based approach.
    """

    def __init__(self, chunk_size=None, chunk_overlap=None):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size or DEFAULT_CHUNK_SIZE,
            chunk_overlap=chunk_overlap or DEFAULT_CHUNK_OVERLAP,
            separators=["\n\n",
                        "\n",
                        " ",
                        "",
                        ". ",
                        "? ",
                        "! ",
                        "",]
            )
    def chunk(self, docs: list[Document]) -> list[Document]:
        return self.text_splitter.split_documents(docs)
    
    
