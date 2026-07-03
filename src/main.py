from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from src.config import settings
from src.api.v1.router import api_router

# 1. Definimos el gestor del ciclo de vida (Lifespan)
@asynccontextmanager
async def lifespan(app: FastAPI):
    loggers_a_modificar = ("uvicorn", "uvicorn.access", "uvicorn.error")
    for logger_name in loggers_a_modificar:
        uvicorn_logger = logging.getLogger(logger_name)
        # Asignamos los handlers globales configurados previamente
        uvicorn_logger.handlers = logging.getLogger().handlers
        
    logging.getLogger("mi_aplicacion").info("Logs estructurados acoplados a Uvicorn con éxito.")
    
    yield 
    
    logging.getLogger("mi_aplicacion").info("Cerrando recursos de la aplicación...")


app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}