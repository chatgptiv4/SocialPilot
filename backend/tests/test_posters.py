from fastapi import status

from app.models.content import Template


def test_generate_poster(client, db_session):
    register = client.post("/api/auth/register", json={"email": "poster@example.com", "password": "pass1234"})
    assert register.status_code == status.HTTP_200_OK

    login = client.post("/api/auth/login", json={"email": "poster@example.com", "password": "pass1234"})
    token = login.json()["access_token"]

    template = Template(name="Basic", size="instagram_post", layout_config={"layers": []})
    db_session.add(template)
    db_session.commit()

    brand_payload = {
        "name": "Acme",
        "niche": "Retail",
        "target_audience": "Young adults",
        "tone": "Playful",
        "brand_colors": ["#000000"],
        "fonts": {"headline": "Inter", "body": "Arial"},
        "watermark_text": "Acme",
        "watermark_opacity": 40,
        "banned_words": ["cheap"],
        "preferred_cta": "Shop now",
    }
    brand = client.post("/api/brands", json=brand_payload, headers={"Authorization": f"Bearer {token}"})
    brand_id = brand.json()["id"]

    payload = {
        "brand_id": brand_id,
        "template_id": template.id,
        "title": "Launch",
        "size": "instagram_post",
        "overlay_text": "New product",
    }
    response = client.post("/api/posters/generate", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["image_url"].endswith(".png")
