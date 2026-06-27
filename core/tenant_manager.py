import os
import requests
import logging
from core.config import config

logger = logging.getLogger(__name__)

class TenantContext:
    """
    Holds all data and configurations related to a specific tenant.
    """
    def __init__(self, tenant_id: str, config_data: dict):
        self.tenant_id = tenant_id
        self.config = config_data

class TenantManager:
    """
    Loads tenant configuration dynamically from Supabase.
    """
    def __init__(self):
        self.base_url = config.SUPABASE_URL
        self.headers = {
            "apikey": config.SUPABASE_API_KEY,
            "Authorization": f"Bearer {config.SUPABASE_API_KEY}",
            "Content-Type": "application/json"
        }

    def load_tenant(self, tenant_id: str) -> TenantContext:
        # Fetch the config directly from Supabase (bypassing the local file system)
        # Adjust 'tenant_configs' to whatever your actual table name is
        url = f"{self.base_url}/rest/v1/tenant_configs?tenant_id=eq.{tenant_id}&select=*"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                raise ValueError(f"No configuration found in Supabase for tenant: {tenant_id}")
                
            tenant_config = data[0] # Assuming the query returns a list with one match
            
            if not tenant_config.get("system_prompt"):
                raise RuntimeError("Invalid tenant config: missing system_prompt")

            if not tenant_config.get("organization_id"):
                raise RuntimeError("Invalid tenant config: missing organization_id")

            logger.info(
                f"Tenant '{tenant_id}' loaded from Supabase "
                f"(organization_id={tenant_config.get('organization_id')})"
            )

            return TenantContext(tenant_id=tenant_id, config_data=tenant_config)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch tenant config from Supabase: {str(e)}")
            raise

tenant_manager = TenantManager()




# from vectorstores.supabase_store import supa_base_vector_db
# from core.constants import (TENANT_CONFIG_FILE,
#                             TENANT_PROMPT_DIR,
#                             TENANT_DOCS_DIR,
#                             TENANT_BITS_DIR,
#                             PROJECT_ROOT,
#                             )
# import os
# import json
# import logging

# logger = logging.getLogger(__name__)

# class TenantContext:
#     """
#     Holds all data and configurations related to a specific tenant.
#     """

#     def __init__(self, tenant_id, config:dict):
#         self.tenant_id = tenant_id
#         # self.base_path = base_path
#         self.config = config
#         # self.prompts_path = os.path.join(base_path, TENANT_PROMPT_DIR)
#         # self.docs_path = os.path.join(base_path, TENANT_DOCS_DIR)
#         # self.bits_path = os.path.join(base_path, TENANT_BITS_DIR)


# class TenantManager:

#     """
#     Loads tenant configuration from local JSON files.
#     """

#     def __init__(self, config_root:str | None = None):
#         self.config_root = config_root or os.path.join(PROJECT_ROOT, "vectorstores")

#         if not os.path.exists(self.config_root):
#             raise ValueError(f"Tenant config root path does not exist: {self.config_root}")
    
#     def get_config_path(self, tenant_id:str) -> str:
#         return os.path.join(self.config_root, f"{tenant_id}.json")

#     def load_tenant(self, tenant_id: str) -> TenantContext:
#         config_path = self.get_config_path(tenant_id)

#         if not os.path.exists(config_path):
#             raise FileNotFoundError(f"Missing tenant config file: {config_path}")

#         with open(config_path, "r") as f:
#             config = json.load(f)

#         if not config.get("system_prompt"):
#             raise RuntimeError("Invalid tenant config: missing system_prompt")

#         if not config.get("organization_id"):
#             raise RuntimeError("Invalid tenant config: missing organization_id")

#         logger.info(
#             f"Tenant '{tenant_id}' loaded from local config "
#             f"(organization_id={config.get('organization_id')})"
#         )

#         return TenantContext(tenant_id=tenant_id, config=config)
# tenant_manager = TenantManager()
