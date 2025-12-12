from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.database import master_db
from passlib.hash import argon2
from config.jwt import create_access_token

router = APIRouter()

class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post('/admin/login')
async def admin_login(data: AdminLoginRequest):
    admin = await master_db.admins.find_one({'email': data.email})
    if not admin:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    if not argon2.verify(data.password, admin.get('password')):
        raise HTTPException(status_code=401, detail='Invalid credentials')

    # find organization meta for this admin (if any)
    org_meta = await master_db.organizations.find_one({'admin_id': str(admin['_id'])})
    org_id = str(org_meta['_id']) if org_meta else None
    token = create_access_token({'admin_id': str(admin['_id']), 'org_id': org_id})
    return {'access_token': token, 'token_type': 'bearer'}
