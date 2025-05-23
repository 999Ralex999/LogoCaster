from PIL import Image
import os

# --- Папки ---
INPUT_DIR = "input"
OUTPUT_DIR = "output"
LOGO_DIR = "logos"
LOGO_SIZE_RATIO = 0.3  # Размер логотипа относительно ширины изображения

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
    W, H = base_img.size

    # Пропорция логотипа относительно ширины изображения
    LOGO_SIZE_RATIO = 0.25
    logo_w_target = int(W * LOGO_SIZE_RATIO)
    
    # Масштабирование логотипа по ширине
    ratio = logo_w_target / logo_img.width
    logo_h_target = int(logo_img.height * ratio)
    logo_resized = logo_img.resize((logo_w_target, logo_h_target), Image.LANCZOS)

    lw, lh = logo_resized.size
    center_x = W // 2
    center_y = H // 2

    # Смещение от центра (35% ширины и высоты)
    offset_x = int(W * 0.35)
    offset_y = int(H * 0.35)

    # 5 позиций: центр + диагонали
    positions = [
        (center_x - lw // 2, center_y - lh // 2),                            # Центр
        (center_x - offset_x - lw // 2, center_y - offset_y - lh // 2),     # Левый верх
        (center_x + offset_x - lw // 2, center_y - offset_y - lh // 2),     # Правый верх
        (center_x - offset_x - lw // 2, center_y + offset_y - lh // 2),     # Левый низ
        (center_x + offset_x - lw // 2, center_y + offset_y - lh // 2),     # Правый низ
    ]

    overlay = Image.new("RGBA", base_img.size, (255, 255, 255, 0))

    for x, y in positions:
        overlay.paste(logo_resized, (x, y), logo_resized)

    result = Image.alpha_composite(base_img, overlay)

    output_filename = os.path.splitext(os.path.basename(image_path))[0] + "." + output_format.lower()
    result.convert("RGB").save(os.path.join(OUTPUT_DIR, output_filename), output_format)
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

