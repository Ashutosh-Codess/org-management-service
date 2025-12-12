from fastapi import APIRouter, HTTPException, Depends
from app.database import master_db
from bson import ObjectId
from app.models.org_models import OrgUpdateModel
from deps.admin_deps import get_current_admin

router = APIRouter(prefix="/org", tags=["Organization Management"])

@router.put("/update")
async def update_org(data: OrgUpdateModel, payload: dict = Depends(get_current_admin)):
    meta = await master_db.organizations.find_one({"organization_name": data.old_organization_name})
    if not meta:
        raise HTTPException(status_code=404, detail="Old organization not found")

    if payload.get("org_id") and str(meta["_id"]) != payload.get("org_id"):
        raise HTTPException(status_code=403, detail="Forbidden")

    new_collection = f"org_{data.new_organization_name}"
    old_collection = meta["collection"]

    await master_db[old_collection].rename(new_collection)

    await master_db.organizations.update_one(
        {"_id": meta["_id"]},
        {"": {
            "organization_name": data.new_organization_name,
            "collection": new_collection
        }}
    )
    return {"message": "Organization updated"}

@router.delete("/delete")
async def delete_org(organization_name: str, payload: dict = Depends(get_current_admin)):
    meta = await master_db.organizations.find_one({"organization_name": organization_name})
    if not meta:
        raise HTTPException(status_code=404, detail="Organization not found")

    if payload.get("org_id") and str(meta["_id"]) != payload.get("org_id"):
        raise HTTPException(status_code=403, detail="Forbidden")

    coll_name = meta["collection"]

    try:
        await master_db.drop_collection(coll_name)
    except:
        pass

    try:
        await master_db.admins.delete_one({"_id": ObjectId(meta["admin_id"])})
    except:
        pass

    await master_db.organizations.delete_one({"_id": meta["_id"]})

    return {"message": "Organization deleted"}
