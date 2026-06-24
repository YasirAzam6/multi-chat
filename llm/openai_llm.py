from core.config import config
from openai import OpenAI
from llm.base_llm import BaseLLM
# import os

class OpenAILLM(BaseLLM):
    """
    OpenAI LLM implementation.
    System prompt comes from tenant.config JSON.
    """

    def __init__(self, tenant):
        self.tenant = tenant
        self.model_name = tenant.config.get("llm_model", config.LLM_MODEL)
        self.temperature = tenant.config.get("temperature", 0.7)
        self.max_tokens = tenant.config.get("max_tokens", 1500)
        # self.prompts_dir = os.path.join(tenant.prompts_path)
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
    
    # def _load_file(self, file_path):
    #     if os.path.exists(file_path):
    #         with open(file_path, 'r', encoding='utf-8') as f:
    #             return f.read().strip()
    #     return ""
    
    def load_system_prompt(self):
        return (self.tenant.config.get("system_prompt") or "You are a helpful assistant.").strip()

    def generate(self, full_prompt):
        system_prompt = self.load_system_prompt()
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        return response.choices[0].message.content.strip()
    
    def generate_simple_call(self, prompt, system_prompt=None):
        if system_prompt is None:
            system_prompt = """You are a helpful assistant."""
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        return response.choices[0].message.content.strip()