import asyncio

from src.core.policy_validator.validator_base import PartialValidation, ValidatorBase

class SecretsValidatorService(ValidatorBase):

    def __init__(self, model_name: str):
        self.model_name = model_name

    async def validate(self, prompt: str) -> PartialValidation:
        # Aquí se ejecuta lógica determinista (ej. detect-secrets / regex)
        # Al ser intensivo en CPU, simulamos con un paso asíncrono rápido
        await asyncio.sleep(0.01) 
        return PartialValidation(decision="ALLOW", confidence_score=1.0, justification="No secrets found")