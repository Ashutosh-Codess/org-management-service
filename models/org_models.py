from pydantic import BaseModel, EmailStr

class OrgCreateRequest(BaseModel):
    organization_name: str
    email: EmailStr
    password: str

class OrgUpdateModel(BaseModel):
    old_organization_name: str
    new_organization_name: str

class AdminLoginModel(BaseModel):
    email: EmailStr
    password: str
