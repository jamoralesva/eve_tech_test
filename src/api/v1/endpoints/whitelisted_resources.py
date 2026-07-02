from typing import List

from fastapi import APIRouter, status

from src.config import settings
from src.repository.whitelisted_resources_repository import WhitelistedResourcesRepository

router = APIRouter()

whitelisted_repository = WhitelistedResourcesRepository()
whitelisted_repository.bulk_whitelisted_resources(path=settings.PATH_WHITELISTED_REPOSITORY)

@router.get("/origin/{origin_id}", response_model=List[str], status_code=status.HTTP_200_OK)
async def get_policies(origin_id: str):
    return whitelisted_repository.get_whitelisted_resources(origin_id)

