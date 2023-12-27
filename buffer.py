import random
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, Normalize
from scipy.ndimage import gaussian_filter

from target import Target

WIDTH = 2048
HEIGHT = 1200

norm = Normalize(-1, 1)
CMAP = LinearSegmentedColormap.from_list("", [[norm(-1.0), "0"], [norm(1.0), "yellow"]])  # black


@dataclass
class Coord:
    center_x: int
    center_y: int
    target_w: int
    target_h: int


@dataclass
class BufferTarget:
    target: Target
    coord: Coord


class Buffer:
    def __init__(self, width: int = WIDTH, height: int = HEIGHT) -> None:
        self.width = width
        self.height = height
        self._matrix = self._gen_empty()
        self.targets: list[BufferTarget] = []

    def _gen_empty(self):
        return np.zeros((self.height, self.width))

    def place_target(self, target: Target):
        x = random.randint(0, self.width)
        y = random.randint(0, self.height)

        self._place_target_on_buffer(x, y, target)
        coord = self.gen_coord(x, y, target)
        self.targets.append(BufferTarget(target, coord))

    def _place_target_on_buffer(self, x, y, target):
        target_matrix = target._matrix
        th, tw = target_matrix.shape
        bh, bw = self._matrix.shape

        # Calculate the region where the target will be placed
        x_start = max(0, x - tw // 2)
        x_end = min(bw, x + tw // 2)
        y_start = max(0, y - th // 2)
        y_end = min(bh, y + th // 2)

        # Place the target onto the buffer
        self._matrix[y_start:y_end, x_start:x_end] = np.maximum(
            self._matrix[y_start:y_end, x_start:x_end], target_matrix[: y_end - y_start, : x_end - x_start]
        )

    def gen_coord(self, x, y, target):
        center_x = x / self.width
        center_y = y / self.height

        target_width = target.area_width / self.width
        target_height = target.area_height / self.height

        return Coord(center_x, center_y, target_width, target_height)

    def to_img(self, show: bool = False, path: str = None):
        plt.imshow(self._matrix, cmap=CMAP)
        plt.axis("off")
        if path:
            plt.savefig(path, bbox_inches="tight", pad_inches=0.0)
        if show:
            plt.show()
        plt.close()

    def gen_coords_file(self, path):
        with open(path, "w") as f:
            for target in self.targets:
                f.write(
                    f"0 {target.coord.center_x} {target.coord.center_y} {target.coord.target_w} {target.coord.target_h}\n"
                )

    def add_random_spots(self, num_spots=1, max_size=200, max_intensity=0.6):
        bh, bw = self._matrix.shape

        for _ in range(num_spots):
            # Random position and size
            center_x = random.randint(0, bw)
            center_y = random.randint(0, bh)
            # size = random.randint(1, max_size)
            size = max_size

            # Create a spot using a Gaussian blob
            spot = np.zeros((bh, bw))
            spot[center_y, center_x] = np.random.uniform(0, max_intensity)

            # Apply Gaussian filter to create a smooth spot
            spot = gaussian_filter(spot, sigma=size)

            # Add the spot to the buffer
            self._matrix = np.maximum(self._matrix, spot)


if __name__ == "__main__":
    b = Buffer()
    b.to_img(show=True)
