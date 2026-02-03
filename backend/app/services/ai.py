from app.models.brand import Brand
from app.core.config import settings
import httpx


def build_brand_prompt(brand: Brand) -> str:
    return (
        f"Brand Name: {brand.name}\n"
        f"Niche: {brand.niche}\n"
        f"Target Audience: {brand.target_audience}\n"
        f"Tone: {brand.tone}\n"
        f"Brand Colors: {', '.join(brand.brand_colors)}\n"
        f"Fonts: {brand.fonts}\n"
        f"Watermark: {brand.watermark_text or 'None'}\n"
        f"Banned Words: {', '.join(brand.banned_words)}\n"
        f"Preferred CTA: {brand.preferred_cta}\n"
    )


def call_ai(prompt: str) -> str:
    if not settings.openai_api_key:
        return "AI response generated locally based on prompt." 
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a marketing assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
    }
    headers = {"Authorization": f"Bearer {settings.openai_api_key}"}
    with httpx.Client(timeout=30) as client:
        response = client.post(f"{settings.openai_base_url}/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
    return data["choices"][0]["message"]["content"]


def interpret_intent(message: str) -> str:
    lowered = message.lower()
    if "campaign" in lowered:
        return "campaign"
    if "caption" in lowered:
        return "caption"
    if "poster" in lowered or "flyer" in lowered:
        return "poster"
    return "general"
