from utils.env_loader import env_loader
from core.constants import (DEFAULT_EMBEDDING_MODEL, 
                            DEFAULT_LLM_MODEL,
                            SUPABASE_URL,
                            SUPABASE_API_KEY,
                            TENANT_DIR,
                            DEBUG
                            )

class Config:
    """
    Configuration class to manage application settings.
    """

    def __init__(self):
        self.OPENAI_API_KEY = env_loader.get("OPENAI_API_KEY")
        self.SUPABASE_URL = env_loader.get("SUPABASE_URL", SUPABASE_URL)
        self.SUPABASE_API_KEY = env_loader.get("SUPABASE_API_KEY", SUPABASE_API_KEY)

        # Constants
        self.EMBEDDING_MODEL = env_loader.get("EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL)
        self.LLM_MODEL = env_loader.get("LLM_MODEL", DEFAULT_LLM_MODEL)
        # # PATHS
        self.TENANT_ROOT = env_loader.get("TENANT_ROOT", TENANT_DIR)
        self.DEBUG = env_loader.get("DEBUG", str(DEBUG)).lower() == "true"


config = Config()

