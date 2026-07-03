
from string import Template

from returns.future import FutureResult
from src.core.policy_validator.validator_base import FailedValidation, PartialValidation

# Este componente maneja los casos en los que el score de confianza de la validación es bajo.
# A vuelo de pajaro creo que los falsos negativos son más peligrosos que los falsos positivos, 
# por lo que se podría considerar bloquear la operación si el score de confianza es bajo.

class LowConfidenceScoreHandler:
    def __init__(self, threshold_allow: float = 0.5, threshold_block: float = 0.2):
        self.threshold_allow = threshold_allow
        self.threshold_block = threshold_block
        self.message = Template("Se cambia la decision automaticamente a 'ALERT'. "+
                                "El score de confianza para la decision '$decision' es bajo ($confidence_score). "+
                                "Se recomienda revisar la policy context y la decisión tomada por el modelo. " +
                                "Justificación original: $justification. " +
                                "Se utilizan los siguientes umbrales de confianza: " +
                                "Threshold $threshold_allow para ALLOW y $threshold_block para BLOCK.")
        
    def _change_to_alert(self, 
            partial_validation_result: PartialValidation
            ) -> PartialValidation:
        return PartialValidation(
                    decision="ALERT",
                    confidence_score=1.0,
                    justification=self.message.substitute(
                        decision=partial_validation_result.decision,
                        confidence_score=partial_validation_result.confidence_score,
                        justification=partial_validation_result.justification,
                        threshold_allow=self.threshold_allow,
                        threshold_block=self.threshold_block
                    )
            )

    def handle(
            self, 
            validation_result: PartialValidation
        ) -> FutureResult[FailedValidation, PartialValidation]:
        
        low_allow = (validation_result.decision == "ALLOW" and 
                     validation_result.confidence_score < self.threshold_allow)
        
        low_block = (validation_result.decision == "BLOCK" and 
                     validation_result.confidence_score < self.threshold_block)

        if low_allow or low_block:
            transformado = self._change_to_alert(validation_result)
            return FutureResult.from_value(transformado)
        
        return FutureResult.from_value(validation_result)