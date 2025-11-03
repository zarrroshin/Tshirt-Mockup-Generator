from celery import shared_task
from PIL import Image, ImageDraw, ImageFont
from .models import Mockup
import os
from django.conf import settings

@shared_task
def generate_mockup(text):
    base_colors = ["black", "blue", "white", "yellow"]
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 60)

    results = []
    for color in base_colors:
        base_path = os.path.join(settings.BASE_DIR, f"mockups/static/mockups/{color}.png")
        image = Image.open(base_path)

        draw = ImageDraw.Draw(image)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        image_width, image_height = image.size
        position = ((image_width - text_width) // 2, (image_height - text_height) // 2)

        # Choose contrasting text color automatically
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
