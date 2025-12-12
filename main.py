from fastapi import FastAPI
from routes import org_routes, admin_routes
import uvicorn

app = FastAPI(title="Wedding Project - Org Management")

app.include_router(org_routes.router, prefix="/org", tags=["org"])
app.include_router(admin_routes.router, prefix="/admin", tags=["admin"])

@app.get("/")
def root():
    return {"message": "Wedding project backend running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
