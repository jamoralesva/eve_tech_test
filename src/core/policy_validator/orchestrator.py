import asyncio
from typing import List
from returns.methods import partition
from returns.unsafe import unsafe_perform_io

from returns.future import FutureResult
from returns.io import IOResult

from src.core.policy_validator.low_confidense_score_handler import LowConfidenceScoreHandler
from src.core.policy_validator.validator_base import FailedValidation, PartialValidation, ValidatorBase
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


    async def validate(self, policy_context: PolicyValidationRequest) -> LLMValidationResponse:
        
        # Scatter
        # TODO: en este momento no se maneja una dependencia explicita entre las validaciones
        # En la practica podrían haber validaciones que dependan de otras

        futures: list[FutureResult[PartialValidation, FailedValidation]] = [
            v.validate(policy_context)
             .bind(self.low_confidense_score_handler.handle)
            for v in self.validators
        ]

        resultados = await asyncio.gather(*futures)

        return self.combinar_resultados(resultados)

    def combinar_resultados(
        self,
        resultados: List[IOResult[PartialValidation, FailedValidation]]
    ) -> LLMValidationResponse:

        exitos_io, fallos_io = partition(resultados)
        exitos: List[PartialValidation] = [unsafe_perform_io(io) for io in exitos_io]
        fallos: List[FailedValidation] = [unsafe_perform_io(io) for io in fallos_io]

        match (fallos, exitos):
            case (v_fallidos, _) if v_fallidos:
                justificacion = " | ".join(
                    f"{f.error_message}, validator_id: {f.validator_id}" for f in v_fallidos
                )
                return LLMValidationResponse(decision="ALERT", confidence_score=1.0, justification=justificacion)
            
            case (_, v_exitosos) if any(v.decision == "ALERT" for v in v_exitosos):
                alertas = [v for v in v_exitosos if v.decision == "ALERT"]
                justificacion = " | ".join(f"{b.justification}, validator_id:{b.validator_id}" for b in alertas)
                return LLMValidationResponse(decision="ALERT", confidence_score=1.0, justification=justificacion)


            case (_, v_exitosos) if any(v.decision == "BLOCK" for v in v_exitosos):
                bloqueos = [v for v in v_exitosos if v.decision == "BLOCK"]
                min_score = min(b.confidence_score for b in bloqueos)
                justificacion = " | ".join(b.justification for b in bloqueos)
                return LLMValidationResponse(decision="BLOCK", confidence_score=min_score, justification=justificacion)

            case (_, v_exitosos):
                avg_score = sum(v.confidence_score for v in v_exitosos) / len(v_exitosos) if v_exitosos else 1.0
                justificacion = " | ".join(v.justification for v in v_exitosos)
                return LLMValidationResponse(decision="ALLOW", confidence_score=avg_score, justification=justificacion)