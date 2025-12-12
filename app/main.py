from fastapi import FastAPI
from app.routers.org_routes import router as org_router
from app.routers.org_create import router as create_router
from app.routers.admin_auth import router as admin_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

# Register routers
app.include_router(create_router)
app.include_router(org_router)
app.include_router(admin_router)
