import numpy
import time
import board
import neopixel
import random
import noise
import math
import PIL.Image
from tkinter import *

USE_VIZ_CANVAS =False
COLOR_MODE = "RAINBOW" #"LOGO"
ANIM_MODE = "RIPPLE" #"PERLIN" "RIPPLE"

im = PIL.Image.open('images/uw.jpg')
imw, imh = im.size
im_vals = list(im.getdata())
im_array = numpy.array(im)
#im_array[imw, imh]
#print(im_vals)

pixel_pin = board.D18
num_pixels = 118
ripple_ctr = 0
ORDER = neopixel.GRB
CHASE_INTERVAL = 0.05
RAINBOW_INTERVAL = 0.01

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1.0, auto_write=False, pixel_order=ORDER)

NUM_ROWS = 15

##IMAGE = numpy.zeros( (NUM_ROWS,NUM_ROWS) )
IMAGE = [[ numpy.random.randint(0,16777215) for x in range(NUM_ROWS) ] for y in range(NUM_ROWS) ]
IMAGE[0][0] = 16777215

r = 12
g = 100
b = 25
bgrVal = (b << 16) + (g << 8) + r

IMAGE[4][0] = bgrVal


top = Tk()
top.title("makr canvas")

canvas = Canvas(top, bg="black", height=300, width=300)
canvas.pack()

canvas_pixels = [[ canvas.create_rectangle(x*20,y*20, (x*20)+20, (y*20)+20, fill="red") for y in range(NUM_ROWS) ] for x in range(NUM_ROWS) ]



BLUE_MASK = 0xFF0000
GREEN_MASK = 0xFF00
RED_MASK = 0XFF

RED = (0, 100, 0)
pixels.fill(RED)
pixels.show()
time.sleep(1)

PIXEL_MAPPING = [
    (0,0), ## 0
    (1,0), ## 1
    (2,0), ## 2
    (3,0),
    (4,0),
    (5,0),
    (6,0),
    (7,0),
    (8,0),
    (9,0),
    (10,0), ## 10
    (11,0),
    (12,0),
    (13,0),
    (14,0), ## 14, top right corner
    (14,1),
    (14,2),
    (14,3),
    (14,4),
    (14,5),
    (14,6),
    (14,7),
    (14,8),
    (14,9),
    (14,10),
    (14,11),
    (14,12),
    (14,13),
    (14,14), ## 28 bottom right corner
    (13,14),
    (12,14),
    (11,14),
    (10,14),
    (9,14),
    (8,14),
    (7,14),
    (6,14),
    (5,14),
    (4,14),
    (3,14),
    (2,14),
    (1,14),
    (0,14), ## 42 bottom left
    (0,13),
    (0,12),
    (0,11),
    (0,10),
    (0,9),
    (0,8),
    (0,7),
    (0,6),
    (0,5),
    (0,4),
    (0,3),
    (0,2),
    (0,1),  ## 55 end of square

    (2,2), ## 56 top left of M
    (2,3),
    (2,4),
    (2,5),
    (2,6), ## 60 bot left of M
    (3,6),
    (4,6),
    (5,6),
    (5,5),
    (4,4),
    (3,3),
    (5,3),
    (6,2),
    (6,3),
    (6,4),
    (6,5),
    (6,6), ## 72 bot right of M

    (8,6), ## 73 bot left of A
    (8,5), ## 74, 8.5, 5
    (9,4),
    (9,3), ## 76, 9.5, 3
    (10,2), ## top of A
    (10,3), ## 78, 10.5,3
    (11,4),
    (11,5), ## 80, 11.5,5
    (12,6), ## bot right of A
    (11,6),
    (10,6),
    (9,6), ## 84, end of A

    (8,8), ## 85, top left of R
    (9,8),
    (10,8),
    (11,8),
    (12,8), ## 89 top rt of R
    (12,9),
    (12,10),
    (11,10),
    (12,12), ## 93 bot rt of R
    (11,11),
    (10,10),
    (9,9),
    (8,9),
    (8,10),
    (8,11),
    (8,12), ## 100 bot left of R

    (6,12), ## 101 bot rt of K
    (5,12),
    (4,12),
    (3,12),
    (2,12), ## 105 bot left of K
    (2,11),
    (2,10),
    (2,9),
    (2,8), ## 109 top left of K
    (3,8),
    (4,8),
    (5,8),
    (6,8), ## 113 top rt of K
    (5,9),
    (4,10),
    (3,11),
    (5,11)  ## 117 end
    ]


for i in range(len(PIXEL_MAPPING)):
    canvas.create_oval( (PIXEL_MAPPING[i][0] * 20)+5, (PIXEL_MAPPING[i][1] * 20)+5, (PIXEL_MAPPING[i][0] * 20) + 10, (PIXEL_MAPPING[i][1] * 20) + 10)


