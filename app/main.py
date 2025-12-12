from fastapi import FastAPI
from app.routers import router

app = FastAPI(
    title="Organization Management Service",
    version="1.0.0"
)

@app.get("/", tags=["system"])
async def root():
    return {
        "message": "Organization Management Backend is Running!",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok"}

app.include_router(router)
