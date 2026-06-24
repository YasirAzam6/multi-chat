from langgraph.graph import END
from langchain_core.documents import Document
from langgraph.graph import StateGraph
from core.tenant_manager import tenant_manager


def query_node(state, config):
    """
    A node that handles querying a document store and returning the results.
    """
    
    # tenant = tenant_manager.load_tenant(state.tenant_id)
    # state.tenant = tenant
    return state