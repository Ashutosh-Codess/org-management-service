from fastapi import FastAPI
from app.routers.org_routes import router as org_router
from app.routers.org_create import router as create_router
from app.routers.admin_auth import router as admin_router

app = FastAPI(
    title="Org Management Service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(org_router)
app.include_router(create_router)
app.include_router(admin_router)
