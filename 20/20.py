import sys
from dataclasses import dataclass
from enum import Enum
from typing import List


class Pixel(Enum):
    """Enum of possible pixel types."""
    DARK = 0
    LIGHT = 1

    @staticmethod
    def from_char(ch):
        """Convert a character into a pixel."""
        if ch == ".":
            return Pixel.DARK
        elif ch == "#":
            return Pixel.LIGHT

    def to_int(self):
        """Convert a pixel into a number."""
        if self is Pixel.DARK:
            return 0
        elif self is Pixel.LIGHT:
            return 1


@dataclass
class Image:
    outer_space: Pixel
    interesting_pixels: List[List[Pixel]]
    width: int

    def get_alg_index(self, i, j):
        """Get the algorithm index for the pixel at Image.interesting_pixels[i][j]."""
        binary_num = 0
        power_of_two = 1
        for i_delta in (1, 0, -1):
            for j_delta in (1, 0, -1):
                try:
                    bit = self.interesting_pixels[i + i_delta][j + j_delta].to_int()
                except IndexError:
                    bit = self.outer_space.to_int()
                binary_num += bit * power_of_two
                power_of_two *= 2
        return binary_num
    
    def enhance(self, algorithm):
        """Enhance this image. Returns a new image."""
        next_outer_space = algorithm[0] if self.outer_space is Pixel.DARK else algorithm[-1]
        next_width = self.width + 2
        next_interesting_pixels = [[next_outer_space] * next_width]
        for i, pixel_row in enumerate(self.interesting_pixels):
            next_interesting_pixel_row = [next_outer_space]
            for j in range(len(pixel_row)):
                next_interesting_pixel_row.append(algorithm[self.get_alg_index(i, j)])
            next_interesting_pixel_row.append(next_outer_space)
            next_interesting_pixels.append(next_interesting_pixel_row)
        next_interesting_pixels.append([next_outer_space] * next_width)
        return Image(outer_space=next_outer_space, interesting_pixels=next_interesting_pixels, width=next_width)
    
    def count_lit(self):
        """Count the number of lit pixels in this image."""
        count = 0
        for pixel_row in self.interesting_pixels:
            for pixel in pixel_row:
                if pixel is Pixel.LIGHT:
                    count += 1
        return count


def read_input(lines):
    """Read the puzzle input."""
    algorithm = [Pixel.from_char(ch) for ch in lines[0].rstrip()]
    image_characters = [[Pixel.DARK] + [Pixel.from_char(ch) for ch in line.rstrip()] + [Pixel.DARK] for line in lines[2:]]
    image_width = len(image_characters[0])
    image_characters = [[Pixel.DARK] * image_width] + image_characters + [[Pixel.DARK] * image_width]
    return algorithm, Image(outer_space=Pixel.DARK, interesting_pixels=image_characters, width=image_width)


def main():
    """Advent of Code day 20."""
    algorithm, image = read_input(sys.stdin.readlines())
    image = image.enhance(algorithm).enhance(algorithm)
    print(image.count_lit())
    for _ in range(48):
        image = image.enhance(algorithm)
    print(image.count_lit())


main()