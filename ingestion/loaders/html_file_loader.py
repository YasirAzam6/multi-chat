from langchain_community.document_loaders import BSHTMLLoader

class HTMLFileLoader:

    def load(self, file_path: str):
        loader = BSHTMLLoader(file_path=file_path, open_encoding='utf-8')
        return loader.load()