import ntpath
from PIL import Image

# TODO transform s=V/H slicer in crop box slicer (x * y)

# Input Parameters
max_pixel = 2000
nb_slices = 5
# TODO crop = "3x5"
slice_orientation = "H"
input_image = "images/vertical01.jpg"

# Prepare Data - Variables
print("Input file = " + input_image)
# extract filename from imput file name
filename = ntpath.basename(input_image)
index = filename.index('.')
filename = filename[:index]
# print(file_name)
output_image = "out/" + filename + "_slice"
print("Output file = " + output_image)

# Open Input File
im = Image.open(input_image)
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

# Resize to max_pixel
if width > height:
    print(" -- Format Landscape")
    ratio_reduction = width / max_pixel
    new_size = (int(width / ratio_reduction), int(height / ratio_reduction))
elif width < height:
    print(" -- Format Portrait")
    ratio_reduction = height / max_pixel
    new_size = (int(width / ratio_reduction), int(height / ratio_reduction))
else:
    print(" -- Format Square")
    ratio_reduction = width / max_pixel
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
right = int(width / nb_slices) - 1
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

if slice_orientation == "V":
    print("Slice orientation = " + "vertical")
    for i in range(nb_slices):
        left = i * int(width / nb_slices)
        top = 0
        right = (i + 1) * int(width / nb_slices)
        bottom = height

        box = (left, top, right, bottom)
        print(box)
        im1 = im.crop(box)
        im1.save(output_image + "_" + str(i) + ".jpg", 'jpeg')
        print("-- Slice created : " + output_image + "_" + str(i) + ".jpg")
else:
    print("Slice orientation= " + "Horizontal")
    for i in range(nb_slices):
        left = 0
        top = i * int(height / nb_slices)
        right = width
        bottom = (i + 1) * int(height / nb_slices)

        box = (left, top, right, bottom)
        print(box)
        im1 = im.crop(box)
        im1.save(output_image + "_" + "{:02d}".format(i) + ".jpg", 'jpeg')
#        print("-- Slice created : " + output_image + "_" + str(i) + ".jpg")
        print("-- Slice created : " + output_image + "_" + "{:02d}".format(i) + ".jpg")

print("End ...")
