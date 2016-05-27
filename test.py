#!/usr/bin/env python3
from PIL import Image
from math import sqrt, floor, sin, cos
import operator
import sys

def dot(a,b):
    return a[0]*b[0]+a[1]*b[1]

def qq(q, l):
    return floor(q/l)

def convert_to_thing(vec, loc, l):
        qw = dot(loc, vec)
        return qq(qw, l)

def main(argv):
    name = argv[0]
    lm = 64
    #vecs = ['hex', (1,(sqrt(3)/2, 1/2)),(1,(-sqrt(3)/2, 1/2)), (1,(0, 1))] # HEXAGONS
    #vecs = ['dia', (1,(sqrt(3)/2, 1/2)),(1,(-sqrt(3)/2, 1/2))] # Diamonds
    #vecs = ['pixel', (1, (1, 0)), (1, (0, 1))] # Normal
    vecs = ['pixel', (10, (1, 0)), (10, (0, 1))] # Normal
    #vecs = ['squarecross', (1,0), (1/sqrt(2), 1/sqrt(2)), (0, 1)] # SQUARE
    #ang = 45 /180 *3.14
    #vecs = ['pixang', (-sin(ang), cos(ang)),(sin(ang), cos(ang))] # DIAG
    #vecs = ['smear', (cos(ang), sin(ang))] #smear
    #vecs = ['iso', (1, (1,0)), (sqrt(2), (-1/sqrt(2), 1/sqrt(2))), (sqrt(2), (1/sqrt(2), 1/sqrt(2))), (1, (0, 1))] # isosceles
    #vecs = ['iso2', (1, (1,0)), (1/sqrt(2), (-1/sqrt(2), 1/sqrt(2))), (1/sqrt(2), (1/sqrt(2), 1/sqrt(2))), (1, (0, 1))] # square diag
    im = Image.open(name)
    im = im.convert("RGB")

    x, y = im.size

    groups = {}
    gcurr = {}

    for i in range(x):
        for j in range(y):
            loc = (i, j)
            px = im.getpixel(loc)
            v2 = []
            for v in vecs[1:]:
                l = v[0] *lm
                va = v[1]
                v2.append(convert_to_thing(va, loc, l))
            nl = tuple(v2)
            if groups.get(nl) is None:
                groups[nl] = tuple(0 for x in range(len(px)))
                gcurr[nl] = 0
            groups[nl] = tuple(groups[nl][x]+px[x]/255 for x in range(len(px)))
            gcurr[nl] += 1
    new_group = {}

    for k in groups:
        new_group[k] = tuple(int(groups[k][x]*255/gcurr[k]) for x in range(len(groups[k])))

    d = 1
    l *= d
    x = int(d*x)
    y = int(d*y)

    im2 = Image.new("RGB",(x, y))
    for i in range(x):
        for j in range(y):
            loc = (i, j)
            v2 = []
            for v in vecs[1:]:
                l = v[0] *lm
                va = v[1]
                v2.append(convert_to_thing(va, loc, l))
            nl = tuple(v2)
            col = new_group.get(nl, (127,127,127))
            im2.putpixel(loc, col)
    # DOOT
    im2.save(vecs[0] + "_" + str(lm) + "_" + name)

if __name__ == "__main__":
    main(sys.argv[1:])
