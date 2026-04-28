import numpy as np
from PIL import Image
import os

def save_image(array, filename):
    """Сохраняет numpy-массив (0 и 1) как ч/б изображение."""
    # Переводим 1 -> 255 (белый), 0 -> 0 (чёрный)
    img = Image.fromarray((array * 255).astype(np.uint8), mode='L')
    img.save(filename)

def horizontal_lines(size=32, line_thickness=2):
    """
    32 картинки с горизонтальной линией на разной высоте.
    Высота линии меняется от 0 до size-1.
    """
    os.makedirs("horizontal", exist_ok=True)
    images = []

    for y_offset in range(size):
        arr = np.zeros((size, size), dtype=np.uint8)
        # Рисуем линию толщиной line_thickness
        half_t = line_thickness // 2
        y_start = max(0, y_offset - half_t)
        y_end = min(size, y_offset + line_thickness - half_t)
        arr[y_start:y_end, :] = 1

        images.append(arr)
        save_image(arr, f"horizontal/line_y_{y_offset:02d}.png")

    print(f"Создано {len(images)} изображений с горизонтальными линиями в папке 'horizontal/'")
    return images

def vertical_lines(size=32, line_thickness=2):
    """
    32 картинки с вертикальной линией на разной позиции по X.
    """
    os.makedirs("vertical", exist_ok=True)
    images = []

    for x_offset in range(size):
        arr = np.zeros((size, size), dtype=np.uint8)
        half_t = line_thickness // 2
        x_start = max(0, x_offset - half_t)
        x_end = min(size, x_offset + line_thickness - half_t)
        arr[:, x_start:x_end] = 1

        images.append(arr)
        save_image(arr, f"vertical/line_x_{x_offset:02d}.png")

    print(f"Создано {len(images)} изображений с вертикальными линиями в папке 'vertical/'")
    return images

def circles_different_diameter(size=32):
    """
    32 картинки с окружностями разного диаметра.
    Центр окружности всегда в середине изображения (size/2, size/2).
    Диаметр меняется от 1 до size (или чуть больше размера).
    Рисуется только контур окружности (граница).
    """
    os.makedirs("circles", exist_ok=True)
    images = []

    cx, cy = (size - 1) / 2, (size - 1) / 2  # центр

    for diameter in range(1, size + 1):
        arr = np.zeros((size, size), dtype=np.uint8)
        radius = diameter / 2.0

        # Создаём сетку координат
        Y, X = np.ogrid[:size, :size]
        dist = np.sqrt((X - cx)**2 + (Y - cy)**2)

        # Рисуем окружность: точки, где расстояние близко к радиусу (контур)
        thickness = 1.0
        # Всё, что между radius-thickness и radius+thickness — контур
        ring_mask = (dist >= radius - thickness/2) & (dist <= radius + thickness/2)
        arr[ring_mask] = 1

        images.append(arr)
        save_image(arr, f"circles/circle_d_{diameter:02d}.png")

    print(f"Создано {len(images)} изображений с окружностями в папке 'circles/'")
    return images

# =======================
# ГЕНЕРАЦИЯ ВСЕХ НАБОРОВ
# =======================
if __name__ == "__main__":
    SIZE = 32

    # 1. Горизонтальные линии (32 штуки)
    h_images = horizontal_lines(SIZE, line_thickness=2)

    # 2. Вертикальные линии (32 штуки)
    v_images = vertical_lines(SIZE, line_thickness=2)

    # 3. Окружности разного диаметра (32 штуки)
    c_images = circles_different_diameter(SIZE)

    print("\nГотово! Всего создано:")
    print(f"  - горизонтальные линии: {len(h_images)} шт.")
    print(f"  - вертикальные линии:   {len(v_images)} шт.")
    print(f"  - окружности:           {len(c_images)} шт.")
