# Implementación de un componente de verificación de Policies basado en LLM

## Introducción

TODO

Este proyecto tiene un histórico en git, donde puede ver la evolución de la solución.

`git log`

## Estructura del proyecto

```
EVE_TECH_TEST/
├── pyproject.toml
├── README.md               # este documento
├── ADR.md                  # Aquí iré poniendo en forma de log dudas y decisiones tomadas.
├── .env                    # Variables de entorno (no commitear)
└── src/
    ├── __init__.py
    ├── main.py             # Punto de entrada de la aplicación ASGI (Uvicorn)
    ├── config.py           # Gestión de configuraciones con Pydantic Settings
    ├── api/                # Capa de transporte (HTTP/REST)
    │   ├── __init__.py
    │   ├── v1/
    │   │   ├── __init__.py
    │   │   ├── router.py   # Agregador de rutas de la versión 1
    │   │   └── endpoints/  # Controladores por recurso (e.g., usuarios, productos)
    │   └── dependencies.py # Dependencias globales de FastAPI (Inyección de Dependencias)
    ├── core/               # Lógica de negocio pura (Servicios / Casos de uso)
    ├── schemas/            # Modelos de validación de datos (Pydantic)
    └── repository/         # Capa de persistencia (SQLAlchemy, Motor, etc.)
```

## Instalación

Versión de Poetry usada: `Poetry (version 2.3.2)`

`poetry env activate`
`poetry install`

- Instalar [Ollama](https://ollama.com/):

- Descargar llama3.2: `ollama pull llama3.2:3b`
- Ejecutar Ollama en background: `ollama serve > /dev/null 2>&1 &`

## Ejecución

`poetry run uvicorn src.main:app --reload`


## Documentación Arquitectura P1

TODO

## Arquitectura P2

### Invocación desde el componente principal (EVE Guard)
TODO

### Uso origin → policy mapping 
TODO

### Construcción de Prompts
TODO



- how it differentiates between request verification and response verification
how you conceptually distinguish between ALLOW, ALERT, and BLOCK


## Consumo de la API

### Casos de Prueba

1. A benign operation → ALLOW:

- Request:
```sh
curl -L -X POST http://127.0.0.1:8000/api/v1/policy/validation/ \
  -H "Content-Type: application/json" \
  -d '{
    "origin_id": "agent-001",
    "policy": ["This origin must not return PII"],
    "candidate_operation": {
      "kind": "inbound_response",
      "origin_id": "agent-001",
      "context": {
        "body": {
          "address": "Cra 8 # 13-48",
          "phone": "+573176455555"
        }
      }
    }
  }'
```

- Response:
```json
{
  "origin_id": "agent-001",
  "policy": ["This origin must not return PII"],
  "candidate_operation": {
    "kind": "inbound_response",
    "origin_id": "agent-001",
    "context": {
      "body": {
        "address": "Cra 8 # 13-48",
        "phone": "+573176455555"
      }
    }
  },
  "validation_id": 1,
  "decision": "BLOCK",
  "justification": "contains PII data",
  "confidence_score": 1.0
}
```
2. A response containing PII → BLOCK
TODO

3. A request to a non-whitelisted API → BLOCK
TODO

4. An ambiguous or borderline case → ALERT
TODO

5. A malformed or contradictory policy → ALERT
TODO

6. An adversarial case (e.g., obfuscated sensitive data) → ALERT
TODO

7. Get Policies
- Request:
```sh
curl -L -X GET http://127.0.0.1:8000/api/v1/policy/origin/agent_001 
```

- Response:
```json
[
  "allow: origin_001",
  "block: origin_002"
]
```

8. Get Policies Safety Review
- Request:
```sh
curl -L -X GET http://127.0.0.1:8000/api/v1/policy/origin/agent_001/safety_review
```

- Response:
TODO
```json
[]
```

9. Health:

```sh
curl http://127.0.0.1:8000/health
```




TODO:

log and audit decisions at the origin level
add non-LLM hard checks for known-bad patterns 
