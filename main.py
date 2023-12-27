import os
import random

from buffer import Buffer
from target import Target

DATASETS_PATH = "/home/user/datasets"


def write_coords_to_file(coords, filename):
    with open(filename, "a") as f:
        f.write(f"0 {coords[0]} {coords[1]} {coords[2]} {coords[3]}\n")



# Main function
def main():
    # Create a buffer
    buffer = Buffer()

    # Generate and place 3 to 6 targets
    os.remove("out/output.txt")
    for _ in range(random.randint(10, 30)):
        t = Target()
        buffer.place_target(t)
    print(buffer.targets)

    with open("out/classes.txt", "w") as f:
        f.write(f"target 0")

    buffer.to_img(show=True, path="out/output.png")


if __name__ == "__main__":
    main()
