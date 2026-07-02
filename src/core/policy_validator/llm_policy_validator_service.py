
from src.core.policy_validator.validator_base import (
    OllamaValidatorBase
)


# prompts
prompt_specific_instructions = """Analiza la siguiente policy context y determina si la policy es válida o no. """

class LLMPolicyValidatorService(OllamaValidatorBase):
    def __init__(self, model_name: str):
        super().__init__(model_name=model_name, prompt_specific_instructions=prompt_specific_instructions)
    