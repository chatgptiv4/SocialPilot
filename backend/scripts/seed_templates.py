from app.db.session import SessionLocal
from app.models.content import Template


def run():
    db = SessionLocal()
    try:
        templates = [
            Template(name="Instagram Post", size="instagram_post", layout_config={"layers": ["title", "cta"]}),
            Template(name="Instagram Story", size="instagram_story", layout_config={"layers": ["headline", "logo"]}),
            Template(name="Facebook Post", size="facebook_post", layout_config={"layers": ["title", "body"]}),
            Template(name="Twitter Post", size="twitter", layout_config={"layers": ["headline"]}),
            Template(name="LinkedIn Post", size="linkedin", layout_config={"layers": ["title", "subtitle"]}),
        ]
        db.add_all(templates)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    run()
