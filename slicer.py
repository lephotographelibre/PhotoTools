import ntpath
import argparse
import sys
import os
import os.path
from PIL import Image


# TODO transform s=V/H slicer in crop box slicer (x * y)

def main():
    # Input Parameters

    args = parse_parameters()
    print('-- Input parameters args --', str(args))

    if not os.path.isfile(args.inputimage):
        raise FileNotFoundError(args.inputimage)
        exit()

    # Prepare Data - Variables
    print("Input file = " + args.inputimage)
    # extract filename from imput file name
    filename = ntpath.basename(args.inputimage)
    index = filename.index('.')
    filename = filename[:index]
    # print(file_name)
    output_image = "out/" + filename + "_slice"
    print("Output file = " + output_image)

    # Open Input File
    im = Image.open(args.inputimage)
    print(im.format, im.size, im.mode)

    # Get size
    width = im.size[0]
    height = im.size[1]
    print("Input Image Size -- Width = ", width, "Height = ", height)

    # Resize Syntax
    # Syntax: Image.resize(size, resample=0)
    # Parameters:
    # size – The requested size in pixels, as a 2-tuple: (width, height).
    # resample – An optional resampling filter. This can be one of PIL.Image.NEAREST (use nearest neighbour),
    # PIL.Image.BILINEAR (linear interpolation), PIL.Image.BICUBIC (cubic spline interpolation), or
    # PIL.Image.LANCZOS (a high-quality downsampling filter). If omitted, or if the image has mode “1” or “P”,
    # it is set PIL.Image.NEAREST.

    # Resize to args.maxsize
    if width > height:
        print(" -- Format Landscape")
        ratio_reduction = width / args.maxsize
        new_size = (int(width / ratio_reduction), int(height / ratio_reduction))
    elif width < height:
        print(" -- Format Portrait")
        ratio_reduction = height / args.maxsize
        new_size = (int(width / ratio_reduction), int(height / ratio_reduction))
    else:
        print(" -- Format Square")
        ratio_reduction = width / args.maxsize
        new_size = (int(width / ratio_reduction), int(height / ratio_reduction))

    im = im.resize(new_size, resample=Image.Resampling.LANCZOS)

    # Get size
    width = im.size[0]
    height = im.size[1]
    print("New Image size = ", "Width = ", width, "Height = ", height)

    # im.show()

    # Crop Syntax
    # Syntax: PIL.Image.crop(box = None)
    # Parameters:
    # box – a 4-tuple defining the left, upper, right, and lower pixel coordinate.
    #      the first two numbers define the top-left coordinates of the outtake (x,y),
    #      while the last two define the right-bottom coordinates
    #
    # (top,left)
    #	+-----------------------+
    #	|                       |
    #	|                       |
    #	|                       |
    #	+-----------------------+
    #                                (right, lower)
    #
    # Return type: Image (Returns a rectangular region as (left, upper, right, lower)-tuple).
    # Return: An Image object.

    # Setting the points for cropped image
    left = 0
    top = 0
    right = int(width / args.slicenumber) - 1
    bottom = height

    box = (left, top, right, bottom)

    # Cropped image of above dimension
    # (It will not change original image)
    # im1 = im.crop((left, top, right, bottom))
    # im1 = im.crop(box)
    # im1.show()

    # save crop image
    # im1.save(output_image, 'jpeg')

    # Loop for each slice (H or V)

    if args.orientation == "V":
        print("Slice orientation = " + "vertical")
        for i in range(args.slicenumber):
            left = i * int(width / args.slicenumber)
            top = 0
            right = (i + 1) * int(width / args.slicenumber)
            bottom = height

            box = (left, top, right, bottom)
            print(box)
            im1 = im.crop(box)
            im1.save(output_image + "_" + "{:02d}".format(i) + ".jpg", 'jpeg')
            print("-- Slice created : " + output_image + "_" + "{:02d}".format(i) + ".jpg")
    else:
        print("Slice orientation= " + "Horizontal")
        for i in range(args.slicenumber):
            left = 0
            top = i * int(height / args.slicenumber)
            right = width
            bottom = (i + 1) * int(height / args.slicenumber)

            box = (left, top, right, bottom)
            print(box)
            im1 = im.crop(box)
            im1.save(output_image + "_" + "{:02d}".format(i) + ".jpg", 'jpeg')
            print("-- Slice created : " + output_image + "_" + "{:02d}".format(i) + ".jpg")


def parse_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputimage')
    # parser.add_argument('outputimage')
    # parser.add_argument('-l', '--log-level')
    parser.add_argument('--jpeg-quality', type=int, default=50)
    parser.add_argument('--maxsize', type=int, default=2000)
    # TODO crop = "3x5"
    parser.add_argument('--slicenumber', type=int, default=5)
    parser.add_argument('--orientation')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    sys.exit(main())
