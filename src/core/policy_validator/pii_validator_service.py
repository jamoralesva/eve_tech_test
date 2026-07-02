from src.core.policy_validator.validator_base import OllamaValidatorBase


# PII prompts
prompt_specific_instructions = """Se consideran campos PII: 
- `email`
- `address`
- `phone`
- `ssn`

Estos campos NO deberían ir en los siguientes campos:
- `body`, json_path: `$.candidate_operation.context.body``
- `params`, json_path: `$.candidate_operation.context.params`
- `headers` json_path: `$.candidate_operation.context.headers`.

Si se encuentra algún campo PII en los campos mencionados, decision debe ser BLOCK, justification debe explicar qué campo PII se encontró.
"""

# TODO: agregar validación de PII usando regex o librerías especializadas, en lugar de solo simular la validación

class PIIValidatorService(OllamaValidatorBase):
    def __init__(self, model_name: str):
        super().__init__(model_name=model_name, prompt_specific_instructions=prompt_specific_instructions)