from PIL import Image
import os

# --- Папки ---
INPUT_DIR = "input"
OUTPUT_DIR = "output"
LOGO_DIR = "logos"
LOGO_SIZE_RATIO = 0.2  # Размер логотипа относительно ширины изображения

# --- Доступные форматы ---
SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png", ".webp")

# --- Создание выходной папки ---
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Выбор логотипа ---
logo_files = [f for f in os.listdir(LOGO_DIR) if f.lower().endswith(SUPPORTED_FORMATS)]
print("Выберите логотип:")
for idx, name in enumerate(logo_files, start=1):
    print(f"{idx}. {name}")

logo_choice = int(input("Введите номер логотипа: ")) - 1
logo_path = os.path.join(LOGO_DIR, logo_files[logo_choice])
logo = Image.open(logo_path).convert("RGBA")

# --- Выбор формата выхода ---
print("\nВыберите формат на выходе:")
formats = ["JPEG", "PNG", "WEBP"]
for idx, fmt in enumerate(formats, start=1):
    print(f"{idx}. {fmt}")

format_choice = int(input("Введите номер формата: ")) - 1
output_format = formats[format_choice]

# --- Логика наложения логотипа ---
def resize_logo(base_img, logo_img):
    w = int(base_img.width * LOGO_SIZE_RATIO)
    ratio = w / logo_img.width
    h = int(logo_img.height * ratio)
    return logo_img.resize((w, h), Image.LANCZOS)

def apply_logo(image_path, logo_img):
    base_img = Image.open(image_path).convert("RGBA")
    logo_resized = resize_logo(base_img, logo_img)

    W, H = base_img.size
    center_x = W // 2
    center_y = H // 2

    # Смещения в процентах от ширины/высоты
    relative_offsets = [
        (0.0, 0.0),      # Центр
        (0.1, -0.1),     # Вверх-вправо
        (0.2, -0.2),     # Еще выше вправо
        (-0.1, 0.1),     # Вниз-влево
        (-0.2, 0.2)      # Еще ниже влево
    ]

    for dx_perc, dy_perc in relative_offsets:
        dx = int(W * dx_perc)
        dy = int(H * dy_perc)
        x = center_x + dx - logo_resized.width // 2
        y = center_y + dy - logo_resized.height // 2
        base_img.paste(logo_resized, (x, y), logo_resized)

    # Сохраняем
    output_filename = os.path.splitext(os.path.basename(image_path))[0] + "." + output_format.lower()
    base_img.convert("RGB").save(os.path.join(OUTPUT_DIR, output_filename), output_format)
    print(f"✅ {output_filename} создан")



# --- Обработка изображений ---
count = 0
for filename in os.listdir(INPUT_DIR):
    if filename.lower().endswith(SUPPORTED_FORMATS):
        filepath = os.path.join(INPUT_DIR, filename)
        apply_logo(filepath, logo)
        count += 1
        if count >= 10:
            break

print("🚀 Все изображения обработаны.")

