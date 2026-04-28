 # generate_basis_random.py
import numpy as np
from PIL import Image
import os

SIZE = 32
N_BASIS = SIZE * SIZE  # 1024

os.makedirs("basis_random", exist_ok=True)

# Фиксируем seed для воспроизводимости
np.random.seed(42)

basis = []
for i in range(N_BASIS):
    # Случайная бинарная матрица 32x32
    arr = np.random.randint(0, 2, (SIZE, SIZE)).astype(np.uint8)
    basis.append(arr)
    Image.fromarray(arr * 255).save(f"basis_random/basis_{i:04d}.png")

print(f"Создано {N_BASIS} случайных базисных изображений")

# Проверяем линейную независимость (почти наверняка да)
# Разворачиваем каждую картинку в вектор из 1024 пикселей
basis_flat = np.array([b.flatten() for b in basis])  # (1024, 1024)
rank = np.linalg.matrix_rank(basis_flat)

print(f"Ранг матрицы базиса: {rank} (должен быть {N_BASIS})")
print("Базис полный!" if rank == N_BASIS else "ВНИМАНИЕ: базис неполный")
if rank == N_BASIS:
    np.save("basis_random.npy", basis_flat)
