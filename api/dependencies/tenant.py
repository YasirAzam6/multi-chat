from fastapi import Header, HTTPException
from core.tenant_manager import tenant_manager, TenantContext

async def get_tenant( 
    x_tenant_id: str | None = Header(
        default=None,
        alias="X-Tenant-ID",
        description="Tenant identifier (e.g., tenant_1)",
    ),
) -> TenantContext:
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="Missing X-Tenant-ID header")
    try:
        return tenant_manager.load_tenant(tenant_id=x_tenant_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
