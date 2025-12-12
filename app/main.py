from fastapi import FastAPI

from app.routers import router

app = FastAPI(title="Organization Management Service", version="1.0.0")


@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok"}


# ✅ ADD THIS ROUTE
@app.get("/", tags=["system"])
async def root():
    return {"message": "Organization Management Service is running!"}


app.include_router(router)
