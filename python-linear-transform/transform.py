from PIL import Image
import numpy as np
import sys

def linear_transform(
    input_path: str,
    output_path: str,
    matrix: list[list[float]],  # матрица 2x2: [[a, b], [c, d]]
    origin: tuple[int, int] = (0, 0),  # начало координат (неподвижная точка)
    background_color: tuple[int, int, int] = (255, 255, 255)  # чем заливать пустоты (белый)
):
    """
    Применяет линейное преобразование к изображению.
    Точка `origin` остается на месте (A(origin) = origin).

    Матрица действует так:
        x' = a*(x - ox) + b*(y - oy) + ox
        y' = c*(x - ox) + d*(y - oy) + oy
    """

    # Открываем изображение и переводим в RGB (на случай PNG с альфа-каналом)
    img = Image.open(input_path).convert("RGB")
    W, H = img.size
    pixels_in = np.array(img)  # форма (H, W, 3)

    # Распаковываем матрицу для читаемости
    a, b = matrix[0]
    c, d = matrix[1]
    ox, oy = origin

    # Создаем пустой холст под выходное изображение
    # Размеры можно взять с запасом, например как у исходного
    out_img = Image.new("RGB", (W, H), background_color)
    pixels_out = np.array(out_img)

    # --- ПРЯМОЙ ПРОХОД (forward mapping) ---
    # Для каждого пикселя исходного изображения вычисляем,
    # в какой пиксель выходного он попадает под действием матрицы.
    # Так мы гарантируем, что каждый пиксель исходника будет куда-то перенесен.
    for y in range(H):
        for x in range(W):
            # Применяем линейное преобразование относительно origin
            x_new = int(a * (x - ox) + b * (y - oy) + ox)
            y_new = int(c * (x - ox) + d * (y - oy) + oy)

            # Проверяем, попадает ли точка в границы выходного холста
            if 0 <= x_new < W and 0 <= y_new < H:
                pixels_out[y_new, x_new] = pixels_in[y, x]

    # Сохраняем результат
    Image.fromarray(pixels_out).save(output_path)
    print(f"Сохранено: {output_path}")


# ============================================
# ПРИМЕР ИСПОЛЬЗОВАНИЯ
# ============================================
if __name__ == "__main__":
    # 1. Путь к картинке
    photo = "cat.jpg"

    # 2. Выбрали начало координат (например, левый верхний угол книги)
    #    Пусть это точка (150, 100) на фото
    pivot = (150, 100)

    # 3. Столбцы матрицы — это образы базисных векторов.
    mat = [
        [1.0, 0.3],
        [-0.3, 0.5]
    ]
    # первый базисный вектор (1,0) -> (1.0, -0.3)
    # второй базисный вектор (0,1) -> (0.3, 0.5)

    linear_transform(photo, "output_transformed.jpg", mat, origin=pivot)
