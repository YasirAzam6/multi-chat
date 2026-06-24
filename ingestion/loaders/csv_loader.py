from langchain_community.document_loaders.csv_loader import CSVLoader

class CsvLoader:

    def load(self, file_path:str):
        loader = CSVLoader(file_path=file_path)
        return loader.load()