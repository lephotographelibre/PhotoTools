# pip3 install --upgrade extcolors
# Building a color palette generator in Python
# From: https://kylermintah.medium.com/coding-a-color-palette-generator-in-python-inspired-by-procreate-5x-b10df37834ae

import math
import PIL
import extcolors  # From: https://github.com/CairX/extract-colors-py
import numpy as np
import urllib.request
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from matplotlib import gridspec


# Parent function
# In our second code cell, we define our top-level function. The study_image() function will orchestrate our process.
# We will need to define each of the helper functions defined.
def study_image(image_path):
    img = fetch_image(image_path)
    colors = extract_colors(img)
    color_palette = render_color_platte(colors)
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


# from the GIT source https://github.com/CairX/extract-colors-py/blob/master/extcolors/command.py
def print_result(colors, pixel_count):
    print("Extracted colors:")
    color_count = sum([color[1] for color in colors])
    for color in colors:
        rgb = str(color[0])
        count = color[1]
        percentage = "{:.2f}".format((float(count) / float(color_count)) * 100.0)
        print(f"{rgb:15}:{percentage:>7}% ({count})")

    print(f"\nPixels in output: {color_count} of {pixel_count}")


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


# Execution cell
# We simply need to call our study_image() function and pass in a valid image URL in our final cell.
# image_url = 'https://tinyurl.com/unsplash-painted-flowers'
image_url = 'https://lephotographelibre.files.wordpress.com/2018/03/port_de_l_rochelle_1024_logose.jpg'
study_image(image_url)
