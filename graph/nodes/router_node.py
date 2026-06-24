# from openai import OpenAI
# from core.config import config
from llm.llm_router import LLMRouter
from core.tenant_manager import tenant_manager
from langchain_core.messages import HumanMessage


SYSTEM_PROMPT = """
Acting now as a Routing Classifier. Decide whetehr this query requires
knowledge from Tenant documents or if a general LLM response is sufficient.

Output MUST be exactly one of these labels:

- "RAG" -> if the question needs tenant-specific documents, internal policies
or whatever is stored in the tenant's knowledge base.
- "LLM" -> if the question can be answered by a general LLM without any
tenant-specific context.

Example:
Question: What is the project overview of Sharaka AI portal?
Label: RAG
Question: What is the weather today?
Label: LLM
Question: What are the steps in our hiring process?
Label: RAG
Question: How to reset my password?
Label: LLM

Think breifly and output only the "RAG" or "LLM" label.
"""

def router_node(state):
    """
    Router node to classify the query and decide whether to use RAG or LLM.
    """
    
    state.messages.append(
        HumanMessage(content=state.query)
    )

    user_prompt = """
    Classify the following question into "RAG" or "LLM":
    Question: {query}
    """.format(query=state.query)
    tenant = tenant_manager.load_tenant(state.tenant_id)
    
    llm = LLMRouter(tenant=tenant).get_llm()
    decision = llm.generate_simple_call(prompt=user_prompt, system_prompt=SYSTEM_PROMPT)
    if "RAG" in decision:
        state.router = "RAG"
    elif "LLM" in decision:
        state.router = "LLM"
    
    return state