from pydantic import BaseModel


class UserAuthResponse(BaseModel):
    id: int
    login: str
    email: str | None
    email_verified: bool
    subscription_active: bool


class AuthCheckResponse(BaseModel):
    authenticated: bool
    user: UserAuthResponse | None
