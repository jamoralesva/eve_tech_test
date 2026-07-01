import asyncio

from src.core.policy_validator.validator_base import PartialValidation, ValidatorBase


# Coherence prompts
prompt_specific_instructions = """TODO"""

class CoherenceValidatorService(ValidatorBase):
    def __init__(self, model_name: str):
        self.model_name = model_name

    async def validate(self, prompt: str) -> PartialValidation:
        await asyncio.sleep(0.01) 
        return PartialValidation(decision="ALLOW", confidence_score=1.0, justification="Prompt is coherent")