import os
from ingestion.loaders.docx_loader import DocxLoader
from ingestion.loaders.html_file_loader import HTMLFileLoader
from ingestion.loaders.pdf_loader import PDFLoader
from langchain_community.document_loaders import TextLoader
from ingestion.loaders.csv_loader import CsvLoader

class GenericLoader:
    """"
    A generic loader that selects the appropriate loader based on the file type.
    """
    def __init__(self):
        self.pdf = PDFLoader()
        self.docx = DocxLoader()
        self.html = HTMLFileLoader()
        self.csv = CsvLoader()

    def load(self, file_path: str):
        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            return self.pdf.load(file_path=file_path)
        elif extension == ".docx":
            return self.docx.load(file_path=file_path)
        elif extension == ".html" or extension == ".htm":
            return self.html.load(file_path=file_path)
        elif extension == ".csv":
            return self.csv.load(file_path=file_path)
        else:
            loader = TextLoader(file_path=file_path, encoding='utf-8' )
            return loader.load()
