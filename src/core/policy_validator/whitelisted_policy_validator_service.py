
import json
from string import Template

from src.core.policy_validator.validator_base import (
    OllamaValidatorBase
)
from src.repository.whitelisted_resources_repository import WhitelistedResourcesRepository
from src.schemas.policy_context import PolicyContextBase


# prompts
prompt_specific_instructions = Template("""Act as a strict, binary policy enforcement gate. Your only job is to return "ALLOW" or "BLOCK" inside the "decision" field.

### Decision Workflow (Strict): ###
- If the "policy" array does NOT contain the word "whitelist" or "allowlist" -> You must return "ALLOW".
- If the "policy" array CONTAINS "whitelist" or "allowlist" AND "resource_id" is NOT in "whitelisted_resources" -> You must return "BLOCK".

### Example 1 (No Whitelist Policy -> ALWAYS ALLOW): ###
Input: {"policy": ["This origin must not return PII"], "resource_id": null, "whitelisted_resources": []}
Output: {"decision": "ALLOW", "justification": "Policy is unrelated to whitelists. Request permitted.", "confidence_score": 1.0}

### Example 2 (Whitelist Policy & Missing Match -> BLOCK): ###
Input: {"policy": ["This origin may only call whitelisted APIs"], "resource_id": "https://key_vault.com", "whitelisted_resources": ["https://api.gateway.local"]}
Output: {"decision": "BLOCK", "justification": "Resource is not present in the required whitelist.", "confidence_score": 1.0}

### JSON to Evaluate ###
$fields_to_check

Output JSON:
""")

# TODO: hacer llamado a la API para ver si tiene acceso a los recursos en la whitelist

class WhitelistedPolicyValidatorService(OllamaValidatorBase):
    def __init__(
            self, 
            model_name: str, 
            whitelisted_resources_repo: WhitelistedResourcesRepository):
        super().__init__(model_name=model_name)
        self.whitelisted_resources_repo = whitelisted_resources_repo

    def build_specific_prompt(self, policy_context: PolicyContextBase) -> str:
        # TODO: este llamado quizas deba ser asincróno y ser llamado por el LLM
        # solo cuando sea necesario para reducir latencias
        whitelisted_resources = self.whitelisted_resources_repo.get_whitelisted_resources(
            origin_id=policy_context.origin_id
        )

        fields_to_check = {
            "policy": policy_context.policy,
            #"kind": policy_context.candidate_operation.kind,
            "origin_id": policy_context.origin_id,
            "resource_id": policy_context.candidate_operation.resource_id,
            "whitelisted_resources": whitelisted_resources
        }

        return prompt_specific_instructions.substitute({
            "fields_to_check": json.dumps(fields_to_check)
        })

    def validate(self, policy_context):
        return super().validate(policy_context)
