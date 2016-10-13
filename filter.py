#!/usr/bin/env python3
from PIL import Image
from math import sqrt, floor, sin, cos
import operator
import sys

def convert_to_shape(vector, location, length):
    position = location[0] * vector[0] + location[1] * vector[1]
    floored = floor(position / length)
    return floored

def get_pixel_group(shape, location, edge):
    group = []
    for vector in shape[1:]:
        length = vector[0] * edge
        vectorPoint = vector[1]
        group.append(convert_to_shape(vectorPoint, location, length))
    return tuple(group)

def correct_colors(colors, groupSize):
    for group in colors:
        red = int(colors[group][0] / groupSize[group])
        green = int(colors[group][1] / groupSize[group])
        blue = int(colors[group][2] / groupSize[group])
        colors[group] = (red, green, blue)
    return colors

def choose_shape(label):
    ang = 45 / 180 * 3.14
    if label == "normal":
        shape = ['pixel', (1, (1, 0)), (1, (0, 1))] # Normal
    elif label == "diamond":
        shape = ['dia', (1, (sqrt(3)/2, 1/2)),(1,(-sqrt(3)/2, 1/2))] # Diamonds
    elif label == "hexagon":
        shape = ['hex', (1, (sqrt(3)/2, 1/2)),(1,(-sqrt(3)/2, 1/2)), (1,(0, 1))] # HEXAGONS
    elif label == "pixel":
        shape = ['pixel', (1, (1, 0)), (1, (0, 1))] # Normal
    elif label == "square": 
        shape = ['squarecross', (1,0), (1/sqrt(2), 1/sqrt(2)), (0, 1)] # SQUARE
    elif label == "diagonal":
        shape = ['pixang', (1, (-sin(ang), cos(ang))),(1, (sin(ang), cos(ang)))] # DIAG
    elif label == "iso":
        shape = ['iso', (1, (1,0)), (sqrt(2), (-1/sqrt(2), 1/sqrt(2))), (sqrt(2), (1/sqrt(2), 1/sqrt(2))), (1, (0, 1))] # isosceles
    elif label == "iso2":
        shape = ['iso2', (1, (1,0)), (1/sqrt(2), (-1/sqrt(2), 1/sqrt(2))), (1/sqrt(2), (1/sqrt(2), 1/sqrt(2))), (1, (0, 1))] # square diag
    elif label == "smear":
        shape = ['smear', (cos(ang), sin(ang))] #smear
    else:
        print("Invalid argument")
        sys.exit()
    return shape

def main(argv):
    name = argv[0]
    label = argv[1]

    shape = choose_shape(label)

    sourceImage = Image.open(name)
    sourceImage = sourceImage.convert("RGB")

    width, height = sourceImage.size
    size = min(width, height)
    edge = round(size / 10)

    colors = {}
    groupSize = {}

    for x in range(width):
        for y in range(height):
            location = (x, y)
            pixel = sourceImage.getpixel(location)
            group = get_pixel_group(shape, location, edge)
            if colors.get(group) is None:
                colors[group] = (0, 0, 0)
                groupSize[group] = 0
            red = colors[group][0] + pixel[0]
            green = colors[group][1] + pixel[1]
            blue = colors[group][2] + pixel[2]
            colors[group] = (red, green, blue)
            groupSize[group] += 1

    colors = correct_colors(colors, groupSize)
    destinationImage = Image.new("RGB",(width, height))
    for x in range(width):
        for y in range(height):
            location = (x, y)
            group = get_pixel_group(shape, location, edge)
            color = colors.get(group, (127, 127, 127))
            destinationImage.putpixel(location, color)
    # DOOT
    destinationImage.save(shape[0] + "_" + str(edge) + "_" + name)

if __name__ == "__main__":
    main(sys.argv[1:])
