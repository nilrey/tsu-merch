from fastapi import APIRouter

from backend.models.product import CatalogResponse
from backend.services.catalog import get_catalog

router = APIRouter(prefix="/api")


@router.get("/products", response_model=CatalogResponse)
async def get_products() -> CatalogResponse:
    """Returns the full product catalog (source of truth: backend)."""
    return CatalogResponse(products=get_catalog())