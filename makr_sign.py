import numpy
import time
import board
import neopixel
import random
import noise
import math
import RPi.GPIO as GPIO
import PIL.Image
from tkinter import *

USE_VIZ_CANVAS = False
COLOR_MODE = "LOGO" #"LOGO" "RAINBOW"
ANIM_MODE = "PERLIN" #"PERLIN" "RIPPLE"


## ALL BCM NUMBERS
LED_PIN_RED1 = 26
LED_PIN_RED2 = 13
POT_PIN = 6
LED_PIN_BLUE = 5
LED_PIN_GREEN = 22
LED_PIN_YELLOW = 27
LED_PIN_WHITE = 17

BUTTON_PIN_1 = 16
BUTTON_PIN_2 = 12
BUTTON_PIN_3 = 25
BUTTON_PIN_4 = 24
BUTTON_PIN_5 = 23
BUTTON_PIN_6 = 4

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN_RED1,GPIO.OUT)
GPIO.setup(LED_PIN_RED2,GPIO.OUT)
GPIO.setup(LED_PIN_BLUE,GPIO.OUT)
GPIO.setup(LED_PIN_GREEN,GPIO.OUT)
GPIO.setup(LED_PIN_YELLOW,GPIO.OUT)
GPIO.setup(LED_PIN_WHITE,GPIO.OUT)


GPIO.setup(POT_PIN, GPIO.IN)
GPIO.setup(BUTTON_PIN_1, GPIO.IN)
GPIO.setup(BUTTON_PIN_2, GPIO.IN)
GPIO.setup(BUTTON_PIN_3, GPIO.IN)
GPIO.setup(BUTTON_PIN_4, GPIO.IN)
GPIO.setup(BUTTON_PIN_5, GPIO.IN)
GPIO.setup(BUTTON_PIN_6, GPIO.IN)



im = PIL.Image.open('images/uw.jpg')
imw, imh = im.size
im_vals = list(im.getdata())
im_array = numpy.array(im)
#im_array[imw, imh]
#print(im_vals)

pixel_pin = board.D18
num_pixels = 19
ripple_ctr = 0
ORDER = neopixel.GRB
CHASE_INTERVAL = 0.05
RAINBOW_INTERVAL = 0.01

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1.0, auto_write=False, pixel_order=ORDER)

NUM_ROWS = 5

##IMAGE = numpy.zeros( (NUM_ROWS,NUM_ROWS) )
IMAGE = [[ numpy.random.randint(0,16777215) for x in range(NUM_ROWS) ] for y in range(NUM_ROWS) ]
IMAGE[0][0] = 16777215

r = 12
g = 100
b = 25
bgrVal = (b << 16) + (g << 8) + r

IMAGE[4][0] = bgrVal



GPIO.output(LED_PIN_RED1,GPIO.LOW)
GPIO.output(LED_PIN_RED2,GPIO.LOW)
GPIO.output(LED_PIN_BLUE,GPIO.LOW)
GPIO.output(LED_PIN_GREEN,GPIO.LOW)
GPIO.output(LED_PIN_YELLOW,GPIO.LOW)
GPIO.output(LED_PIN_WHITE,GPIO.LOW)

time.sleep(0.5)

GPIO.output(LED_PIN_RED1,GPIO.HIGH)
GPIO.output(LED_PIN_RED2,GPIO.HIGH)
GPIO.output(LED_PIN_BLUE,GPIO.HIGH)
GPIO.output(LED_PIN_GREEN,GPIO.HIGH)
GPIO.output(LED_PIN_YELLOW,GPIO.HIGH)
GPIO.output(LED_PIN_WHITE,GPIO.HIGH)

time.sleep(0.5)

GPIO.output(LED_PIN_RED1,GPIO.LOW)
GPIO.output(LED_PIN_RED2,GPIO.LOW)
GPIO.output(LED_PIN_BLUE,GPIO.LOW)
GPIO.output(LED_PIN_GREEN,GPIO.LOW)
GPIO.output(LED_PIN_YELLOW,GPIO.LOW)
GPIO.output(LED_PIN_WHITE,GPIO.LOW)

top = Tk()
top.title("makr canvas")

