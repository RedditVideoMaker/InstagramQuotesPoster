import requests
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random
from datetime import datetime
import os
import json

QUOTES_FILE = "posted_quotes.json"

def fetch_random_quote():
    url = "https://zenquotes.io/api/random"
    response = requests.get(url)
    data = response.json()
    return data[0]["q"], data[0]["a"]

def draw_text_with_shadow(draw, position, text, font, text_color, shadow_color, shadow_offset):
    x, y = position
    # Draw shadow
    draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=shadow_color)
    # Draw text
    draw.text(position, text, font=font, fill=text_color)

def create_instagram_post(quote, author):
    """Creates an Instagram post image with a warm, cozy background and the quote."""
    # Image dimensions (square for Instagram)
    width, height = 1080, 1080

    # Create a warm, cozy gradient background
    bg_colors = [
        (255, 213, 153),  # Light orange
        (255, 179, 102),  # Soft orange
        (255, 140, 105),  # Warm peach
        (255, 204, 153)   # Warm beige
    ]
    gradient_color = random.choice(bg_colors)
    image = Image.new("RGB", (width, height), gradient_color)
    draw = ImageDraw.Draw(image)

    # Load the Cormorant Garamond font
    font_path = "fonts/CormorantGaramond-Bold.ttf"
    font = ImageFont.truetype(font_path, 60)  # Increased font size
    author_font = ImageFont.truetype(font_path, 50)  # Increased font size
    watermark_font = ImageFont.truetype(font_path, 30)  # Increased font size

    margin = 100
    max_width = width - 2 * margin
    lines = textwrap.wrap(quote, width=30)
    y_text = height // 2 - len(lines) * 30  # Adjusted for larger font size

    # Draw the quote
    text_color = "black"
    for line in lines:
        text_bbox = draw.textbbox((0, 0), line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x_text = (width - text_width) // 2
        draw.text((x_text, y_text), line, font=font, fill=text_color)
        y_text += text_height + 15  # Adjusted for larger font size

    # Draw the author below the quote
    author_text = f"- {author}"
    author_bbox = draw.textbbox((0, 0), author_text, font=author_font)
    author_width = author_bbox[2] - author_bbox[0]
    draw.text(((width - author_width) // 2, y_text + 20),
              author_text, font=author_font, fill=text_color)

    # Add watermark
    watermark_text = "@radiantrisevibes"
    watermark_bbox = draw.textbbox((0, 0), watermark_text, font=watermark_font)
    watermark_width = watermark_bbox[2] - watermark_bbox[0]
    watermark_height = watermark_bbox[3] - watermark_bbox[1]
    draw.text((width - watermark_width - 10, height - watermark_height - 10),
              watermark_text, font=watermark_font, fill=text_color)

    # Save the image in the Images folder with the date as the filename
    date_str = datetime.now().strftime("%Y-%m-%d")
    images_folder = "Images"
    os.makedirs(images_folder, exist_ok=True)
    image_path = os.path.join(images_folder, f"{date_str}.png")
    image.save(image_path)
    print(f"Instagram post saved as '{image_path}'")

    # Save the quote to the JSON file
    save_posted_quote(quote, author)

def save_posted_quote(quote, author):
    if os.path.exists(QUOTES_FILE):
        with open(QUOTES_FILE, "r") as file:
            posted_quotes = json.load(file)
    else:
        posted_quotes = []

    posted_quotes.append({"quote": quote, "author": author})

    with open(QUOTES_FILE, "w") as file:
        json.dump(posted_quotes, file, indent=4)

if __name__ == "__main__":
    quote, author = fetch_random_quote()
    create_instagram_post(quote, author)
