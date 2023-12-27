import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, Normalize

WIDTH = 2048
HEIGHT = 1200

norm = Normalize(-1, 1)
CMAP = LinearSegmentedColormap.from_list("", [[norm(-1.0), "0"], [norm(1.0), "yellow"]])  # black


class Buffer:
    def __init__(self, width: int = WIDTH, height: int = HEIGHT) -> None:
        self.width = width
        self.height = height
        self._matrix = self._gen_empty()

    def _gen_empty(self):
        return np.zeros((self.height, self.width))

    def to_img(self, show: bool = False, path: str = None):
        plt.imshow(self._matrix, cmap=CMAP)
        plt.axis("off")
        if path:
            plt.savefig(path, bbox_inches="tight", pad_inches=0.0)
        if show:
            plt.show()
        plt.close()

if __name__ == "__main__":
    b = Buffer()
    b.to_img(show=True)
