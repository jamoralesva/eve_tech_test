import ollama
from ..schemas.policy_context import LLMValidationResponse, PolicyContextBase
from .prompts.base import prompt_base_LLM_validation, prompt_system, prompt_base_pii

class LLMPolicyValidatorService:
    def __init__(self, model_name: str = "llama2"):
        self.model_name = model_name

    def validate_policy(self, policy_context: PolicyContextBase) -> LLMValidationResponse:
        # Construir el prompt con el contexto de la política
        # TODO: Quizas sea buena idea dividir la validación en pequeños expertos. Ej: uno para PII, otro para validación de reglas, etc. y luego combinar las respuestas.
        prompt = f"{prompt_base_LLM_validation}\n\nPolicy Context: {policy_context}\n\nPII Context: {prompt_base_pii}"

        # Llamar al modelo LLM usando Ollama
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "system", 
                    "content": prompt_system
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            format=LLMValidationResponse.model_json_schema(),
        )
        # TODO: Manejar errores y excepciones de la llamada al modelo LLM
        # revisar la salidad del modelo y revisar que sea un JSON válido con los campos esperados

        # Procesar la respuesta del modelo y devolverla como un diccionario
        return LLMValidationResponse.model_validate_json(response['message']['content'])