
from src.core.policy_validator.validator_base import (
    OllamaValidatorBase
)


# prompts
prompt_specific_instructions = """Analiza la siguiente policy context y determina si el origen tiene acceso a los
recursos en la whitelist
. """

# TODO: hacer llamado a la API para ver si tiene acceso a los recursos en la whitelist

class WhitelistedPolicyValidatorService(OllamaValidatorBase):
    def __init__(self, model_name: str, whitelisted_resources_repo):
        super().__init__(model_name=model_name, prompt_specific_instructions=prompt_specific_instructions)
        self.whitelisted_resources_repo = whitelisted_resources_repo

    def validate(self, policy_context):
        return super().validate(policy_context)