def convert_int_to_rgb(col):
    b = (col & BLUE_MASK) >> 16
    r = (col & RED_MASK)
    g = (col & GREEN_MASK) >> 8
    if ORDER == neopixel.RGB:
        return (r, g, b)
    elif ORDER == neopixel.GRB:
        return (g,r,b)
    else:
        return (r, g, b, 0)


def convert_rgb_to_int(coltup):
    r = coltup[0]
    g = coltup[1]
    b = coltup[2]
    bgrVal = (b << 16) + (g << 8) + r
    return bgrVal

def convert_int_to_hex(col):
    b = (col & BLUE_MASK) >> 16
    r = (col & RED_MASK)
    g = (col & GREEN_MASK) >> 8
    bhex = '{:02x}'.format(b)
    rhex = '{:02x}'.format(r)
    ghex = '{:02x}'.format(g)
    return "#" + rhex + ghex + bhex

def update_canvas():
    for j in range(NUM_ROWS):
        for i in range(NUM_ROWS):
            hexstr = convert_int_to_hex( IMAGE[i][j] )
            canvas.itemconfig( canvas_pixels[i][j], fill=hexstr )
    top.update_idletasks()
    top.update()

def set_pixels_from_IMAGE():
    if (USE_VIZ_CANVAS):
        update_canvas()
    for i in range(len(PIXEL_MAPPING)):
        col = int(IMAGE[ PIXEL_MAPPING[i][0] ][ PIXEL_MAPPING[i][1] ])
        newcol = convert_int_to_rgb(col)
        pixels[i] = newcol

    pixels.show()


def randomize_IMAGE():
    for i in range(NUM_ROWS):
        for j in range(NUM_ROWS):
            IMAGE[i][j] = numpy.random.randint(0,16777215)

def set_image_border(color):
    for i in range(0,56):
        IMAGE[ PIXEL_MAPPING[i][0] ][ PIXEL_MAPPING[i][1] ] = convert_rgb_to_int(color)

def set_image_M(color):
    for i in range(56,73):
        IMAGE[ PIXEL_MAPPING[i][0] ][ PIXEL_MAPPING[i][1] ] = convert_rgb_to_int(color)

def set_image_A(color):
    for i in range(73,85):
        IMAGE[ PIXEL_MAPPING[i][0] ][ PIXEL_MAPPING[i][1] ] = convert_rgb_to_int(color)

def set_image_K(color):
    for i in range(101,118):
        IMAGE[ PIXEL_MAPPING[i][0] ][ PIXEL_MAPPING[i][1] ] = convert_rgb_to_int(color)

def set_image_R(color):
    for i in range(85,101):
        IMAGE[ PIXEL_MAPPING[i][0] ][ PIXEL_MAPPING[i][1] ] = convert_rgb_to_int(color)


def wheel(pos):
    # Input 0-255 to get color value
    # colors are transition r-g-b and back to r
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)

