"""Auth Pydantic schemalari."""
from __future__ import annotations

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=64)
    password: str = Field(..., min_length=1)
    tenant_id: str = Field(default="default")


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int  # saniye
    user: dict


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str | None = None


class CurrentUserResponse(BaseModel):
    username: str
    role: str
    ad_soyad: str | None = None
    tenant_id: str
    email: str | None = None
    student_id: str | None = None
    children_ids: list[str] = []
