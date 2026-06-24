from llm.llm_router import LLMRouter
from core.tenant_manager import tenant_manager
from langchain_core.messages import AIMessage 

def direct_llm_node(state):
    """
    A node that directly interacts with the LLM to generate a response based on the query.
    """
    tenant = tenant_manager.load_tenant(state.tenant_id)
    llm = LLMRouter(tenant=tenant).get_llm()
    response = llm.generate_simple_call(
    "\n".join([m.content for m in state.messages])
)
    state.messages.append(AIMessage(content=response))
    state.answer = response
    return state