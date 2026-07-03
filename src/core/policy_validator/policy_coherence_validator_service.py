from src.core.policy_validator.validator_base import OllamaValidatorBase

# Coherence prompts
prompt_specific_instructions = """Analyze the following policy context and determine whether the policy is consistent or not.
If the policy is inconsistent, the decision should be BLOCK, and the justification should explain what inconsistency was found.
If the policy is consistent, the decision should be ALLOW, and the justification should explain why it is considered consistent."""

class CoherenceValidatorService(OllamaValidatorBase):
    def __init__(self, model_name: str):
        super().__init__(model_name=model_name, prompt_specific_instructions=prompt_specific_instructions)