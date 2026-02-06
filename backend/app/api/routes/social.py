from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.crypto import encrypt_value
from app.db.session import get_db
from app.models.content import ConnectedAccount
from app.schemas.social import ConnectedAccountCreate, ConnectedAccountOut

router = APIRouter(prefix="/social", tags=["social"])


@router.get("/accounts", response_model=list[ConnectedAccountOut])
def list_accounts(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(ConnectedAccount).filter(ConnectedAccount.user_id == user.id).all()


@router.post("/connect/{provider}", response_model=ConnectedAccountOut)
def connect_account(
    provider: str, payload: ConnectedAccountCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    account = ConnectedAccount(
        user_id=user.id,
        provider=provider,
        account_name=payload.account_name,
        access_token=encrypt_value(payload.access_token),
        refresh_token=encrypt_value(payload.refresh_token) if payload.refresh_token else None,
        expires_at=payload.expires_at,
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@router.delete("/accounts/{account_id}")
def delete_account(account_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    account = db.query(ConnectedAccount).filter(ConnectedAccount.id == account_id, ConnectedAccount.user_id == user.id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    db.delete(account)
    db.commit()
    return {"status": "deleted"}
