#!/usr/bin/python
import argparse
import json
import shutil
from typing import Tuple, List

import requests
from PIL import Image
from colr import color

from requests import Response

SHIBA_API = 'http://shibe.online/api/shibes'
API_COUNT_ARG = '?count='


def get_img_size(arg_width: int = 0, arg_height: int = 0) -> Tuple[int, int]:
    """
    Returns (width, height) tuple of console image. If arg width or height were passed in, use that.
    Otherwise, use the size of the console window.
    :param arg_width: width argument passed in, pixels
    :param arg_height: height argument passed in, pixels
    :return: tuple of ints (width, height)
    """
    term_size = shutil.get_terminal_size()
    return arg_width or term_size.columns, arg_height or term_size.lines


def get_shiba_address(shiba_count: int = 1) -> List[str]:
    """
    Have to go to the learn the home address(es) of our shiba(s).
    Calls shiba.online API, gets URL(s) to shibas, returns it as an array.
    :param shiba_count: number of shiba url's wanted
    :return: list of urls of shiba pics
    """
    shiba_content = requests.get(f'{SHIBA_API}{API_COUNT_ARG}{shiba_count}').content
    shibarray = json.loads(shiba_content)
    return shibarray


def summon_molten_shiba(shiba_url: str) -> Response:
    """
    Downloads the shiba from the shiba_url as raw data.
    :param shiba_url: A single image url of a shiba
    :return: raw image data
    """
    summon = requests.get(shiba_url, stream=True)
    raw_shiba_juice = summon.raw
    raw_shiba_juice.decode_content = True
    return raw_shiba_juice


def open_shiba(raw_image: Response, output_size: Tuple[int, int]) -> Image:
    """
    Opens raw image file w/ pillow, resizes it, and returns the image object
    :param raw_image: raw image
    :param output_size: Tuple of image size (width, height), like (128, 128).
    :return: pillow image
    """
    img = Image.open(raw_image)
    img.thumbnail((output_size))
    return img.getdata()


def spit_out_shiba(shiba_image: Image, invert: bool = False):
    """
    Prints out shiba - gets pixel color of image, prints a char with that color, jumps to new line if width index hit.
    :param shiba_image: pillow image object
    :param invert: if true, invert the colors of every pixel
    """
    width, height = shiba_image.size
    [
        print(color(' ', fore=pinv if invert else pixel, back=pinv if invert else pixel), end='\n' if (index + 1) % width == 0 else '')
        for index, pixel in enumerate(shiba_image) if (pinv:= (abs(pixel[0] - 255), abs(pixel[1] - 255), abs(pixel[2] - 255)))
    ]


def loop_all_shibas(output_size: Tuple[int, int], shiba_count: int = 1, invert: bool = False):
    """
    Main shiba summoning func.
    :param output_size: Tuple of image size (width, height), like (128, 128).
    :param shiba_count: count of shibas needed
    """
    if shiba_count < 1 or shiba_count > 100:
        print(f"Shiba count must be between 1 to 100. Got {shiba_count}.")
        quit()
    urls = get_shiba_address(shiba_count)
    for shibaddress in urls:
        raw_shiba = summon_molten_shiba(shibaddress)
        shibimage = open_shiba(raw_shiba, output_size)
        spit_out_shiba(shibimage, invert)
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', '-c', type=int, help='Count of shibas to display: 1-100. (Default 1)', default=1)
    parser.add_argument('--height', type=int, help='Height of shiba to output. (Defaults to console size)')
    parser.add_argument('--width', type=int, help='Width shiba to output. (Defaults to console size)')
    parser.add_argument('--invert', '-i', action='store_true', help='If passed, invert the output colors.')

    pargs = parser.parse_args()
    arg_width = pargs.width if pargs.width else 0
    args_height = pargs.height if pargs.height else 0
    img_size = get_img_size(arg_width, args_height)
    loop_all_shibas(img_size, pargs.count, pargs.invert)
