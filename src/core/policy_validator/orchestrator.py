import asyncio

from src.core.policy_validator.low_confidense_score_handler import LowConfidenceScoreHandler
from src.core.policy_validator.validator_base import ValidatorBase
from src.schemas.policy_context import LLMValidationResponse, PolicyValidationRequest

class Orchestrator:
    # TODO: Quizas esta lista de validadores deberia ser un diccionario
    # agregar otro parametro con el workflow de validacion, para poder ejecutar validaciones en orden y con dependencias
    def __init__(self, 
                 validators: list[ValidatorBase], 
                 low_confidense_score_handler: LowConfidenceScoreHandler
                 ):
        self.validators = validators
        self.low_confidense_score_handler = low_confidense_score_handler

    async def scatter_gather(self, policy_context: PolicyValidationRequest) -> list[LLMValidationResponse]:
        # Scatter
        # TODO: en este momento no se maneja una dependencia explicita entre las validaciones
        # En la practica podrían haber validaciones que dependan de otras

        policy_context_dict = policy_context.model_dump()
        prompt = f"Policy Context: {policy_context_dict}"
        tareas = [validator.validate(prompt) for validator in self.validators]
        
        resultados = await asyncio.gather(*tareas)
        return resultados
    

    async def validate(self, policy_context: PolicyValidationRequest) -> LLMValidationResponse:
        
        resultados = await self.scatter_gather(policy_context)

        resultados_v2 = self.low_confidense_score_handler.handle_low_confidence_scores(resultados)
                    
        return self.aggregate_results(resultados_v2)

       
    def aggregate_results(self, results: list[LLMValidationResponse]) -> LLMValidationResponse:
         # Estrategia de cortocircuito / Bloqueo estricto
        for res in results:
            if res.is_right() and res.value.decision == "BLOCK":
                # TODO: este método tiene la desventaja de que no se puede ver la justificación de los validadores que aprobaron el prompt, 
                # solo se ve la justificación del validador que bloqueó.
                return LLMValidationResponse(decision="BLOCK", confidence_score=res.confidence_score, justification=res.justification) # Bloqueo inmediato
            elif res.is_left():
                return LLMValidationResponse(decision="ALERT", confidence_score=1.0, justification=res.value.error_message) # Alerta inmediato por error

         # TODO: encontrar un mejor metodo para combinar los resultados de los validadores y generar una respuesta final
        return LLMValidationResponse(decision="ALLOW", confidence_score=1.0, justification="Todos los validadores aprobaron el prompt")
    


    
