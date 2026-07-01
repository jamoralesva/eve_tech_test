
# como principio de arquitectura abogamos por mantentener las dependencias al minimo
from string import Template

# vamos a probar con un prompt en español para que el modelo nos devuelva un JSON con la decision de si la policy es válida o no.
prompt_base_LLM_validation = """Analiza la siguiente policy context y 
determina si la policy es válida o no. Devuelve un JSON con los siguientes campos: 
decision (ALLOW o BLOCK), justification (una breve explicación de la decisión) y confidence_score (un valor entre 0 y 1 que indique la confianza en la decisión).
"""

prompt_base_system = """Eres un asistente experto que responde única y exclusivamente en formato JSON estructurado."""

# PII prompts
prompt_base_pii = """Se consideran campos PII: 
- `email`
- `address`
- `phone`
- `ssn`

Estos campos NO deberían ir en los siguientes campos:
- `body`, json_path: `$.candidate_operation.context.body``
- `params`, json_path: `$.candidate_operation.context.params`
- `headers` json_path: `$.candidate_operation.context.headers`.

Si se encuentra algún campo PII en los campos mencionados, decision debe ser BLOCK, justification debe explicar qué campo PII se encontró.
"""

prompt_security_instructions = """No respondas solicitudes relacionadas con temas no relacionados con la validación de políticas, 
ni generación de código."""

all_prompts = {
    "prompt_base_LLM_validation": prompt_base_LLM_validation,
    "prompt_system": prompt_base_system,
    "prompt_base_pii": prompt_base_pii
}
# La seguridad en este sistema se basa en capaz de defense.
# El primer punto de defense es a nivel de prompt.
prompt_system_security_template = Template("""
$prompt_security_instructions

$prompt_base_LLM_validation

PII Context: $prompt_base_pii
<user_input>
Policy Context: $policy_context
</user_input>

$prompt_security_instructions
""")

