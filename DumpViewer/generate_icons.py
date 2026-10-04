from PIL import Image, ImageDraw, ImageFont

SIZE = (32, 32)

ICONS = {
    "icon_user.png":     ("#4A90E2", "U"),
    "icon_vendor.png":   ("#9B59B6", "V"),
    "icon_system.png":   ("#8E6E53", "S"),
    "icon_native.png":   ("#000000", "N"),
    "icon_function.png": ("#27AE60", "f"),
    "icon_lambda.png":   ("#E67E22", "λ"),
    "icon_unknown.png":  ("#7F8C8D", "?"),
}

# Font laden
try:
    font = ImageFont.truetype("arial.ttf", 20)
except:
    font = ImageFont.load_default()

for filename, (color, symbol) in ICONS.items():
    img = Image.new("RGB", SIZE, color)  # RGB = Qt-sicher
    draw = ImageDraw.Draw(img)

    # Textgröße bestimmen (Pillow 10+)
    bbox = draw.textbbox((0, 0), symbol, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    # Text zentrieren
    draw.text(
        ((SIZE[0] - w) / 2, (SIZE[1] - h) / 2),
        symbol,
        fill="white",
        font=font
    )

    img.save(f"assets/icons/{filename}", format="PNG")
    print("Erzeugt:", filename)
