from fastapi import FastAPI
from app.routers.org_routes import router as org_router
from app.routers.org_create import router as create_router
from app.routers.admin_auth import router as admin_router

app = FastAPI(
    title="Org Management Service",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

@app.get("/")
def root():
    return {"status": "API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

app.include_router(org_router, prefix="/api")
app.include_router(create_router, prefix="/api")
app.include_router(admin_router, prefix="/api")
