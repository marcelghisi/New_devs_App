from decimal import Decimal, ROUND_HALF_UP

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from app.services.cache import get_revenue_summary
from app.core.auth import authenticate_request as get_current_user
from app.constants import MONETARY_DECIMAL_PLACES

router = APIRouter()

def _format_monetary(value: str) -> str:
    """Quantize a numeric string to MONETARY_DECIMAL_PLACES decimals."""
    quantizer = Decimal(10) ** -MONETARY_DECIMAL_PLACES  # e.g. Decimal('0.001')
    return str(Decimal(value).quantize(quantizer, rounding=ROUND_HALF_UP))

@router.get("/dashboard/summary")
async def get_dashboard_summary(
    property_id: str,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:

    tenant_id = current_user.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=403, detail="No tenant context for user")

    revenue_data = await get_revenue_summary(property_id, tenant_id)

    return {
        "property_id": revenue_data['property_id'],
        "total_revenue": _format_monetary(revenue_data['total']),
        "currency": revenue_data['currency'],
        "reservations_count": revenue_data['count']
    }
