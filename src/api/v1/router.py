from fastapi import APIRouter
from src.api.v1.endpoints import policy_validation

api_router = APIRouter()
api_router.include_router(policy_validation.router, prefix="/policy/validation", tags=["policy", "validation"])