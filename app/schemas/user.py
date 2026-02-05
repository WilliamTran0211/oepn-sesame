import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Email for login")
    password: str = Field(..., description="Password for login")


class UserRegistration(BaseModel):
    email: EmailStr = Field(
        ..., description="Valid email address", examples=["user@company.com"]
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Password must be 8-100 characters",
    )
    is_active: bool = Field(default=True)

    @field_validator("password")
    def validate_password_complexity(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one number")
        return v


class UserSchemaBase(BaseModel):
    email: str | None = None
    full_name: str | None = None


class UserSchemaCreate(UserSchemaBase):
    """Schema for creating a user"""

    id: str = Field(..., description="Unique user identifier")

    class Config:
        from_attributes = True
