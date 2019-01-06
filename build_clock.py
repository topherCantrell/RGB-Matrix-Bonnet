import argparse
import time
import sys
import os

# Bag and Tag: February 19, 2019 - 23:59 Eastern (22:59 Central)

import datetime

BAG_AND_TAG = datetime.datetime(2019,2,19,22,59,59)
def get_bag_tag_delta():    
    NOW = datetime.datetime.now()
    until = int(BAG_AND_TAG.timestamp() - NOW.timestamp())
    
    days = int(until/(24*60*60))
    until = until - days*(24*60*60)
    
    hours = int(until/(60*60))
    until = until - hours*(60*60)
    
    minutes = int(until/60)
    seconds = until - minutes*60
    
    return (days,hours,minutes,seconds)

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from rgbmatrix import graphics

options = RGBMatrixOptions()
        
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.row_address_type = 0
options.multiplexing = 0
options.pwm_bits = 11
options.brightness = 100
options.pwm_lsb_nanoseconds = 130
options.led_rgb_sequence = 'RGB'
options.pixel_mapper_config = ''
                
matrix = RGBMatrix(options = options)

font = graphics.Font()
font.LoadFont("rpi-rgb-led-matrix/fonts/7x13.bdf")

seven_seg = [
  [1,1,1,1,1,1,0],
  [0,1,1,0,0,0,0],
  [1,1,0,1,1,0,1],
  [1,1,1,1,0,0,1],
  [0,1,1,0,0,1,1],
  [1,0,1,1,0,1,1],
  [1,0,1,1,1,1,1],
  [1,1,1,0,0,0,0],
  [1,1,1,1,1,1,1],
  [1,1,1,1,0,1,1]      
]

colon_dots = [
    [15,17],[15,18],
    [15,22],[15,23],
    [31,17],[31,18],
    [31,22],[31,23],
    [47,17],[47,18],
    [47,22],[47,23],
    ]

digit_coords = [
    [1,15],[8,15],
    [17,15],[24,15],
    [33,15],[40,15],
    [49,15],[56,15],
    
    ]

def draw_digit(offscreen_canvas,coords,digit,color):
    x = coords[0]
    y = coords[1]
    dat = seven_seg[digit]
    for a in range(6):
        if dat[0]:
            offscreen_canvas.SetPixel(x+a,y,color[0],color[1],color[2])
        if dat[1]:
            offscreen_canvas.SetPixel(x+5,y+a,color[0],color[1],color[2])
        if dat[2]:
            offscreen_canvas.SetPixel(x+5,y+a+5,color[0],color[1],color[2])
        if dat[3]:
            offscreen_canvas.SetPixel(x+a,y+10,color[0],color[1],color[2])
        if dat[4]:
            offscreen_canvas.SetPixel(x,y+5+a,color[0],color[1],color[2])
        if dat[5]:
            offscreen_canvas.SetPixel(x,y+a,color[0],color[1],color[2])
        if dat[6]:
            offscreen_canvas.SetPixel(x+a,y+5,color[0],color[1],color[2])

def draw_number(offscreen_canvas,ind,num,color):
    a = int(num/10)
    b = int(num%10)      
    draw_digit(offscreen_canvas,digit_coords[ind*2],a,color) 
    draw_digit(offscreen_canvas,digit_coords[ind*2+1],b,color)          

  
                
while True:       
    days,hours,minutes,seconds = get_bag_tag_delta()
    offscreen_canvas = matrix.CreateFrameCanvas()
    
    # Digit placement (tops shown)    
    # ................................................................
    # .######.######.#.######.######.#.######.######.#.######.######..
    
    RED = [255,0,0]
    GREEN = [0,255,0]
    BLUE = [0,0,255]
    CYAN = [0,255,255]
    WHITE = [255,255,255]
    
    textColor = graphics.Color(255, 255, 0)
    graphics.DrawText(offscreen_canvas, font, 1, 10, textColor, 'Bag & Tag')
    
    color = WHITE
    for cs in colon_dots:
        offscreen_canvas.SetPixel(cs[0],cs[1],color[0],color[1],color[2])    
    
    draw_number(offscreen_canvas,0,days,RED)
    draw_number(offscreen_canvas,1,hours,BLUE)
    draw_number(offscreen_canvas,2,minutes,GREEN)
    draw_number(offscreen_canvas,3,seconds,CYAN)
    
    matrix.SwapOnVSync(offscreen_canvas)
    time.sleep(1) 
    
