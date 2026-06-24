from llm.prompt_manager import PromptManager
from core.tenant_manager import tenant_manager

def prompt_node(state, config):
    tenant = tenant_manager.load_tenant(state.tenant_id)
    prompt_manager = PromptManager(tenant=tenant)
    final_prompt = prompt_manager.build_full_prompt(
        user_query=state.query, context_docs=state.re_ranked_docs
    )
    state.final_prompt = final_prompt
    return state