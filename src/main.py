from fastapi import FastAPI
from src.config import settings
from src.api.v1.router import api_router

app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}