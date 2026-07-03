import json
from string import Template

from src.core.policy_validator.validator_base import OllamaValidatorBase, prompt_standard_output
from src.schemas.policy_context import PolicyContextBase
# Prompt Injection prompts
prompt_specific_instructions = Template(
    """
Specifically, act as a strict automated, review the data provided by the user and check that they are not sharing secrets, passwords, or tokens.
### Decision Workflow (Strict): ###
- If the "policy" array does NOT contain the word "PII" or "Secrets" -> You must return "ALLOW".

$prompt_standard_output

### JSON to Evaluate ###
$fields_to_check

Output JSON:
"""
)

class SecretsValidatorService(OllamaValidatorBase):
    def __init__(self, model_name: str):
        super().__init__(model_name=model_name)

    def build_specific_prompt(self, policy_context: PolicyContextBase):
        # des-anidamos los campos para evaluar
        fields_to_check = {
            "policy": policy_context.policy,
            **(policy_context.candidate_operation.context.body or {}),
            **(policy_context.candidate_operation.context.headers or {}),
            **(policy_context.candidate_operation.context.params or {})
        }

        return prompt_specific_instructions.substitute({
            "prompt_standard_output": prompt_standard_output,
            "fields_to_check": json.dumps(fields_to_check)
        })