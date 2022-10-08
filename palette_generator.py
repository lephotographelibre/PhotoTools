# pip3 install --upgrade extcolors
# Building a color palette generator in Python
# From: https://kylermintah.medium.com/coding-a-color-palette-generator-in-python-inspired-by-procreate-5x-b10df37834ae

import sys
import math
import PIL
import extcolors  # From: https://github.com/CairX/extract-colors-py
import numpy as np
import urllib.request
import matplotlib.pyplot as plt
import webcolors


from PIL import Image, ImageDraw
from PIL import ImageFont
from matplotlib import gridspec


def main():
    # Execution cell
    # We simply need to call our study_image() function and pass in a valid image URL in our final cell.
    # image_url = 'https://tinyurl.com/unsplash-painted-flowers'
    image_url = 'https://lephotographelibre.files.wordpress.com/2018/03/port_de_l_rochelle_1024_logose.jpg'
    study_image(image_url)


# Parent function
# In our second code cell, we define our top-level function. The study_image() function will orchestrate our process.
# We will need to define each of the helper functions defined.
def study_image(image_path):
    img = fetch_image(image_path)
    # colors = extract_colors(img) # Standard rendering fonction
    # color_palette = render_color_platte(colors) # Standard rendering fonction
    colors, pixel_count = extract_colors_pixelcount(img)
    color_palette = render_color_percent(colors, pixel_count)
    overlay_palette(img, color_palette)


# Helper functions
# In our third code cell, we define our helper functions. Let’s talk about them.
#
# fetch_image(image_path), grabs our image via HTTP request, and stores it in local memory.
# extract_colors(img), extracts the most frequently appearing colors from our image up to a defined limit and based on
# a tolerance threshold. This returns an array of tuples of type ‘(color.rgb, color.count)’
# render_color_palette(colors), takes the extracted colors array and uses it to generate a grid of colors on a canvas
# that we can plot.
# overlay_palette(img, color_palette), takes the original image and rendered color palette and creates a new image
# using matplotlib.
def fetch_image(image_path):
    urllib.request.urlretrieve(image_path, "image")
    img = PIL.Image.open("image")
    return img


def extract_colors(img):
    tolerance = 32
    limit = 24
    colors, pixel_count = extcolors.extract_from_image(img, tolerance, limit)
    #    print(colors)
    print_result(colors, pixel_count)
    return colors


def extract_colors_pixelcount(img):
    # tolerance = 32
    tolerance = 16
    limit = 24  # max cell number
    colors, pixel_count = extcolors.extract_from_image(img, tolerance, limit)
    #    print(colors)
    print_result(colors, pixel_count)
    return colors, pixel_count


# from the GIT source https://github.com/CairX/extract-colors-py/blob/master/extcolors/command.py
def print_result(colors, pixel_count):
    print("Extracted colors:")
    color_count = sum([color[1] for color in colors])
    for color in colors:
        rgb = str(color[0])  # color[0] is the rgb tuples
        print(get_colour_name(color[0]))
        count = color[1]  # color[1] is the number is the color[0] pixel number
        percentage = "{:.2f}".format((float(count) / float(color_count)) * 100.0)
        print(f"{rgb:15}:{percentage:>7}% ({count})")

    print(f"\nPixels in output: {color_count} of {pixel_count}")


# Get Pixel count percentage for a current_color
def get_color_percentage(colors, current_color):
    color_count = sum([color[1] for color in colors])
    count = current_color[1]
    percentage = "{:.2f}".format((float(count) / float(color_count)) * 100.0)
    # percentage = math.trunc(float(count) / float(color_count) * 100.0)
    return percentage


# Get approminate Color Name (CSS21)
# From: https://stackoverflow.com/questions/9694165/convert-rgb-color-to-english-color-name-like-green-with-python
def get_colour_name(rgb_triplet):
    min_colours = {}
    for key, name in webcolors.CSS21_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - rgb_triplet[0]) ** 2
        gd = (g_c - rgb_triplet[1]) ** 2
        bd = (b_c - rgb_triplet[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


# the standard rendering function
def render_color_platte(colors):
    size = 100
    columns = 6
    width = int(min(len(colors), columns) * size)
    height = int((math.floor(len(colors) / columns) + 1) * size)
    result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    canvas = ImageDraw.Draw(result)
    for idx, color in enumerate(colors):
        x = int((idx % columns) * size)
        y = int(math.floor(idx / columns) * size)
        canvas.rectangle([(x, y), (x + size - 1, y + size - 1)], fill=color[0])

    return result


# the modified rendering function with % text in the palette cells
def render_color_percent(colors, pixel_count):
    size = 100
    columns = 6
    # Palette Size
    width = int(min(len(colors), columns) * size)
    height = int((math.floor(len(colors) / columns) + 1) * size)
    #
    # font = ImageFont.load_default()
    font = ImageFont.truetype("Arial.ttf", 24)  # locally store Arial.ttf font file
    # Palette Image
    result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    canvas = ImageDraw.Draw(result)
    for idx, color in enumerate(colors):
        x = int((idx % columns) * size)
        y = int(math.floor(idx / columns) * size)
        canvas.rectangle([(x, y), (x + size - 1, y + size - 1)], fill=color[0])
        # TODO Calculate and write % (If color is White - Font is Black, Inf color is Black Font is White)
        print("% = " + str(get_color_percentage(colors, color)))
        canvas.text((x + 10, y + 10), get_color_percentage(colors, color) + " %", (255, 255, 255), font=font)
    return result


def get_font_color(rgb):
    font_color = "white"
    # Parse rgb format (134, 237, 255)
    rgb = rgb[1:-1]
    rgblist = rgb.split(',')
    rgblist = list(map(int, rgblist))
    # print("Red color component= {}".format(rgblist[0]))
    # print("Green color component= {}".format(rgblist[1]))
    # print("Blue color component= {}".format(rgblist[2]))

    # Compute font_color
    OpositeColor = (0.3 * int(rgblist[0])) + (0.59 * int(rgblist[1])) + (0.11 * int(rgblist[1]))
    # print("OpositeColor = " + str(OpositeColor))
    if OpositeColor < 128:
        font_color = "white"
    else:
        font_color = "Black"
    print("Font color = " + font_color)
    return font_color

    # TODO render_color_platte(colors) with color list and percentage
    # Create a color Palette with Percentage


def overlay_palette(img, color_palette):
    nrow = 2
    ncol = 1
    f = plt.figure(figsize=(20, 30), facecolor='None', edgecolor='k', dpi=55, num=None)
    gs = gridspec.GridSpec(nrow, ncol, wspace=0.0, hspace=0.0)
    f.add_subplot(2, 1, 1)
    plt.imshow(img, interpolation='nearest')
    plt.axis('off')
    f.add_subplot(1, 2, 2)
    plt.imshow(color_palette, interpolation='nearest')
    plt.axis('off')
    plt.subplots_adjust(wspace=0, hspace=0, bottom=0)
    plt.show(block=True)


if __name__ == "__main__":
    sys.exit(main())
