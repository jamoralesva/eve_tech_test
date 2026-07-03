
from src.core.policy_validator.validator_base import (
    OllamaValidatorBase
)


# prompts
prompt_specific_instructions = """Analyze the following policy context and determine whether the policy is valid or not."""

class LLMPolicyValidatorService(OllamaValidatorBase):
    def __init__(self, model_name: str):
        super().__init__(model_name=model_name, prompt_specific_instructions=prompt_specific_instructions)
