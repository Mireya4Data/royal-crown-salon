from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    # Create image with teal background
    img = Image.new('RGB', (size, size), color='#0F4C5C')
    draw = ImageDraw.Draw(img)

    # Draw a gold circle
    margin = size // 8
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill='#D4AF37'
    )

    # Draw "RC" text in teal color centered on the gold circle
    text = "RC"
    font_size = size // 3

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()

    # Get text size and center it
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - (size // 20)

    draw.text((x, y), text, fill='#0F4C5C', font=font)

    # Save
    os.makedirs('core/static/icons', exist_ok=True)
    img.save(filename)
    print(f"Created {filename}")

create_icon(192, 'core/static/icons/icon-192.png')
create_icon(512, 'core/static/icons/icon-512.png')
print("Icons created successfully!")