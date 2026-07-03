import json
from string import Template

from src.core.policy_validator.validator_base import OllamaValidatorBase, prompt_standard_output
from src.schemas.policy_context import PolicyContextBase

# Coherence prompts
prompt_specific_instructions = Template(
"""Specifically, analyze the following policies and determine whether the policy set is consistent or not.
If the policy is inconsistent, the decision should be ALERT, and the justification should explain what inconsistency was found.
If the policy is consistent, the decision should be ALLOW, and the justification should explain why it is considered consistent.

$prompt_standard_output

### JSON to Evaluate ###
$fields_to_check

Output JSON:

""")

class CoherenceValidatorService(OllamaValidatorBase):
    def __init__(self, model_name: str):
        super().__init__(model_name=model_name)

    def build_specific_prompt(self, policy_context: PolicyContextBase):
        # des-anidamos los campos para evaluar
        fields_to_check = {
            "policy": policy_context.policy,
        }

        return prompt_specific_instructions.substitute({
            "prompt_standard_output": prompt_standard_output,
            "fields_to_check": json.dumps(fields_to_check)
        })