
from string import Template
from src.core.policy_validator.either import Either
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
        
    def change_to_alert(self, 
            partial_validation_result: PartialValidation
            ) -> Either[FailedValidation, PartialValidation]:
        return Either.is_right(
                PartialValidation(
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
            )

    def handle(
            self, 
            validation_result: Either[FailedValidation, PartialValidation]
        ) -> Either[FailedValidation, PartialValidation]:
        if validation_result.is_right():
            # Regla:
            v = validation_result.value
            if (v.decision == "ALLOW" and 
                v.confidence_score < self.threshold_allow):
                # Si la decisión es ALLOW pero el score de confianza es bajo, se considera ALERT
                return self.change_to_alert(validation_result)
            elif (v.decision == "BLOCK" and
                   v.confidence_score < self.threshold_block):
                # Si la decisión es BLOCK pero el score de confianza es muy bajo, se considera ALERT
                return self.change_to_alert(validation_result)
        # propagar sin cambios
        return validation_result
