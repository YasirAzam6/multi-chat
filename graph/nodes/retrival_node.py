from retrieval.retrieval_router import RetrievalRouter
from core.tenant_manager import tenant_manager

def retrieval_node(state):
    """
    A node that handles retrieval of documents based on a query.
    """
    tenant = tenant_manager.load_tenant(state.tenant_id)
    router = RetrievalRouter(tenant=tenant)
    retriever = router.get_retriever()

    question = state.query
    retrieved_docs = retriever.retrieve(question)
    state.retrieved_docs = retrieved_docs
    return state