import numpy
import time
import board
import neopixel

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
    (0,1)
    ]


def convert_int_to_rgb(col):
    b = (col & BLUE_MASK) >> 16
    r = (col & RED_MASK)
    g = (col & GREEN_MASK) >> 8
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0) 



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
    
while True:
    randomize_IMAGE()
    set_pixels_from_IMAGE()
    time.sleep(0.5)


##print(IMAGE[2][0])
##print(PIXEL_MAPPING[1])
##
##print( IMAGE[ PIXEL_MAPPING[1][0] ][ PIXEL_MAPPING[1][1] ] )
##
##col = int(IMAGE[ PIXEL_MAPPING[1][0] ][ PIXEL_MAPPING[1][1] ])
##
##print("blue:")
##print(( (col & BLUE_MASK) >> 16 ) )
##print("red:")
##print( ( (col & RED_MASK) ) )
##print("GREEN:")
##print(( (col & GREEN_MASK) >> 8 ) )
##
##print(IMAGE[4][0])
##print(PIXEL_MAPPING[2])
##
##print( IMAGE[ PIXEL_MAPPING[2][0] ][ PIXEL_MAPPING[2][1] ] )
##
##col = int(IMAGE[ PIXEL_MAPPING[2][0] ][ PIXEL_MAPPING[2][1] ])
##
##print("blue:")
##print(( (col & BLUE_MASK) >> 16 ) )
##print("red:")
##print( ( (col & RED_MASK) ) )
##print("GREEN:")
##print(( (col & GREEN_MASK) >> 8 ) )
