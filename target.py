import random

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

from utils import CMAP


class Target:
    def __init__(
        self,
        area_width: int = None,
        area_height: int = None,
        target_width: int = None,
        target_height: int = None,
        curvature: int = None,
        noise: int = None,
        blur: int = None,
    ) -> None:
        self.area_width = area_width or random.randint(60, 110)
        self.area_height = area_height or int(self.area_width // 6 * 1.05)
        self.target_width = target_width or int(self.area_width / 5 * random.uniform(2.5, 4))
        self.target_height = target_height or int(self.target_width / 22 * random.uniform(0.8, 1))
        self.curvature = curvature or random.uniform(0.01, 0.03)
        self.noise = noise or random.uniform(0.01, 0.04)
        self.blur = blur or random.randint(3, 6)

        self._matrix = self._gen_matrix()

    def __repr__(self) -> str:
        return f"Target(area_width={self.area_width}, area_height={self.area_height}, target_width={self.target_width}, target_height={self.target_height}, curvature={self.curvature}, noise={self.noise}, blur={self.blur})"

    def _gen_matrix(self):
        matrix = np.zeros((self.area_height, self.area_width))
        center_x = self.area_width // 2
        center_y = self.area_height // 2

        for i in range(self.area_width):
            for j in range(self.area_height):
                if ((i - center_x) / self.target_width) ** 2 + ((j - center_y) / self.target_height) ** 2 <= 1:
                    distance_to_center = np.sqrt((i - center_x) ** 2 + (j - center_y) ** 2)
                    gradient_value = 1.0 - np.clip(
                        distance_to_center / max(self.target_width, self.target_height), 0, 1
                    )  # Normalize to [0, 1] and invert

                    # Introduce random noise within the ellipse region
                    noise = np.random.normal(0, self.noise)

                    # Introduce random curvature
                    curvature = 1 + self.curvature * np.random.normal(0, 1)

                    gradient_value = gradient_value * (1 - self.noise) + noise
                    gradient_value *= curvature

                    matrix[j, i] = gradient_value

        # Apply Gaussian blur to make the edges more blurred
        matrix = gaussian_filter(matrix, sigma=self.blur)  # 6 - 18

        return matrix

    def to_img(self, show: bool = False, path: str = None):
        plt.imshow(self._matrix, cmap=CMAP)
        plt.axis("off")
        if path:
            plt.savefig(path, bbox_inches="tight", pad_inches=0.0)
        if show:
            plt.show()
        plt.close()


if __name__ == "__main__":
    for i in range(10):
        t = Target()
        t.to_img(show=True)
        print(i, t)
