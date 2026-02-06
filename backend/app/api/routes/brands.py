from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.db.session import get_db
from app.models.brand import Brand, BrandAsset
from app.schemas.brand import BrandCreate, BrandOut, BrandUpdate

router = APIRouter(prefix="/brands", tags=["brands"])


@router.get("", response_model=list[BrandOut])
def list_brands(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Brand).filter(Brand.user_id == user.id).all()


@router.post("", response_model=BrandOut)
def create_brand(brand_in: BrandCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    brand = Brand(user_id=user.id, **brand_in.model_dump())
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand


@router.put("/{brand_id}", response_model=BrandOut)
def update_brand(brand_id: int, brand_in: BrandUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    brand = db.query(Brand).filter(Brand.id == brand_id, Brand.user_id == user.id).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    for key, value in brand_in.model_dump().items():
        setattr(brand, key, value)
    db.commit()
    db.refresh(brand)
    return brand


@router.post("/{brand_id}/upload-logo", response_model=BrandOut)
def upload_logo(
    brand_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    brand = db.query(Brand).filter(Brand.id == brand_id, Brand.user_id == user.id).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    output_dir = Path(settings.media_root) / "logos"
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / file.filename
    filepath.write_bytes(file.file.read())
    brand.logo_url = str(filepath)
    db.commit()
    return brand


@router.post("/{brand_id}/upload-background")
def upload_background(
    brand_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    brand = db.query(Brand).filter(Brand.id == brand_id, Brand.user_id == user.id).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    output_dir = Path(settings.media_root) / "backgrounds"
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / file.filename
    filepath.write_bytes(file.file.read())
    asset = BrandAsset(brand_id=brand.id, asset_type="background", file_url=str(filepath))
    db.add(asset)
    db.commit()
    return {"status": "uploaded"}
