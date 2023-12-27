import random

import numpy as np

from buffer_gen import Buffer
from target_gen import Target


def gen_pytorch_coords(min_x, min_y, max_x, max_y, buffer_height, buffer_width):
    # Generate PyTorch-style coordinates
    center_x = (min_x + max_x) / 2 / buffer_width
    center_y = (min_y + max_y) / 2 / buffer_height
    target_width = (max_x - min_x) / buffer_width
    target_height = (max_y - min_y) / buffer_height
    return center_x, center_y, target_width, target_height


# Function to place a target onto the buffer
def place_target_on_buffer(buffer, target, x, y):
    target_matrix = target._matrix
    buffer_matrix = buffer._matrix
    th, tw = target_matrix.shape
    bh, bw = buffer_matrix.shape

    # Calculate the region where the target will be placed
    x_start = max(0, x - tw // 2)
    x_end = min(bw, x + tw // 2)
    y_start = max(0, y - th // 2)
    y_end = min(bh, y + th // 2)

    # Place the target onto the buffer
    buffer_matrix[y_start:y_end, x_start:x_end] = np.maximum(
        buffer_matrix[y_start:y_end, x_start:x_end], target_matrix[: y_end - y_start, : x_end - x_start]
    )


def write_coords_to_file(coords, filename):
    with open(filename, "a") as f:
        f.write(f"0 {coords[0]} {coords[1]} {coords[2]} {coords[3]}\n")


# Main function
def main():
    # Create a buffer
    buffer = Buffer()

    # Generate and place 3 to 6 targets
    for _ in range(random.randint(10, 30)):
        target = Target()
        # Randomly choose a position to place the target
        x = random.randint(0, buffer.width)
        y = random.randint(0, buffer.height)
        pt_coords = gen_pytorch_coords(
            min_x=x,
            min_y=y,
            max_x=x + target.area_width,
            max_y=y + target.area_height,
            buffer_height=buffer.height,
            buffer_width=buffer.width,
        )

        place_target_on_buffer(buffer, target, x, y)
        write_coords_to_file(coords=pt_coords, filename="out/output.txt")

    with open("out/classes.txt", "w") as f:
        f.write(f"target 0")

    buffer.to_img(show=True, path="out/output.png")


if __name__ == "__main__":
    main()
