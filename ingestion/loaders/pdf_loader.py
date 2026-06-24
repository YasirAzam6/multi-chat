from langchain_community.document_loaders import PyPDFLoader

class PDFLoader:

    """
    Load PDF files using PyPdfLoader.
    """
    def load(self, file_path: str):
        loader = PyPDFLoader(file_path=file_path)
        return loader.load()