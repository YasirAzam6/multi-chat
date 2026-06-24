from openai import OpenAI
from core.config import config

class RerankerOpenAI:
    """
    Using OpenAI to rerank retrieved documents based on their relevance to the query.
    """

    def __init__(self, model_name: str = "gpt-4.1-mini"):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model_name = model_name

    def rerank(self, query: str, documents):
        reranked_docs = []
        for doc in documents:
            prompt = f""" You are a relevance scorer (1 to 10).
            Query: {query}
            Document: {doc.page_content}
            Return only a number between 1 and 10.
            """
            system_prompt = """
            You are an expert at ranking documents based
            on their relevance to a given query. Score each document
            on a scale of 1 to 10, where 10 is highly relevant and
            1 is not relevant at all.
            """
            res = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
            )
            score_text = res.choices[0].message.content.strip()
            try:
                score = float(score_text)
            except:
                score = 5.0
            reranked_docs.append((doc, score))
        reranked_docs.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, score in reranked_docs]


