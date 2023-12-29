import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

from utils import CMAP


def generate_black_background_interference(
    size=(100, 100),
    min_spot_width=10,
    max_spot_width=20,
    min_spot_height=0,
    max_spot_height=3,
    intensity=1.5,
    blur_sigma=0.9,
    spot_frequency=0.4,
):
    """
    Генерирует радио помехи на черном фоне с редкими пятнами помех.

    Параметры:
    size (tuple): размер матрицы (высота, ширина).
    min_spot_width (int): минимальная ширина пятна.
    max_spot_width (int): максимальная ширина пятна.
    min_spot_height (int): минимальная высота пятна.
    max_spot_height (int): максимальная высота пятна.
    intensity (int): интенсивность помех.
    blur_sigma (float): степень размытия границ пятен.
    spot_frequency (float): частота появления пятен помех.

    Возвращает:
    numpy.ndarray: матрица с радио помехами.
    """
    interference = np.zeros(size) - 1  # Изначально весь фон черный (-1)
    rows, cols = size

    # Покрытие матрицы вытянутыми пятнами помех с низкой частотой
    for i in range(0, rows, max_spot_height):
        for j in range(0, cols, max_spot_width):
            if np.random.rand() < spot_frequency:  # Решаем, создавать ли пятно
                spot_width = np.random.randint(min_spot_width, max_spot_width)
                spot_height = np.random.randint(min_spot_height, max_spot_height)

                # Создаем вытянутое пятно помех
                for x in range(i, i + spot_height):
                    for y in range(j, j + spot_width):
                        if 0 <= x < rows and 0 <= y < cols:
                            interference[x, y] = np.random.normal(0, intensity)  # Заполняем пятно помехами

    # Применяем размытие для смягчения границ
    blurred_interference = gaussian_filter(interference, sigma=blur_sigma)

    return blurred_interference


# Создаем матрицу с радио помехами на черном фоне
black_background_interference_matrix = generate_black_background_interference()

# Отрисовка матрицы с кастомной цветовой картой
plt.imshow(black_background_interference_matrix, cmap=CMAP)
plt.title("Radio Interference with Black Background")
plt.colorbar()
plt.show()