canvas = Canvas(top, bg="black", height=300, width=300)
canvas.pack()

canvas_pixels = [[ canvas.create_rectangle(x*20,y*20, (x*20)+20, (y*20)+20, fill="red") for y in range(NUM_ROWS) ] for x in range(NUM_ROWS) ]



BLUE_MASK = 0xFF0000
GREEN_MASK = 0xFF00
RED_MASK = 0XFF

RED = (0, 200, 0)
pixels.fill(RED)
pixels.show()
time.sleep(1)

PIXEL_MAPPING = [
    (0,0), ## 0
    (1,0), ## 1
    (2,0), ## 2
    (3,0),
    (4,0),
    (4,1),
    (4,2),
    (4,3),
    (4,4),
    (3,4), ## 10
    (2,4),
    (1,4),
    (0,4),
    (0,3), ## 14, top right corner
    (0,2),
    (0,1),
    (1,1),
    (2,2),
    (3,3)
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
    mainnumber = 256
    if ( COLOR_MODE == "LOGO" ):
        mainnumber = imw * imh
    halfnumber = math.floor(mainnumber/2)
    for i in range(NUM_ROWS):
        for j in range(NUM_ROWS):
            d = math.hypot( i-7, j-7 )
            num = math.floor( (math.sin(d/2-(ripple_ctr/halfnumber))*halfnumber) + halfnumber )
            if ( COLOR_MODE == "LOGO" ):
                col = convert_rgb_to_int(im_vals[int(num)])
            else:
                col = convert_rgb_to_int(linear_rainbow(num))
            #col = convert_rgb_to_int((num,num,num))
            IMAGE[i][j] = col

zinc = 0

##viz_image(im_array)
##set_pixels_from_IMAGE()

while True:
    if GPIO.input(BUTTON_PIN_1) == True:
        print("Button 1")
        COLOR_MODE == "RAINBOW"
        GPIO.output(LED_PIN_RED1,GPIO.HIGH)
        GPIO.output(LED_PIN_RED2,GPIO.LOW)

    if GPIO.input(BUTTON_PIN_2) == True:
        print("Button 2")
        COLOR_MODE == "LOGO"
        GPIO.output(LED_PIN_RED2,GPIO.HIGH)
        GPIO.output(LED_PIN_RED1,GPIO.LOW)

    if GPIO.input(BUTTON_PIN_3) == True:
        print("Button 3")
        ANIM_MODE == "PERLIN"
        GPIO.output(LED_PIN_BLUE,GPIO.HIGH)
    else :
        GPIO.output(LED_PIN_BLUE,GPIO.LOW)

    if GPIO.input(BUTTON_PIN_4) == True:
        print("Button 4")
        ANIM_MODE == "RIPPLE"
        GPIO.output(LED_PIN_GREEN,GPIO.HIGH)
    else :
        GPIO.output(LED_PIN_GREEN,GPIO.LOW)

    if GPIO.input(BUTTON_PIN_5) == True:
        print("Button 5")
        GPIO.output(LED_PIN_YELLOW,GPIO.HIGH)
    else :
        GPIO.output(LED_PIN_YELLOW,GPIO.LOW)

    if GPIO.input(BUTTON_PIN_6) == True:
        print("Button 6")
        GPIO.output(LED_PIN_WHITE,GPIO.HIGH)
    else :
        GPIO.output(LED_PIN_WHITE,GPIO.LOW)

    #time.sleep(0.5)
##    perl = perlin(x+xoffset,y+yoffset,seed=seednum)
##    visualize_perlin(perl)
##    xoffset += random.uniform(-0.5,0.5)
##    yoffset += random.uniform(-0.5,0.5)


##    viz_perlin_logo(zinc)
##    set_pixels_from_IMAGE()
##    zinc += 0.02

    if ANIM_MODE == "PERLIN":
        if ( COLOR_MODE == "RAINBOW" ):
            vis_perlin_lib(zinc)
        else :
            viz_perlin_logo(zinc)
            set_pixels_from_IMAGE()
            zinc += 0.02
    elif ANIM_MODE == "RIPPLE":
        vis_ripple()
        set_pixels_from_IMAGE()
        ripple_ctr += 20

    time.sleep(0.1)
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
