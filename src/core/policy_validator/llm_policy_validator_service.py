import ollama

from src.core.policy_validator.validator_base import (
    ValidatorBase, 
    PartialValidation, 
    common_prompts, 
    prompt_system_security_template, 
)


# prompts
prompt_specific_instructions = """Analiza la siguiente policy context y determina si la policy es válida o no. """

class LLMPolicyValidatorService(ValidatorBase):
    def __init__(self, model_name: str):
        self.model_name = model_name

    async def validate(self, policy_context: str) -> PartialValidation:
        prompt = prompt_system_security_template.substitute(
            {
                "policy_context": policy_context,
                "prompt_specific_instructions": prompt_specific_instructions,
                **common_prompts
            })
        # Llamar al modelo LLM usando Ollama
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "system", 
                    "content": prompt
                }
            ],
            format=PartialValidation.model_json_schema(),
        )
        # TODO: Manejar errores y excepciones de la llamada al modelo LLM
        # revisar la salidad del modelo y revisar que sea un JSON válido con los campos esperados

        # Procesar la respuesta del modelo y devolverla como un diccionario
        return PartialValidation.model_validate_json(response['message']['content'])