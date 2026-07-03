from typing import Dict, List

from fastapi import APIRouter, status

from src.config import settings
from src.repository.policy_repository import PolicyRepository

router = APIRouter()

policy_repository = PolicyRepository()
policy_repository.bulk_add_policies(path=settings.PATH_POLICY_REPOSITORY)

# TODO: buena idea manejar policies con id
@router.get("/origin/{origin_id}", response_model=List[str], status_code=status.HTTP_200_OK)
async def get_policies(origin_id: str):
    return policy_repository.get_policies(origin_id)


@router.get("/origin/{origin_id}/safety_review", response_model=List[Dict[str, str]], status_code=status.HTTP_200_OK)
async def get_safety_review(origin_id: str):
    # TODO hacer el review de seguridad de la policy, por ahora solo devuelve un arreglo vacío
    return [] 
