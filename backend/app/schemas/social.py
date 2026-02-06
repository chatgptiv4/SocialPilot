from pydantic import BaseModel


class ConnectedAccountCreate(BaseModel):
    provider: str
    account_name: str
    access_token: str
    refresh_token: str | None = None
    expires_at: str | None = None


class ConnectedAccountOut(BaseModel):
    id: int
    provider: str
    account_name: str

    class Config:
        from_attributes = True
