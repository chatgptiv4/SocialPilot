from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.brand import Brand
from app.models.content import AISuggestion, Caption, Campaign, CampaignItem, Poster, Template
from app.schemas.ai import ChatRequest, ChatResponse, OptimizeRequest, OptimizeResponse
from app.schemas.campaign import CampaignGenerate, CampaignOut, CampaignItemOut
from app.schemas.poster import CaptionOut
from app.services.ai import build_brand_prompt, call_ai, interpret_intent
from app.services.poster import generate_poster_image

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    brand = db.query(Brand).filter(Brand.id == payload.brand_id, Brand.user_id == user.id).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    intent = interpret_intent(payload.message)
    prompt = build_brand_prompt(brand) + f"\nUser request: {payload.message}"
    reply = call_ai(prompt)
    action = None
    payload_data = None
    if intent == "campaign":
        action = "generate_campaign"
        payload_data = {"brand_id": brand.id, "name": payload.message, "duration_days": 7}
    elif intent == "poster":
        action = "generate_poster"
        payload_data = {"brand_id": brand.id, "title": payload.message}
    elif intent == "caption":
        action = "generate_caption"
        payload_data = {"brand_id": brand.id, "prompt": payload.message}
    return ChatResponse(reply=reply, intent=intent, action=action, action_payload=payload_data)


@router.post("/generate-caption", response_model=CaptionOut)
def generate_caption(payload: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    poster_id = payload.get("poster_id")
    prompt = payload.get("prompt")
    if not poster_id or not prompt:
        raise HTTPException(status_code=400, detail="Missing poster_id or prompt")
    poster = db.query(Poster).filter(Poster.id == poster_id).first()
    brand = db.query(Brand).filter(Brand.id == poster.brand_id, Brand.user_id == user.id).first()
    ai_prompt = build_brand_prompt(brand) + f"\nWrite a caption: {prompt}"
    response = call_ai(ai_prompt)
    caption = Caption(poster_id=poster.id, content=response, hashtags=["#socialpilot", "#ai"])
    db.add(caption)
    db.commit()
    db.refresh(caption)
    return caption


@router.post("/generate-campaign", response_model=CampaignOut)
def generate_campaign(payload: CampaignGenerate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    brand = db.query(Brand).filter(Brand.id == payload.brand_id, Brand.user_id == user.id).first()
    template = db.query(Template).first()
    if not brand or not template:
        raise HTTPException(status_code=404, detail="Brand or template not found")
    campaign = Campaign(user_id=user.id, brand_id=brand.id, name=payload.name, duration_days=payload.duration_days)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)

    items = []
    for day in range(1, payload.duration_days + 1):
        day_prompt = build_brand_prompt(brand) + f"\nCreate content idea for day {day} of the campaign."
        ai_caption = call_ai(day_prompt)
        poster = Poster(
            brand_id=brand.id,
            template_id=template.id,
            title=f"Day {day} Post",
            size=template.size,
            image_url=generate_poster_image(f"Day {day}", "Campaign content", template.size),
        )
        db.add(poster)
        db.commit()
        db.refresh(poster)
        caption = Caption(poster_id=poster.id, content=ai_caption, hashtags=["#campaign"])
        db.add(caption)
        db.commit()
        db.refresh(caption)
        item = CampaignItem(campaign_id=campaign.id, day_index=day, poster_id=poster.id, caption_id=caption.id)
        db.add(item)
        db.commit()
        items.append(item)

    return CampaignOut(
        id=campaign.id,
        name=campaign.name,
        duration_days=campaign.duration_days,
        items=[
            CampaignItemOut(
                day_index=item.day_index,
                poster_id=item.poster_id,
                caption_id=item.caption_id,
                scheduled_time=item.scheduled_time,
            )
            for item in items
        ],
    )


@router.post("/optimize", response_model=OptimizeResponse)
def optimize(payload: OptimizeRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    brand = db.query(Brand).filter(Brand.id == payload.brand_id, Brand.user_id == user.id).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    suggestion = AISuggestion(brand_id=brand.id, suggestion_type="timing", content="Post at 9am for higher reach")
    db.add(suggestion)
    db.commit()
    return OptimizeResponse(suggestions=["Post at 9am", "Use #growth", "Repeat carousel content"])
