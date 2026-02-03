from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from app.core.config import settings

SIZES = {
    "instagram_post": (1080, 1080),
    "instagram_story": (1080, 1920),
    "facebook_post": (1200, 630),
    "twitter": (1600, 900),
    "linkedin": (1200, 627),
}


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    font_candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in font_candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def _fit_text(draw: ImageDraw.ImageDraw, text: str, max_width: int, start_size: int) -> ImageFont.FreeTypeFont:
    size = start_size
    while size > 12:
        font = _load_font(size, bold=True)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width:
            return font
        size -= 2
    return _load_font(12, bold=True)


def _pick_contrast_color(image: Image.Image) -> tuple[int, int, int]:
    resized = image.resize((32, 32)).convert("L")
    avg = sum(resized.getdata()) / (32 * 32)
    return (20, 20, 20) if avg > 160 else (255, 255, 255)


def generate_poster_image(
    title: str,
    overlay_text: str,
    size_key: str,
    background_url: str | None = None,
    logo_url: str | None = None,
    watermark_text: str | None = None,
    watermark_opacity: int = 40,
) -> str:
    size = SIZES.get(size_key, (1080, 1080))
    if background_url and Path(background_url).exists():
        img = Image.open(background_url).convert("RGB").resize(size)
    else:
        img = Image.new("RGB", size, color=(20, 20, 20))
    draw = ImageDraw.Draw(img)
    title_font = _fit_text(draw, title, max_width=size[0] - 80, start_size=64)
    body_font = _fit_text(draw, overlay_text, max_width=size[0] - 80, start_size=40)
    text_color = _pick_contrast_color(img)
    draw.text((40, 40), title, fill=text_color, font=title_font)
    draw.text((40, 140), overlay_text, fill=text_color, font=body_font)

    if logo_url and Path(logo_url).exists():
        logo = Image.open(logo_url).convert("RGBA")
        logo.thumbnail((int(size[0] * 0.2), int(size[1] * 0.2)))
        img.paste(logo, (size[0] - logo.width - 40, 40), logo)

    if watermark_text:
        watermark_layer = Image.new("RGBA", size, (255, 255, 255, 0))
        watermark_draw = ImageDraw.Draw(watermark_layer)
        watermark_font = _load_font(24)
        opacity = max(0, min(100, watermark_opacity)) / 100
        watermark_draw.text(
            (size[0] - 240, size[1] - 60),
            watermark_text,
            fill=(255, 255, 255, int(255 * opacity)),
            font=watermark_font,
        )
        img = Image.alpha_composite(img.convert("RGBA"), watermark_layer).convert("RGB")

    output_dir = Path(settings.media_root) / "posters"
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"poster_{title.lower().replace(' ', '_')}.png"
    filepath = output_dir / filename
    img.save(filepath)
    return str(filepath)
