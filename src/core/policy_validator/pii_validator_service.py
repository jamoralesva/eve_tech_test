from src.core.policy_validator.validator_base import OllamaValidatorBase


# PII prompts
prompt_specific_instructions = """Specifically, you are an automated validator of PII fields in JSON payloads for Agents.
If any PII field is found, the decision should be BLOCK. The justification field should explain which PII field was found.
"""""

# TODO: agregar validación de PII usando regex o librerías especializadas, en lugar de solo simular la validación

class PIIValidatorService(OllamaValidatorBase):
    def __init__(self, model_name: str):
        super().__init__(model_name=model_name, prompt_specific_instructions=prompt_specific_instructions)