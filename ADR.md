
- Voy a crear una API REST usando FastAPI porque es conocido. Sin embargo para un componente de verificación puede ser lento debido al procesamiento del request. Mas adelante puede migrarse a algo mas rápido como gRPC.

- Se prueba crear una estructura de datos para la creación de policy pero se pierde expresividad a costa de un incremento en la complejidad. Se prefiere usar definición de politicas usando un str plano.

- Para mantener el principio de responsabilidad única y tener un mejor desacople entre los componentes. Se va a usar un patrón scatter & gather con los diferentes componentes (validación de PII, validación de inbound, etc), tambien una arquitectura basada en capas simple para evaluar la entrada y la salida de LLM con el fin de tener un comportamiento lo mas cercano a algo determista; recordemos que estamos usando LLM que son estocasticos por naturaleza.

- En la fase de pruebas y deporación se encontró errores asociados a la implementación ingenua del functor Either. Luego de una revisión rápida de alternativas, se escoge la dependencia `returns` por su buen nivel de integración con `asyncio`.