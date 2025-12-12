from pydantic import BaseModel, EmailStr, field_validator

class OrgCreateRequest(BaseModel):
    organization_name: str
    email: EmailStr
    password: str

    @field_validator("password")
    def check_password_len(cls, v):
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password must be <= 72 bytes for bcrypt.")
        return v
