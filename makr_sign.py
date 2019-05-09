import numpy
import time
import board
import neopixel
##import matplotlib.pyplot as plt

pixel_pin = board.D18
num_pixels = 118

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


def set_pixels_from_IMAGE():
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



def rainbow_wipe( direction, delay ):
    if ( direction == "DOWN" ):
        for h in range(255):
            for j in range(NUM_ROWS):
                rw_index = int((j*255/ (NUM_ROWS*2) ) - (h*3))
                col = convert_rgb_to_int(wheel(((rw_index) & 255)))
                for i in range(NUM_ROWS):
                    IMAGE[i][j] = col

                set_pixels_from_IMAGE()
    elif ( direction == "UP" ):
        for h in range(255):
            for j in range(NUM_ROWS):
                rw_index = int((j*255/ (NUM_ROWS*2) ) + (h*3))
                col = convert_rgb_to_int(wheel(((rw_index) & 255)))
                for i in range(NUM_ROWS):
                    IMAGE[i][j] = col

                set_pixels_from_IMAGE()
    elif ( direction == "LEFT" ):
        for h in range(255):
            for j in range(NUM_ROWS):
                rw_index = int((j*255/ (NUM_ROWS*2) ) + (h*3))
                col = convert_rgb_to_int(wheel(((rw_index) & 255)))
                for i in range(NUM_ROWS):
                    IMAGE[j][i] = col

                set_pixels_from_IMAGE()
    elif ( direction == "RIGHT" ):
        for h in range(255):
            for j in range(NUM_ROWS):
                rw_index = int((j*255/ (NUM_ROWS*2) ) - (h*3))
                col = convert_rgb_to_int(wheel(((rw_index) & 255)))
                for i in range(NUM_ROWS):
                    IMAGE[j][i] = col

                set_pixels_from_IMAGE()



while True:
    
    randomize_IMAGE()
    set_pixels_from_IMAGE()
    time.sleep(0.5)
    
    set_image_border( (255,0,0) )
    set_pixels_from_IMAGE()
    time.sleep(0.5)
    
    set_image_M( (0,255,0) )
    set_pixels_from_IMAGE()
    time.sleep(0.5)
    
    set_image_A( (0,0,255) )
    set_pixels_from_IMAGE()
    time.sleep(0.5)
    
    set_image_K( (255,255,0) )
    set_pixels_from_IMAGE()
    time.sleep(0.5)
    
    set_image_R( (255,0,255) )
    set_pixels_from_IMAGE()
    time.sleep(0.5)

    rainbow_wipe( "DOWN", 0.001 )
    rainbow_wipe( "UP", 0.001 )
    rainbow_wipe( "LEFT", 0.001 )
    rainbow_wipe( "RIGHT", 0.001 )
