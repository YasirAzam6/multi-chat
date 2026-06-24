from llm.openai_llm import OpenAILLM
from core.config import config


class LLMRouter:
    """
    Selects the correct llm based on tenant configuration.
    """

    def __init__(self, tenant):
        self.tenant = tenant


    def get_llm(self):
        model = self.tenant.config.get("llm_model", config.LLM_MODEL)

        if model.startswith("gpt"):
            return OpenAILLM(self.tenant)
    

        return OpenAILLM(self.tenant)
        