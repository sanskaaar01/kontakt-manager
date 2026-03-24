from PIL import Image, ImageDraw, ImageFont
import random
import os

def generate_avatar(name):
    letter = name[0].upper()

    if not os.path.exists("avatars"):
        os.makedirs("avatars")

    colors = ["#FF5733", "#33C1FF", "#28B463", "#8E44AD", "#F39C12"]
    bg_color = random.choice(colors)

    img = Image.new("RGB", (100, 100), bg_color)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 50)
    except:
        font = ImageFont.load_default()

    # ✅ FIXED METHOD (new Pillow)
    bbox = draw.textbbox((0, 0), letter, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    draw.text(((100 - w) / 2, (100 - h) / 2), letter, fill="white", font=font)

    path = f"avatars/{letter}_{random.randint(1,9999)}.png"
    img.save(path)

    return path