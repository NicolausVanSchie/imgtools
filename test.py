#!/usr/bin/env python3
from PIL import Image
from math import sqrt, floor, sin, cos
import operator
import sys

def dot(location,vec):
    return location[0]*vec[0]+location[1]*vec[1]

def convert_to_thing(vec, location, length):
    qw = dot(location, vec)
    floored = floor(qw / length)
    #print(location[0], location[1], qw, length, floored)
    return floored

def get_pixel_group(vecs, location, edge):
    group = []
    for vector in vecs[1:]:
        length = vector[0] * edge
        va = vector[1]
        group.append(convert_to_thing(va, location, length))
    return tuple(group)

def main(argv):
    name = argv[0]
    if len(argv) == 1:
        thing = "normal"
    else:
        thing = argv[1]

    ang = 45 / 180 * 3.14
    print(['pixel', (1, (1, 0)), (1, (0, 1))]) # Normal
    
    if thing == "normal":
        vecs = ['pixel', (1, (1, 0)), (1, (0, 1))] # Normal
    elif thing == "diamond":
        vecs = ['dia', (1, (sqrt(3)/2, 1/2)),(1,(-sqrt(3)/2, 1/2))] # Diamonds
    elif thing == "hexagon":
        vecs = ['hex', (1, (sqrt(3)/2, 1/2)),(1,(-sqrt(3)/2, 1/2)), (1,(0, 1))] # HEXAGONS
    elif thing == "pixel":
        vecs = ['pixel', (1, (1, 0)), (1, (0, 1))] # Normal
    elif thing == "square": 
        vecs = ['squarecross', (1,0), (1/sqrt(2), 1/sqrt(2)), (0, 1)] # SQUARE
    elif thing == "diagonal":
        vecs = ['pixang', (1, (-sin(ang), cos(ang))),(1, (sin(ang), cos(ang)))] # DIAG
    elif thing == "iso":
        vecs = ['iso', (1, (1,0)), (sqrt(2), (-1/sqrt(2), 1/sqrt(2))), (sqrt(2), (1/sqrt(2), 1/sqrt(2))), (1, (0, 1))] # isosceles
    elif thing == "iso2":
        vecs = ['iso2', (1, (1,0)), (1/sqrt(2), (-1/sqrt(2), 1/sqrt(2))), (1/sqrt(2), (1/sqrt(2), 1/sqrt(2))), (1, (0, 1))] # square diag
    elif thing == "smear":
        vecs = ['smear', (cos(ang), sin(ang))] #smear
    else:
        print("Invalid argument")
        sys.exit()
    print(vecs)
    #sys.exit()
    sourceImage = Image.open(name)
    sourceImage = sourceImage.convert("RGB")

    width, height = sourceImage.size

    size = min(width, height)
    edge = round(size / 10)

    colors = {}
    gcurr = {}

    for x in range(width):
        for y in range(height):
            location = (x, y)
            pixel = sourceImage.getpixel(location)
            group = get_pixel_group(vecs, location, edge)
            if colors.get(group) is None:
                colors[group] = tuple(0 for value in range(len(pixel)))
                gcurr[group] = 0
            colors[group] = tuple(colors[group][value]+pixel[value]/255 for value in range(len(pixel)))
            gcurr[group] += 1
    correctedColors = {}

    for k in colors:
        correctedColors[k] = tuple(int(colors[k][value]*255/gcurr[k]) for value in range(len(colors[k])))

    d = 1 #TODO: Whaaaaat is this? It multiples several things by 1.
    #length *= d
    width = int(d * width)
    height = int(d * height)

    destinationImage = Image.new("RGB",(width, height))
    for x in range(width):
        for y in range(height):
            location = (x, y)
            group = get_pixel_group(vecs, location, edge)
            #v2 = []
            #for vector in vecs[1:]:
                #length = vector[0] * edge
                #va = vector[1]
                #v2.append(convert_to_thing(va, location, length))
            #nl = tuple(v2)
            color = correctedColors.get(group, (127,127,127))
            destinationImage.putpixel(location, color)
    # DOOT
    destinationImage.save(vecs[0] + "_" + str(edge) + "_" + name)

if __name__ == "__main__":
    main(sys.argv[1:])
