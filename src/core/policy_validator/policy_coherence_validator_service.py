from src.core.policy_validator.validator_base import OllamaValidatorBase

# Coherence prompts
prompt_specific_instructions = """Analiza la siguiente policy context y determina si la policy es coherente o no.
Si la policy es incoherente, decision debe ser BLOCK, justification debe explicar qué incoherencia se encontró.
Si la policy es coherente, decision debe ser ALLOW, justification debe explicar por qué se considera coherente.
"""

class CoherenceValidatorService(OllamaValidatorBase):
    def __init__(self, model_name: str):
        super().__init__(model_name=model_name, prompt_specific_instructions=prompt_specific_instructions)