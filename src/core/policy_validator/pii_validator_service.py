import json
from string import Template

from src.core.policy_validator.validator_base import OllamaValidatorBase, prompt_standard_output
from src.schemas.policy_context import PolicyContextBase


# PII prompts
prompt_specific_instructions = Template("""Specifically, act as a strict automated PII (Personally Identifiable Information) validator for JSON payloads. Your single task is to scan the entire input JSON for any human personal data fields.
### Decision Workflow (Strict): ###
- If the "policy" array does NOT contain the word "PII" -> You must return "ALLOW".
                                        
### PII Classification Criteria (Strict): ###
You must classify the following fields or concepts as PII:
- "address": Any physical, postal, residential, or geographic location data of a person.
- "email" or "email_address": Any electronic mail format string (user@gmail.com).
- "phone", "phone_number", "telephone": Treat as PII ONLY if the field represents a human telephone number.
- "name", "fullname", "surname": Any human identifying name.
  
### CRITICAL NEGATIVE CONSTRAINTS (Anti-Hallucination Rules): ###
1. DO NOT classify technical identifiers, database keys, auto-incrementing IDs, timestamps, or system tracking numbers as phone numbers, even if they contain only digits.
2. A random string of digits (like "1234567890" or "20260702") inside generic fields like "id", "origin_id", "reference", "timestamp", or "uuid" is NOT PII.
3. If a number belongs to a technical configuration parameter (e.g., "retry_count": 3, "port": 8080, "amount": 1500), it is NOT PII.

### Example False Positive Prevention Case: ###
Input: {"origin_id": "agent-9988112233", "context": {"transaction_id": 4567112233, "status": "active"}}
Output: {"decision": "ALLOW", "justification": ""}

### Decision Rules: ###
1. If ANY of the PII concepts listed above are present in the JSON keys or values (even if nested), the "decision" MUST be "BLOCK".
2. If a field is BLOCKED, the "justification" MUST explicitly name the offending field.
3. If NO human PII fields are found, the "decision" MUST be "ALLOW" .

$prompt_standard_output

### JSON to Evaluate ###
$fields_to_check

Output JSON:
""")

# TODO: agregar validación de PII usando regex o librerías especializadas, en lugar de solo simular la validación

class PIIValidatorService(OllamaValidatorBase):
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
            "fields_to_check": json.dumps(fields_to_check),
            "prompt_standard_output": prompt_standard_output
        })
