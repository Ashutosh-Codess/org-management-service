from fastapi import FastAPI
from routes.org_create import router as org_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(org_router)
