from fastapi import APIRouter, status
from src.schemas.policy_context import PolicyValidationRequest, PolicyValidationResponse
from src.core.llm_policy_validator_service import LLMPolicyValidatorService
from src.config import settings

router = APIRouter()

# Simulación de base de datos en memoria para el ejemplo
fake_db = []
llm_validator = LLMPolicyValidatorService(settings.MODEL_NAME)

@router.post("/", response_model=PolicyValidationResponse, status_code=status.HTTP_200_OK)
async def policy_validation(policy_context: PolicyValidationRequest):
    # En un escenario real, aquí se llamaría a la capa 'core' o 'repository'
    llm_response = llm_validator.validate_policy(policy_context.model_dump())
    print(f"LLM Response: {llm_response}")  # Para depuración
    response = {**policy_context.model_dump(), "validation_id": str(len(fake_db) + 1), "llm_validation_response": llm_response}
    fake_db.append(response)
    return response
