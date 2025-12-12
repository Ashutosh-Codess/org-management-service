from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class OrganizationBase(BaseModel):
    organization_name: str = Field(..., examples=["Acme Inc"])


class OrganizationCreateRequest(OrganizationBase):
    email: EmailStr
    password: str = Field(..., min_length=6)


class OrganizationUpdateRequest(OrganizationBase):
    new_organization_name: Optional[str] = Field(None, examples=["Acme Labs"])
    new_email: Optional[EmailStr] = None
    new_password: Optional[str] = Field(None, min_length=6)


class OrganizationResponse(BaseModel):
    id: str
    organization_name: str
    collection_name: str
    admin_email: EmailStr
    created_at: datetime
    updated_at: datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    admin_id: str
    org_id: str


