from src.core.policy_validator.validator_base import OllamaValidatorBase
# Prompt Injection prompts
prompt_specific_instructions = """Review the data provided by the user and check that they are not sharing secrets, passwords, or tokens."""

class SecretsValidatorService(OllamaValidatorBase):
    def __init__(self, model_name: str):
        super().__init__(model_name=model_name, prompt_specific_instructions=prompt_specific_instructions)