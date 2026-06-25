from typing import Literal

from pydantic import BaseModel, Field

class CandidateOperation(BaseModel):
    kind: Literal["outbound_request", "inbound_response"] | None = Field(
        None,
        description="Tipo de operación (outbound request, inbound response)"
    )
    operation: str = Field(..., min_length=1, description="Identificador de la operación")


class PolicyContextBase(BaseModel):
    origin_id: str = Field(..., min_length=3, max_length=50, description="Origen. El agente/app/tool que requiere hacer la operación")
    # TODO: prefiero usar un modelo para la definición de la politica, pero por simplicidad lo mantendré así.
    policy: str | None = Field(None, description="Definición de la policy en lenguaje natural estructurado")
    candidate_operation: CandidateOperation

class PolicyValidationRequest(PolicyContextBase):
    pass

class PolicyValidationResponse(PolicyContextBase):
    validation_id: int
    decision: Literal["ALLOW", "ALERT", "BLOCK"] | None = Field(
        None,
        description="Tipo de decisión tomada por el agente"
    )
    justification: str
    confidence_score: float = Field(..., ge=0, le=1)
    model_config = {
        "from_attributes": True # Reemplaza el antiguo 'orm_mode = True' en Pydantic v2
    }