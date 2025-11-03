from celery import shared_task
from PIL import Image, ImageDraw, ImageFont
from .models import Mockup
import os
from django.conf import settings

@shared_task
def generate_mockup(text, font_name=None, text_color=None, shirt_colors=None):
    """
    Generates T-shirt mockups with custom font, text color, and shirt colors.
    """

    # Default values
    base_colors = ["black", "blue", "white", "yellow"]
    if shirt_colors:
        # only include requested colors that exist
        base_colors = [c for c in shirt_colors if c in base_colors]

    # font path
    if font_name:
        font_path = os.path.join("/usr/share/fonts/truetype/dejavu", font_name)
        if not os.path.exists(font_path):
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    else:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    # default text color (will be adjusted for contrast if not set)
    default_text_color = text_color or None

    font = ImageFont.truetype(font_path, 60)
    results = []

    for color in base_colors:
        base_path = os.path.join(settings.BASE_DIR, f"mockups/static/mockups/{color}.png")
        image = Image.open(base_path).convert("RGBA")
        draw = ImageDraw.Draw(image)

        # Compute text size using textbbox
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        image_width, image_height = image.size

        position = ((image_width - text_width) // 2, (image_height - text_height) // 2)

        # choose text color (if not given)
        if default_text_color:
            fill_color = default_text_color
        else:
            fill_color = "white" if color in ["black", "blue"] else "black"

        draw.text(position, text, fill=fill_color, font=font)

        output_name = f"{text.replace(' ', '_')}_{color}.png"
        output_path = os.path.join(settings.MEDIA_ROOT, "mockups", output_name)
        image.save(output_path)

        mockup = Mockup.objects.create(
            text=text,
            image=f"mockups/{output_name}"
        )
        results.append(mockup.image.url)

    return results
