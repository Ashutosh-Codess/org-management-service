from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app import auth
from app.database import get_master_db
from app.schemas import (
    LoginRequest,
    OrganizationCreateRequest,
    OrganizationResponse,
    OrganizationUpdateRequest,
    TokenResponse,
)
from app.utils import generate_id, slugify

router = APIRouter()


@router.post("/org/create", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(payload: OrganizationCreateRequest):
    db = get_master_db()
    slug = slugify(payload.organization_name)
    existing = await db.organizations.find_one({"slug": slug})
    if existing:
        raise HTTPException(status_code=400, detail="Organization name already exists")

    admin_conflict = await db.admins.find_one({"email": payload.email})
    if admin_conflict:
        raise HTTPException(status_code=400, detail="Admin email already registered")

    collection_name = f"org_{slug}"
    # Create empty collection for organization
    if collection_name in await db.list_collection_names():
        raise HTTPException(status_code=400, detail="Organization collection already exists")

    await db.create_collection(collection_name)

    admin_id = generate_id()
    org_id = generate_id()
    now = datetime.utcnow()

    await db.admins.insert_one(
        {
            "_id": admin_id,
            "email": payload.email,
            "password_hash": auth.get_password_hash(payload.password),
            "org_id": org_id,
            "created_at": now,
        }
    )
    await db.organizations.insert_one(
        {
            "_id": org_id,
            "name": payload.organization_name,
            "slug": slug,
            "collection_name": collection_name,
            "created_at": now,
            "updated_at": now,
            "admin_id": admin_id,
        }
    )

    return OrganizationResponse(
        id=org_id,
        organization_name=payload.organization_name,
        collection_name=collection_name,
        admin_email=payload.email,
        created_at=now,
        updated_at=now,
    )


@router.get("/org/get", response_model=OrganizationResponse)
async def get_organization(organization_name: str = Query(..., description="Organization name to fetch")):
    db = get_master_db()
    slug = slugify(organization_name)
    org = await db.organizations.find_one({"slug": slug})
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    admin = await db.admins.find_one({"_id": org["admin_id"]})
    return OrganizationResponse(
        id=org["_id"],
        organization_name=org["name"],
        collection_name=org["collection_name"],
        admin_email=admin["email"] if admin else "",
        created_at=org["created_at"],
        updated_at=org["updated_at"],
    )


@router.put("/org/update", response_model=OrganizationResponse)
async def update_organization(
    payload: OrganizationUpdateRequest, current=Depends(auth.get_current_admin)
):
    db = get_master_db()
    org = current["organization"]
    admin = current["admin"]

    # Ensure the token's org matches the payload
    if slugify(payload.organization_name) != org["slug"]:
        raise HTTPException(status_code=403, detail="Organization mismatch")

    updates = {}
    if payload.new_organization_name:
        new_slug = slugify(payload.new_organization_name)
        if new_slug != org["slug"]:
            exists = await db.organizations.find_one({"slug": new_slug})
            if exists:
                raise HTTPException(status_code=400, detail="New organization name already exists")
            new_collection_name = f"org_{new_slug}"
            # rename collection to keep data
            await db[org["collection_name"]].rename(new_collection_name, dropTarget=True)
            updates.update({"name": payload.new_organization_name, "slug": new_slug, "collection_name": new_collection_name})

    changed = False

    if payload.new_email:
        email_conflict = await db.admins.find_one({"email": payload.new_email, "_id": {"$ne": admin["_id"]}})
        if email_conflict:
            raise HTTPException(status_code=400, detail="Email already in use")
        await db.admins.update_one({"_id": admin["_id"]}, {"$set": {"email": payload.new_email}})
        admin["email"] = payload.new_email
        changed = True

    if payload.new_password:
        await db.admins.update_one(
            {"_id": admin["_id"]}, {"$set": {"password_hash": auth.get_password_hash(payload.new_password)}}
        )
        changed = True

    if updates or changed:
        updates["updated_at"] = datetime.utcnow()
        await db.organizations.update_one({"_id": org["_id"]}, {"$set": updates})
        org.update(updates)

    return OrganizationResponse(
        id=org["_id"],
        organization_name=org["name"],
        collection_name=org["collection_name"],
        admin_email=admin["email"],
        created_at=org["created_at"],
        updated_at=org.get("updated_at", datetime.utcnow()),
    )


@router.delete("/org/delete")
async def delete_organization(
    organization_name: str = Query(...), current=Depends(auth.get_current_admin)
):
    db = get_master_db()
    org = current["organization"]
    admin = current["admin"]
    if slugify(organization_name) != org["slug"]:
        raise HTTPException(status_code=403, detail="Organization mismatch")

    # Drop org collection and remove metadata
    await db.drop_collection(org["collection_name"])
    await db.organizations.delete_one({"_id": org["_id"]})
    await db.admins.delete_one({"_id": admin["_id"]})
    return {"message": "Organization deleted"}


@router.post("/admin/login", response_model=TokenResponse)
async def admin_login(payload: LoginRequest):
    db = get_master_db()
    admin = await db.admins.find_one({"email": payload.email})
    if not admin or not auth.verify_password(payload.password, admin["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    org = await db.organizations.find_one({"_id": admin["org_id"]})
    if not org:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Organization not found for admin")

    token = auth.create_access_token({"admin_id": admin["_id"], "org_id": org["_id"], "org_slug": org["slug"]})
    return TokenResponse(access_token=token, admin_id=admin["_id"], org_id=org["_id"])

