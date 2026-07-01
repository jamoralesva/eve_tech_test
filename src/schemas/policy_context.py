from typing import List, Literal

from pydantic import BaseModel, Field

# Intentamos ser agnosticos a REST o MCP
class OperationContext(BaseModel):
    uri: str | None = Field(None, description="URI del recurso, si este tiene asociada una URI")
    params: dict | None = Field(None, description="Diccionario de parametros")
    body:  dict | None = Field(None, description="Diccionario con un body (request/response)")
    headers: dict | None = Field(None, description="Diccionario con headers. Acoplado al protocolo REST")

class CandidateOperation(BaseModel):
    kind: Literal["outbound_request", "inbound_response"] | None = Field(
        None,
        description="Tipo de operación (outbound request, inbound response)"
    )
    origin_id: str | None = Field(None, min_length=3, max_length=50, description="Origen que requiere hacer la operación")
    resource_id: str | None = Field(None, min_length=3, max_length=50, description="Recurso sobre el cual se quiere hacer la operación")
    context: OperationContext | None = Field(None, description="Contexto de la operación, si es un request o response")


class PolicyContextBase(BaseModel):
    origin_id: str = Field(..., min_length=3, max_length=50, description="Origen. El agente/app/tool que requiere hacer la operación")
    policy: List[str] | None = Field(None, description="Definición de la policy estructurado")
    candidate_operation: CandidateOperation = Field(..., description="Contexto de la operación candidata")

class PolicyValidationRequest(PolicyContextBase):
    pass

class LLMValidationResponse(BaseModel):
    decision: Literal["ALLOW", "ALERT", "BLOCK"] | None = Field(
        None,
        description="Tipo de decisión tomada por el agente"
    )
    justification: str = Field(..., min_length=3, max_length=500, description="Justificación de la decisión tomada por el agente")
    confidence_score: float = Field(..., ge=0, le=1)

class PolicyValidationResponse(PolicyContextBase):
    validation_id: str = Field(..., min_length=1, max_length=50, description="Id de la ejecución de la validación")
    llm_validation_response: LLMValidationResponse = Field(..., description="Respuesta del LLM con la decisión de la validación de la policy")
    model_config = {
        "from_attributes": True # Reemplaza el antiguo 'orm_mode = True' en Pydantic v2
    }