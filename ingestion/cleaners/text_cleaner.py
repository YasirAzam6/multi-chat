import re
from langchain_core.documents import Document


class TextCleaner:

    """
    Cleans text documents by removing unwanted characters and formatting.
    """

    def clean(self, docs: list[Document]) -> list[Document]:

        cleaned_docs = []
        for doc in docs:
            text = doc.page_content

            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            # Remove non-printable characters
            text = re.sub(r'[^\x20-\x7E]+', ' ', text).strip()

            cleaned_docs.append(
                Document(page_content=text, 
                         metadata=doc.metadata)
            )
        return cleaned_docs

