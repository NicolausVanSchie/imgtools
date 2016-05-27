# imgtools
Assortment of (very hacky) scripts I have written to do things with images

## makeroll
A bash script that takes a gif, and turns it into a gif that in one animation completes a cycle. This is so many can be placed together and it will look like it is moving across the screen.

Usage: `./makeroll input.gif`

## makestaticroll
A bash script that does the same as above, but with a static image

Usage: edit settings in file and `./makestaticroll input.png`

## test.py
A script that takes an image and "converts" its pixels into a new base. For instance, turning pixels into hexels.

Example: http://imgur.com/a/lnJtH

Usage: edit file to choose base and `./test.py input.png`
