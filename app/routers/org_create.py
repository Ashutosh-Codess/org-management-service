from fastapi import APIRouter, HTTPException
from app.database import master_db
from app.models.org_models import OrgCreateRequest
from passlib.hash import argon2

router = APIRouter()

@router.post("/org/create")
async def create_org(data: OrgCreateRequest):
    existing = await master_db.organizations.find_one({"organization_name": data.organization_name})
    if existing:
        raise HTTPException(status_code=400, detail="Organization already exists")

    hashed = argon2.hash(data.password)

    admin = {
        "email": data.email,
        "password": hashed
    }

    admin_id = await master_db.admins.insert_one(admin)

    collection_name = f"org_{data.organization_name}"

    meta = {
        "organization_name": data.organization_name,
        "collection": collection_name,
        "admin_id": str(admin_id.inserted_id),
    }

    await master_db.organizations.insert_one(meta)

    return {"message": "Organization created", "collection": collection_name}
