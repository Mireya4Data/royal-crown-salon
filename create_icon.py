from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Teal background circle
    draw.ellipse([0, 0, size, size], fill='#0F4C5C')

    # Gold inner circle
    margin = int(size * 0.12)
    draw.ellipse([margin, margin, size - margin, size - margin], fill='#D4AF37')

    # RC text in teal
    font_size = int(size * 0.32)
    try:
        font = ImageFont.truetype("arialbd.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), "RC", font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (size - text_w) // 2
    y = (size - text_h) // 2

    draw.text((x, y), "RC", fill='#0F4C5C', font=font)

    os.makedirs('core/static/icons', exist_ok=True)
    img.save(filename, 'PNG')
    print(f"✅ Created {filename}")

create_icon(192, 'core/static/icons/icon-192.png')
create_icon(512, 'core/static/icons/icon-512.png')
print("🎉 Both icons created!")