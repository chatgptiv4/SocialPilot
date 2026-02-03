from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.brand import Brand, BrandAsset
from app.models.content import Caption, Poster, Template
from app.schemas.poster import CaptionGenerate, CaptionOut, PosterGenerate, PosterOut
from app.services.ai import build_brand_prompt, call_ai
from app.services.poster import generate_poster_image

router = APIRouter(prefix="/posters", tags=["posters"])


@router.post("/generate", response_model=PosterOut)
def generate_poster(payload: PosterGenerate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    brand = db.query(Brand).filter(Brand.id == payload.brand_id, Brand.user_id == user.id).first()
    template = db.query(Template).filter(Template.id == payload.template_id).first()
    if not brand or not template:
        raise HTTPException(status_code=404, detail="Brand or template not found")
    background = payload.background_url
    if not background:
        asset = (
            db.query(BrandAsset)
            .filter(BrandAsset.brand_id == brand.id, BrandAsset.asset_type == "background")
            .order_by(BrandAsset.created_at.desc())
            .first()
        )
        background = asset.file_url if asset else None
    logo_url = payload.logo_url or brand.logo_url
    image_url = generate_poster_image(
        payload.title,
        payload.overlay_text,
        payload.size,
        background_url=background,
        logo_url=logo_url,
        watermark_text=brand.watermark_text,
        watermark_opacity=brand.watermark_opacity,
    )
    poster = Poster(
        brand_id=brand.id,
        template_id=template.id,
        title=payload.title,
        size=payload.size,
        image_url=image_url,
    )
    db.add(poster)
    db.commit()
    db.refresh(poster)
    return poster


@router.get("/{poster_id}", response_model=PosterOut)
def get_poster(poster_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    poster = db.query(Poster).filter(Poster.id == poster_id).first()
    if not poster:
        raise HTTPException(status_code=404, detail="Poster not found")
    return poster


@router.post("/generate-caption", response_model=CaptionOut)
def generate_caption(payload: CaptionGenerate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    poster = db.query(Poster).filter(Poster.id == payload.poster_id).first()
    if not poster:
        raise HTTPException(status_code=404, detail="Poster not found")
    brand = db.query(Brand).filter(Brand.id == poster.brand_id, Brand.user_id == user.id).first()
    prompt = build_brand_prompt(brand) + f"\nWrite a caption: {payload.prompt}"
    response = call_ai(prompt)
    caption = Caption(poster_id=poster.id, content=response, hashtags=["#socialpilot", "#ai"])
    db.add(caption)
    db.commit()
    db.refresh(caption)
    return caption
