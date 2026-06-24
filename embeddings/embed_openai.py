from langchain_openai import OpenAIEmbeddings
from core.config import config
from langchain_core.documents import Document
import logging
import time

logger = logging.getLogger(__name__)


class OpenAIEmbedder:
    """
    OpenAI Embedder using Langchain's OpenAIEmbeddings.
    """

    def __init__(self, model_name: str= None, batch_size: int = 64, max_retries: int = 3):
        self.model_name = model_name or config.EMBEDDING_MODEL
        self.batch_size = batch_size
        self.max_retries = max_retries

        self.embedder  = OpenAIEmbeddings(
            model = self.model_name,
            openai_api_key=config.OPENAI_API_KEY
        )
    
    def extract_texts(self, items):
        texts = []
        for item in items:
            if isinstance(item, Document):
                texts.append(item.page_content)
            else:
                texts.append(str(item))
        return texts

    def _batch(self, items):
        for i in range(0, len(items), self.batch_size):
            yield items[i:i + self.batch_size]

    def embed_docs(self, documents: list[Document]) -> list[list[float]]:
        texts = self.extract_texts(documents)
        embeddings = []
        for batch in self._batch(texts):
            retries = 0
            while True:
                try:
                    logger.info(f"Embedding batch of size {len(batch)} using model {self.model_name}")
                    batch_embeddings = self.embedder.embed_documents(batch)
                    embeddings.extend(batch_embeddings)
                    break
                except Exception as e:
                    retries += 1
                    if retries > self.max_retries:
                        logger.error(f"Failed to embed batch after {self.max_retries} retries.")
                        raise e
                    
                    wait_time = 2 ** retries
                    logger.info(f"Retrying in {wait_time} seconds...")
                    logger.warning(f"Error during embedding: {e}. Retrying {retries}/{self.max_retries}...")
                    time.sleep(wait_time)
        return embeddings



    def embed_question(self, question: str) -> list[float]:
        return self.embedder.embed_query(question)
    