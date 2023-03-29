import time
import sys
from pathlib import Path


def read_snes_image(file_path):
    # Read data from file and return as bytearray.
    with open(file_path, 'rb') as f:
        snes_data = f.read()

    return snes_data


def process_snes_to_rgba(snes_data):
    rgba_pixel_array = []

    # Convert byte pairs in SNES data to two pixels according to reverse of previous code logic.
    for i in range(0, len(snes_data), 2):
        byte_pair = snes_data[i:i + 2]
        for bit_pos in range(7, -1, -1):
            pixel_1 = ((byte_pair[0] >> bit_pos) & 1) | (((byte_pair[1] >> bit_pos) & 1) << 1)
            rgba_pixel_array.append((pixel_1 * 85, pixel_1 * 85, pixel_1 * 85, 255))

    return rgba_pixel_array


def save_rgba_image(rgba_pixel_array, file_path, width, height):
    # Save RGBA pixel array to file.
    from PIL import Image
    image = Image.new('RGBA', (width, height))
    image.putdata(rgba_pixel_array)
    image.save(file_path)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: snes_tile_to_image.py <input_file> <output_file> <width>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    width = int(sys.argv[3])

    snes_data = read_snes_image(input_file)
    rgba_pixel_array = process_snes_to_rgba(snes_data)

    # Calculate height based on the width and the number of pixels.
    height = len(rgba_pixel_array) // width

    save_rgba_image(rgba_pixel_array, output_file, width, height)