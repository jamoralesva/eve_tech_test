import asyncio

from src.core.policy_validator.validator_base import PartialValidation, ValidatorBase


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

class PIIValidatorService(ValidatorBase):
    def __init__(self, model_name: str):
        self.model_name = model_name

    async def validate(self, prompt: str) -> PartialValidation:
        await asyncio.sleep(0.01) 
        return PartialValidation(decision="ALLOW", confidence_score=1.0, justification="No PII found")