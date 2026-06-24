from langchain_community.document_loaders import Docx2txtLoader

class DocxLoader:
    
    """
    Load DOCX files using Docx2txtLoader.
    """
    def load(self, file_path: str):
        loader = Docx2txtLoader(file_path=file_path)
        return loader.load()