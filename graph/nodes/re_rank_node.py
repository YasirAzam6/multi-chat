from retrieval.rerankers.reraker_openai import RerankerOpenAI

def rerank_node(state):
    reranker = RerankerOpenAI()
    re_ranked_docs = reranker.rerank(
        state.query, state.retrieved_docs
    )
    state.re_ranked_docs = re_ranked_docs
    return state