def linear_rainbow(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 128:
        r = int( 255 - pos*2 )
        g = int( pos*2 )
        b = 0
    else:
        pos -= 128
        r = 0
        g = int( 255 - pos*2 )
        b = int( pos * 2 )
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


def rainbow_wipe( direction, width = 0.5, speed = 0.3 ):
    ## width is how much of a full rainbow shows at a time, 0.5
    hmult = 1
    if ( direction == "DOWN" or direction == "RIGHT" ):
        hmult = -1

    for h in range(25):
        for j in range(NUM_ROWS):
            rw_index = int((j*255/ (NUM_ROWS/width) ) + hmult*(h/speed))
            col = convert_rgb_to_int(wheel(((rw_index) & 255)))
            for i in range(NUM_ROWS):
                if ( direction == "UP" or direction == "DOWN" ):
                    IMAGE[i][j] = col
                else:
                    IMAGE[j][i] = col
            set_pixels_from_IMAGE()



def perlin(x,y,seed=0):
    #permutation table
    numpy.random.seed(seed)
    p = numpy.arange(256,dtype=int)
    numpy.random.shuffle(p)
    p = numpy.stack([p,p]).flatten()
    #coords of top-left
    xi = x.astype(int)
    yi = y.astype(int)
    # internal coords
    xf = x - xi
    yf = y - yi
    # fade factors
    u = fade(xf)
    v = fade(yf)
    # noise components
    n00 = gradient( p[p[xi]+yi], xf, yf )
    n01 = gradient( p[p[xi]+yi+1], xf, yf-1 )
    n11 = gradient( p[p[xi+1]+yi+1], xf-1, yf-1 )
    n10 = gradient( p[p[xi+1]+yi], xf-1, yf )
    # combine noises
    x1 = lerp( n00, n10, u)
    x2 = lerp( n01, n11, u)
    return lerp(x1, x2, v)

def lerp(a,b,x):
    #linear interpolation
    return a + x * (b-a)

def fade(t):
    return (6 * t**5) - (15 * t**4) + (10 * t**3)

def gradient(h,x,y):
    # gradient converts h to the right gradient vector and return the dot product with (x,y)
    vectors = numpy.array([[0,1],[0,-1],[1,0],[-1,0]])
    g = vectors[h%4]
    return g[:,:,0] * x + g[:,:,1] * y

def visualize_perlin(p):
    for j in range(NUM_ROWS):
        for i in range(NUM_ROWS):
            a = p[i][j]
            a += 0.5
            a = numpy.clip(a,0,1)
            a *= 255
            ahex = '{:02x}'.format(int(a))
            if ( ahex == "-1" ):
                print(i, j, a)
            hexstr = "#"+ahex+ahex+ahex
            canvas.itemconfig( canvas_pixels[i][j], fill=hexstr )
    top.update_idletasks()
    top.update()


def vis_perlin_lib(z):
    for j in range(NUM_ROWS):
        for i in range(NUM_ROWS):
            x = i / 8
            y = j / 8
            a = noise.snoise3(x,y, z)
            a *= 127
            a += 128
            ahex = '{:02x}'.format(int(a))
            if ( ahex == "-1" ):
                print(i, j, a)
            #hexstr = "#"+ahex+ahex+ahex

            col = convert_rgb_to_int(wheel(a))
            IMAGE[i][j] = col

            #canvas.itemconfig( canvas_pixels[i][j], fill=hexstr )
    #top.update_idletasks()
    #top.update()

def viz_perlin_logo(z):
    for j in range(NUM_ROWS):
        for i in range(NUM_ROWS):
            x = i / 2
            y = j / 2
            a = noise.snoise3(x,y, z)
            ## use 225 for a 15x15 image
            a *= 112
            a += 113
            ahex = '{:02x}'.format(int(a))
            if ( ahex == "-1" ):
                print(i, j, a)
            #hexstr = "#"+ahex+ahex+ahex

            col = convert_rgb_to_int(im_vals[int(a)])
            IMAGE[i][j] = col

def viz_image(arr):
    for i in range(NUM_ROWS):
        for j in range(NUM_ROWS):
            col = convert_rgb_to_int(arr[j][i])
            IMAGE[i][j] = col

##lin = numpy.linspace(0,5,15,endpoint=False)
##x,y = numpy.meshgrid(lin,lin)
##xoffset = 0
##yoffset = 0
##seednum = 0
##perl = perlin(x,y,seed=seednum)
##visualize_perlin(perl)

def vis_ripple():
    #current_millis = int(round(time.time() * 100000))
    for i in range(NUM_ROWS):
        for j in range(NUM_ROWS):
            d = math.hypot( i-7, j-7 )
            num = math.floor( (math.sin(d/2-(ripple_ctr/128))*128) + 128 )
            col = convert_rgb_to_int(linear_rainbow(num))
            #col = convert_rgb_to_int((num,num,num))
            IMAGE[i][j] = col

zinc = 0

##viz_image(im_array)
set_pixels_from_IMAGE()

while True:
##    time.sleep(0.5)
##    perl = perlin(x+xoffset,y+yoffset,seed=seednum)
##    visualize_perlin(perl)
##    xoffset += random.uniform(-0.5,0.5)
##    yoffset += random.uniform(-0.5,0.5)


##    viz_perlin_logo(zinc)
##    set_pixels_from_IMAGE()
##    zinc += 0.02
    if ANIM_MODE == "PERLIN":
        vis_perlin_lib(zinc)
        set_pixels_from_IMAGE()
        zinc += 0.02
    elif ANIM_MODE == "RIPPLE":
        vis_ripple()
        set_pixels_from_IMAGE()
        ripple_ctr += 20


    #seednum += 1
##
##    randomize_IMAGE()
##    set_pixels_from_IMAGE()
##    time.sleep(0.5)
##
##    set_image_border( (255,0,0) )
##    set_pixels_from_IMAGE()
##    time.sleep(0.5)
##
##    set_image_M( (0,255,0) )
##    set_pixels_from_IMAGE()
##    time.sleep(0.5)
##
##    set_image_A( (0,0,255) )
##    set_pixels_from_IMAGE()
##    time.sleep(0.5)
##
##    set_image_K( (255,255,0) )
##    set_pixels_from_IMAGE()
##    time.sleep(0.5)
##
##    set_image_R( (255,0,255) )
##    set_pixels_from_IMAGE()
##    time.sleep(0.5)
##
##    rainbow_wipe( "DOWN", 0.5, 0.3 )
##    rainbow_wipe( "UP", 1, 1 )
##    rainbow_wipe( "LEFT", 2, 0.1 )
##    rainbow_wipe( "RIGHT" )
