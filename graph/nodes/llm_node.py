from llm.llm_router import LLMRouter
from core.tenant_manager import tenant_manager
from langchain_core.messages import AIMessage, HumanMessage

def llm_node(state):
    tenant = tenant_manager.load_tenant(state.tenant_id)
    llm = LLMRouter(tenant=tenant).get_llm()


    prompt = "\n".join([m.content for m in state.messages])
    prompt = prompt + "\n" + state.final_prompt
    answer = llm.generate(prompt)

    state.messages.append(
        AIMessage(content=answer)
    )
    
    state.answer = answer
    print("MEMORY:", [m.content for m in state.messages])

    return state