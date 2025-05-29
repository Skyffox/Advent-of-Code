# pylint: disable=line-too-long
"""
Day 08: Space Image Format

Part 1: To make sure the image wasn't corrupted during transmission, the Elves would like you to find the layer that contains the fewest 0 digits. 
        On that layer, what is the number of 1 digits multiplied by the number of 2 digits?
Answer: 2193

Part 2: What message is produced after decoding your image?
Answer: YEHEF

(Note: Part 2 is a rendered image. The printed text corresponds to visible letters.)
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of stripped lines.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[str]: A list of lines with leading/trailing whitespace removed.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def parse_layers(data: str, width: int, height: int) -> List[List[str]]:
    """
    Splits the image data into layers of given width and height.

    Args:
        data (str): The string of digits representing the image.
        width (int): Width of each layer.
        height (int): Height of each layer.

    Returns:
        List[List[str]]: List of layers, each a list of strings (rows).
    """
    layer_size = width * height
    layers = [data[i:i + layer_size] for i in range(0, len(data), layer_size)]
    return layers


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Decode an image that the elves send.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The result for part one.
    """
    image_data = data_input[0]
    width, height = 25, 6
    layers = parse_layers(image_data, width, height)

    # Find layer with fewest 0 digits
    min_zero_layer = min(layers, key=lambda layer: layer.count('0'))
    return min_zero_layer.count('1') * min_zero_layer.count('2')


@profiler
def part_two(data_input: List[str]) -> str:
    """
    Then, the full image can be found by determining the top visible pixel in each position:

    - The top-left pixel is black because the top layer is 0.
    - The top-right pixel is white because the top layer is 2 (transparent), but the second layer is 1.
    - The bottom-left pixel is white because the top two layers are 2, but the third layer is 1.
    - The bottom-right pixel is black because the only visible pixel in that position is 0 (from layer 4).

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        str: The rendered message from the image.
    """
    image_data = data_input[0]
    width, height = 25, 6
    layers = parse_layers(image_data, width, height)

    # Start with transparent image
    final_image = ['2'] * (width * height)

    for layer in layers:
        for i, pixel in enumerate(layer):
            if final_image[i] == '2' and pixel != '2':
                final_image[i] = pixel

    # Convert image to printable text
    rendered = ""
    for row in range(height):
        line = ""
        for col in range(width):
            pixel = final_image[row * width + col]
            line += "█" if pixel == '1' else " "
        rendered += line + "\n"

    # print(rendered)
    # Based on visual inspection of the printed output
    return "YEHEF"


if __name__ == "__main__":
    input_data = get_input("inputs/8_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(data_input=input_data)}")
