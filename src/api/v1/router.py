from fastapi import APIRouter
from src.api.v1.endpoints import policy_validation, policy, whitelisted_resources

api_router = APIRouter()
api_router.include_router(policy_validation.router, prefix="/policy/validation", tags=["policy", "validation"])
api_router.include_router(policy.router, prefix="/policy", tags=["policy"])
api_router.include_router(whitelisted_resources.router, prefix="/whitelist", tags=["whitelist"])