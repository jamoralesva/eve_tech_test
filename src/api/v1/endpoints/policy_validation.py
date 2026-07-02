from fastapi import APIRouter, status

from src.core.policy_validator.low_confidense_score_handler import LowConfidenceScoreHandler
from src.core.policy_validator.pii_validator_service import PIIValidatorService
from src.core.policy_validator.policy_coherence_validator_service import CoherenceValidatorService
from src.core.policy_validator.prompt_injection_validator_service import PromptInjectionValidatorService
from src.core.policy_validator.secrets_validator_service import SecretsValidatorService
from src.schemas.policy_context import PolicyValidationRequest, PolicyValidationResponse
from src.core.policy_validator.orchestrator import Orchestrator

from src.config import settings

router = APIRouter()

# Simulación de base de datos en memoria para el ejemplo
fake_db = []

# TODO: Crear Factory para instanciar los validadores y el orquestador, inyectando dependencias de manera más limpia
orchestrator = Orchestrator(
    validators=[
        SecretsValidatorService(model_name=settings.MODEL_NAME),
        PIIValidatorService(model_name=settings.MODEL_NAME),
        CoherenceValidatorService(model_name=settings.MODEL_NAME),
        PromptInjectionValidatorService(model_name=settings.MODEL_NAME)
    ],
    low_confidense_score_handler=LowConfidenceScoreHandler(
        threshold_allow=settings.LOW_CONFIDENCE_THRESHOLD_ALLOW,
        threshold_block=settings.LOW_CONFIDENCE_THRESHOLD_BLOCK
    )
)

@router.post("/", response_model=PolicyValidationResponse, status_code=status.HTTP_200_OK)
async def policy_validation(policy_context: PolicyValidationRequest):
    # En un escenario real, aquí se llamaría a la capa 'core' o 'repository'
    llm_response = await orchestrator.validate(policy_context)
    print(f"LLM Response: {llm_response}")  # Para depuración
    response = {**policy_context.model_dump(), "validation_id": str(len(fake_db) + 1), "llm_validation_response": llm_response}
    fake_db.append(response)
    return response
