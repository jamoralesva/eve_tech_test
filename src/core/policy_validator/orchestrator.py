import asyncio

from src.core.policy_validator.validator_base import ValidatorBase
from src.schemas.policy_context import LLMValidationResponse, PolicyValidationRequest

class Orchestrator:
    # TODO: Quizas esta lista de validadores deberia ser un diccionario
    # agregar otro parametro con el workflow de validacion, para poder ejecutar validaciones en orden y con dependencias
    def __init__(self, validators: list[ValidatorBase]):
        self.validators = validators

    async def validate(self, policy_context: PolicyValidationRequest) -> LLMValidationResponse:
        # Scatter
        # TODO: en este momento no se maneja una dependencia explicita entre las validaciones
        # En la practica podrían haber validaciones que dependan de otras

        policy_context_dict = policy_context.model_dump()
        prompt = f"Policy Context: {policy_context_dict}"
        tareas = [validator.validate(prompt) for validator in self.validators]
        
        resultados = await asyncio.gather(*tareas)
        
        # Estrategia de cortocircuito / Bloqueo estricto
        for res in resultados:
            if not res.decision == "ALLOW":
                print(f"Alerta de seguridad en {res.validator}: {res.justification}")
                return LLMValidationResponse(decision="BLOCK", confidence_score=res.confidence_score, justification=res.justification) # Bloqueo inmediato
                
        # TODO: encontrar un mejor metodo para combinar los resultados de los validadores y generar una respuesta final
        return LLMValidationResponse(decision="ALLOW", confidence_score=1.0, justification="Todos los validadores aprobaron el prompt")