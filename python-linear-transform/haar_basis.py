import numpy as np
from PIL import Image
import os

SIZE = 32
os.makedirs("basis_haar", exist_ok=True)

def haar_basis_vector(size, i, j, scale):
    """
    Генерирует один вектор базиса Хаара.
    size: размер изображения (32)
    i, j: координаты блока
    scale: масштаб (размер блока = 2^scale)
    """
    block_size = 2 ** scale
    arr = np.zeros((size, size))

    # Позиция блока
    y_start = i * block_size
    x_start = j * block_size
    y_end = y_start + block_size
    x_end = x_start + block_size

    half = block_size // 2

    # Усредняющая функция (масштабирующая)
    if i == 0 and j == 0 and scale == 0:
        # Это нужно только для самого первого вектора, но мы его не так генерируем
        pass

    # Три типа вейвлетов Хаара в 2D:
    # HH: + в левом верхнем и правом нижнем, - в остальных
    # HG: + слева, - справа  (горизонтальный перепад)
    # GH: + сверху, - снизу  (вертикальный перепад)

    return arr

def generate_haar_basis_2d(size):
    """
    Генерирует полный 2D базис Хаара.
    Возвращает список матриц size x size.
    """
    basis = []
    labels = []

    # Начинаем с постоянной составляющей
    arr = np.ones((size, size))
    arr = arr / np.linalg.norm(arr)  # нормируем
    basis.append(arr)
    labels.append("DC")

    # Для каждого масштаба
    scale = 0
    current_size = size
    while current_size > 1:
        block_size = current_size
        n_blocks = size // block_size

        for i in range(n_blocks):
            for j in range(n_blocks):
                half = block_size // 2
                y = i * block_size
                x = j * block_size

                # HG: лево-право (+ слева, - справа)
                arr = np.zeros((size, size))
                arr[y:y+block_size, x:x+half] = 1
                arr[y:y+block_size, x+half:x+block_size] = -1
                arr = arr / np.linalg.norm(arr)
                basis.append(arr)
                labels.append(f"HG_s{scale}_i{i}_j{j}")

                # GH: верх-низ (+ сверху, - снизу)
                arr = np.zeros((size, size))
                arr[y:y+half, x:x+block_size] = 1
                arr[y+half:y+block_size, x:x+block_size] = -1
                arr = arr / np.linalg.norm(arr)
                basis.append(arr)
                labels.append(f"GH_s{scale}_i{i}_j{j}")

                # HH: диагональный (+ в противоположных углах, - в других)
                arr = np.zeros((size, size))
                arr[y:y+half, x:x+half] = 1                    # левый верх
                arr[y+half:y+block_size, x+half:x+block_size] = 1  # правый низ
                arr[y:y+half, x+half:x+block_size] = -1        # правый верх
                arr[y+half:y+block_size, x:x+half] = -1        # левый низ
                arr = arr / np.linalg.norm(arr)
                basis.append(arr)
                labels.append(f"HH_s{scale}_i{i}_j{j}")

        current_size //= 2
        scale += 1

    # Должно получиться ровно size*size векторов
    return basis[:size*size], labels[:size*size]

basis_vectors, basis_labels = generate_haar_basis_2d(SIZE)

print(f"Сгенерировано {len(basis_vectors)} векторов базиса Хаара")

# Сохраняем как изображения
for idx, (arr, label) in enumerate(zip(basis_vectors, basis_labels)):
    # Нормализуем в [0, 255] для визуализации
    arr_vis = (arr - arr.min()) / (arr.max() - arr.min() + 1e-10) * 255
    Image.fromarray(arr_vis.astype(np.uint8)).save(f"basis_haar/basis_{idx:04d}_{label}.png")

# Сохраняем матрицу
basis_flat = np.array([b.flatten() for b in basis_vectors])
np.save("basis_haar_matrix.npy", basis_flat)

rank = np.linalg.matrix_rank(basis_flat)
print(f"Ранг базиса Хаара: {rank}")

# Проверяем ортогональность
gram = basis_flat @ basis_flat.T
off_diag = gram - np.eye(len(gram))
print(f"Максимальное отклонение от ортогональности: {np.max(np.abs(off_diag)):.10f}")
