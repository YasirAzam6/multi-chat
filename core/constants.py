# TENANT_DIR = "app/tenants"
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

TENANT_DIR = os.path.join(PROJECT_ROOT, "tenants")
DEBUG = False

DEFAULT_CHUNK_SIZE = 512
DEFAULT_CHUNK_OVERLAP = 64

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-large"
DEFAULT_LLM_MODEL = "gpt-4o"

TENANT_CONFIG_FILE = "config.json"
TENANT_PROMPT_DIR = "prompts"
TENANT_DOCS_DIR = "docs"
TENANT_BITS_DIR = "agent_bits"


SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY", "").strip()