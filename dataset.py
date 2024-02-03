import random
import re
from pathlib import Path

from buffer import Buffer
from target import Target

DATASET_SIZE = 5000
MAX_TARGETS_COUNT = 8
SHOW_BUFFER = False


class Dataaset:
    def __init__(self, dataset_path, size=DATASET_SIZE, max_targets=MAX_TARGETS_COUNT) -> None:
        self.size = size
        self.max_targets = max_targets

        self.create_dataset_folder(Path(dataset_path))
        self.add_classes_file()

    def fill(self):
        for i in range(self.size):
            b = Buffer()
            for _ in range(random.randint(1, self.max_targets)):
                t = Target()
                b.place_target(t)

            # b.add_random_spots()
            b.to_img(show=SHOW_BUFFER, path=self.dataset_path / f"buffer_{i}.png")

            b.gen_coords_file(self.dataset_path / f"buffer_{i}.txt")

    def create_dataset_folder(self, base_path):
        base_path.mkdir(parents=True, exist_ok=True)
        dataset_folders = [p for p in base_path.iterdir() if p.is_dir() and re.match(r"dataset_\d+", p.name)]

        if not dataset_folders:
            last_index = 0
        else:
            last_index = max([int(re.search(r"\d+", folder.name).group()) for folder in dataset_folders])

        self.dataset_path = base_path / f"dataset_{last_index + 1}"
        self.dataset_path.mkdir(parents=True, exist_ok=True)

    def add_classes_file(self):
        with open(self.dataset_path / "classes.txt", "w") as f:
            f.write(f"target 0")


if __name__ == "__main__":
    d = Dataaset("/home/d/datasets")
    d.fill()
