from fastapi import APIRouter, status
from src.schemas.policy_context import PolicyValidationRequest, PolicyValidationResponse

router = APIRouter()

# Simulación de base de datos en memoria para el ejemplo
fake_db = []

@router.post("/", response_model=PolicyValidationResponse, status_code=status.HTTP_200_OK)
async def policy_validation(policy_context: PolicyValidationRequest):
    # En un escenario real, aquí se llamaría a la capa 'core' o 'repository'
    response = {**policy_context.model_dump(), "validation_id": len(fake_db) + 1, "decision": "ALLOW", "justification": "ok", "confidence_score": 1.0}
    fake_db.append(response)
    return response
