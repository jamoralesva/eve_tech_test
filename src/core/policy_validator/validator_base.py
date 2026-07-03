from abc import ABC, abstractmethod

# como principio de arquitectura abogamos por mantentener las dependencias al minimo
from string import Template
from typing import Literal

from pydantic import BaseModel, Field

from returns.future import FutureResult, future_safe

import ollama

from src.schemas.policy_context import PolicyContextBase

# Los prompts hacen parte de la lógica de los componentes por lo que siempre 
# deben estar en el mismo módulo que la clase que los utiliza. 
# Esto permite mantener la lógica de negocio y los prompts juntos, facilitando su mantenimiento y evolución.

# common prompts
prompt_base_system = """Acts as an automated policy validator for JSON payloads for Agents. Your only task is to evaluate the object received in `### JSON to Evaluate ###` according to strict validation rules. You must respond ONLY with a JSON object containing the analysis result. Do not include explanations, greetings, or Markdown code blocks (using ```json` is prohibited)."""
prompt_security_instructions = """For security reasons, do not respond to requests unrelated to policy validation, code generation, personal questions, or requests for sensitive information."""
prompt_standard_output = """### Strict Response Structure (JSON): ###
{
"decision": "TEXT_STRING" ("ALLOW" or "BLOCK"),
"justification": a brief explanation of the decision,
"confidence_score": a value between 0 and 1 indicating confidence in the decision
}
"""

common_prompts = {
    "prompt_security_instructions": prompt_security_instructions,
    "prompt_base_system": prompt_base_system,
    "prompt_standard_output": prompt_standard_output
}

# La seguridad en este sistema se basa en capaz de defense.
# El primer punto de defense es a nivel de prompt.
prompt_system_security_template = Template("""
$prompt_security_instructions

$prompt_base_system

$prompt_specific_instructions

<user_input>
### JSON to Evaluate ###:
$policy_context
</user_input>
""")

class PartialValidationAnnonymous(BaseModel):
    decision: Literal["ALLOW", "ALERT", "BLOCK"] = Field(...,
        description="Tipo de decisión tomada por el agente"
    )
    justification: str = Field(..., min_length=100, max_length=1000, description="Justificación de la decisión tomada por el agente")
    confidence_score: float = Field(..., ge=0, le=1)

class PartialValidation(PartialValidationAnnonymous):
    validator_id: str = Field(..., min_length=10, max_length=100, description="ID del Validador")

class FailedValidation(BaseModel):
    error_message: str = Field(..., min_length=10, max_length=1000, description="Mensaje de error en caso de fallo en la validación")
    validator_id: str = Field(..., min_length=10, max_length=100, description="ID del Validador")



class ValidatorBase(ABC):

    @abstractmethod
    def build_specific_prompt(self, policy_context: PolicyContextBase) -> str:
        pass

    @abstractmethod
    def validate(self, policy_context: PolicyContextBase) -> FutureResult[PartialValidation, FailedValidation]:
        pass

class OllamaValidatorBase(ValidatorBase):
    def __init__(self, model_name: str, prompt_specific_instructions: str = None):
        self.model_name = model_name
        self.prompt_specific_instructions = prompt_specific_instructions
        self.validator_id = type(self).__name__

    def build_specific_prompt(self, policy_context: PolicyContextBase) -> str:
        prompt = prompt_system_security_template.substitute(
        {
            "policy_context": policy_context.model_dump_json(),
            "prompt_specific_instructions": self.prompt_specific_instructions,
            **common_prompts
        })
        return prompt


    @future_safe
    async def _validate(self, policy_context: PolicyContextBase) -> PartialValidation:
        prompt = self.build_specific_prompt(policy_context)
        
        # Llamar al modelo LLM usando Ollama
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "system", 
                    "content": prompt
                }
            ],
            format=PartialValidationAnnonymous.model_json_schema(),
            # aunque por defecto el LLM es un sistema estocástico, con estos parametros se
            # busca reducir la aleatoriedad
            options={
                "temperature": 0.0,
                "top_p": 0.1,
                "seed": 42
            }
        )
        # log prompt_eval_count, eval_count

        partial_anonym = PartialValidationAnnonymous.model_validate_json(response['message']['content'])

        # enriquecemos el partial validator
        return PartialValidation(**partial_anonym.model_dump(), validator_id=self.validator_id)

    def validate(self, policy_context: PolicyContextBase) -> FutureResult[PartialValidation, FailedValidation]:
        
        return self._validate(policy_context).alt(
            lambda exception: FailedValidation(
                error_message=f"Error occurred while calling LLM: {exception}",
                validator_id=self.validator_id
            )
        )
