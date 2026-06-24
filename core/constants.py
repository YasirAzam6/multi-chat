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


SUPABASE_URL = "https://xlruzehlbbjehuzhytwn.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhscnV6ZWhsYmJqZWh1emh5dHduIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDUzNTAxNCwiZXhwIjoyMDY2MTExMDE0fQ.RosLV-YxmXr2k9Cwvs_ZMoShmsj-PmZlKLw7n4j-D40"