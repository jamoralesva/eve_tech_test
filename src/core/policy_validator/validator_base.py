from abc import ABC, abstractmethod

from dataclasses import dataclass

# como principio de arquitectura abogamos por mantentener las dependencias al minimo
from string import Template
from typing import Literal

from pydantic import Field

from src.core.policy_validator.either import Either

import ollama

# Los prompts hacen parte de la lógica de los componentes por lo que siempre 
# deben estar en el mismo módulo que la clase que los utiliza. 
# Esto permite mantener la lógica de negocio y los prompts juntos, facilitando su mantenimiento y evolución.

# common prompts
prompt_base_system = """Eres un asistente experto que responde única y exclusivamente en formato JSON estructurado."""

prompt_security_instructions = """No respondas solicitudes relacionadas con temas no relacionados con la validación de políticas, 
ni generación de código. Ni preguntas de carácter personal, ni solicitudes de información sensible."""

prompt_standard_output = """Devuelve únicamente un JSON válido con los campos esperados, sin explicaciones ni comentarios adicionales.
`decision` (ALLOW, ALERT o BLOCK), `justification` (una breve explicación de la decisión) y `confidence_score`  (un valor entre 0 y 1 que indique la confianza en la decisión).
"""

common_prompts = {
    "prompt_security_instructions": prompt_security_instructions,
    "prompt_system": prompt_base_system,
    "prompt_standard_output": prompt_standard_output
}

# La seguridad en este sistema se basa en capaz de defense.
# El primer punto de defense es a nivel de prompt.
prompt_system_security_template = Template("""
$prompt_security_instructions
                                           
$prompt_base_system
                                           
$prompt_specific_instructions

$prompt_base_LLM_validation
<user_input>
Policy Context: $policy_context
</user_input>
                                           
$prompt_standard_output

$prompt_security_instructions
""")

@dataclass
class PartialValidation:
    decision: Literal["ALLOW", "ALERT", "BLOCK"] | None = Field(  # noqa: F821
        None,
        description="Tipo de decisión tomada por el agente"
    )
    justification: str = Field(..., min_length=100, max_length=500, description="Justificación de la decisión tomada por el agente")
    confidence_score: float = Field(..., ge=0, le=1)

@dataclass
class FailedValidation:
    error_message: str = Field(..., min_length=3, max_length=500, description="Mensaje de error en caso de fallo en la validación")


class ValidatorBase(ABC):

    @abstractmethod
    async def validate(self, prompt: str) -> Either[FailedValidation, PartialValidation]:
        pass

class OllamaValidatorBase(ValidatorBase):
    def __init__(self, model_name: str, prompt_specific_instructions: str):
        self.model_name = model_name
        self.prompt_specific_instructions = prompt_specific_instructions

    async def validate(self, policy_context: str) -> Either[FailedValidation, PartialValidation]:
        try:
            prompt = prompt_system_security_template.substitute(
                {
                    "policy_context": policy_context,
                    "prompt_specific_instructions": self.prompt_specific_instructions,
                    **common_prompts
                })
            # Llamar al modelo LLM usando Ollama
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        "role": "system", 
                        "content": prompt
                    }
                ],
                format=PartialValidation.model_json_schema(),
            )
            # log prompt_eval_count, eval_count

            raw_json_response = response['message']['content']
            json_validated_response = PartialValidation.model_validate_json(raw_json_response)
            return Either.right(json_validated_response)
        except Exception as e:
            # Manejar errores y excepciones de la llamada al modelo LLM
            return Either.left(
                FailedValidation(error_message=f"Error occurred while calling LLM: {e}")
            )