# Hardware reference at https://github.com/topherCantrell/pixel-sign

# Adafruit library: https://github.com/hzeller/rpi-rgb-led-matrix
# Python bindings:  https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python

import time
import os
from random import randint

# The RGB matrix libraries
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from rgbmatrix import graphics

# We use PyGame to read the USB controllers
import pygame
pygame.init()
clock = pygame.time.Clock()
#
control_one = pygame.joystick.Joystick(0)
control_one.init()
control_two = pygame.joystick.Joystick(1)
control_two.init()

# This is the configuration for the 64x32 LED matrix
# You shouldn't need to change anything here
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
            
# Object to talk to the matrix    
matrix = RGBMatrix(options = options)

# Lots of fonts in the 'fonts' folder. We'll use a 5x8 in this demo
font = graphics.Font()
font.LoadFont("rpi-rgb-led-matrix/fonts/5x8.bdf")

# Two squares are controlled by the USB controller. This helper
# function draws 4x4-pixel squares
def draw_players(square_1,square_2):
    offscreen_canvas = matrix.CreateFrameCanvas()   
    graphics.DrawText(offscreen_canvas, font, 2, 10, graphics.Color(255, 255, 0), 'Controllers!')    
    for j in range(4):
        for i in range(4):
            offscreen_canvas.SetPixel(square_1[0]+i,square_1[1]+j,255,0,0)
    for j in range(4):
        for i in range(4):
            offscreen_canvas.SetPixel(square_2[0]+i,square_2[1]+j,0,0,255)  
    matrix.SwapOnVSync(offscreen_canvas) 

# The demo is an infinite loop
while True:

    # Flash "HACK ME!" five times
    for i in range(5):
        # Start with a canvas we can draw on behind the scenes
        offscreen_canvas = matrix.CreateFrameCanvas()    
        graphics.DrawText(offscreen_canvas, font, 13, 10, graphics.Color(255, 255, 0), 'HACK ME!')    
        graphics.DrawText(offscreen_canvas, font,  3, 20, graphics.Color(255, 0, 0), 'What fun can')
        graphics.DrawText(offscreen_canvas, font,  8, 28, graphics.Color(0, 255, 255), 'you make?')
        # Once our back-buffer is ready, swap it onto the display    
        matrix.SwapOnVSync(offscreen_canvas)
        
        time.sleep(1)
        
        offscreen_canvas = matrix.CreateFrameCanvas()    
        graphics.DrawText(offscreen_canvas, font, 3, 20, graphics.Color(255, 0, 0), 'What fun can')
        graphics.DrawText(offscreen_canvas, font, 8, 28, graphics.Color(0, 255, 255), 'you make?')    
        matrix.SwapOnVSync(offscreen_canvas)
        
        time.sleep(0.5)

    # Show the IP address  

    ip_addr = os.popen('ifconfig eth0 | grep "inet "').read()
    ip_addr = ip_addr.strip().split(' ')[1].split('.')
    offscreen_canvas = matrix.CreateFrameCanvas()    
    graphics.DrawText(offscreen_canvas, font, 13, 10, graphics.Color(255, 255, 0), 'HACK ME!')
    # Just show the last two bytes    
    graphics.DrawText(offscreen_canvas, font, 1, 25, graphics.Color(200, 255, 200), 'pi @ .'+ip_addr[2]+'.'+ip_addr[3])
    matrix.SwapOnVSync(offscreen_canvas)
    
    time.sleep(5)
    
    # Some random pixels
    for i in range(800):
        x = randint(0,64)
        y = randint(0,32)
        offscreen_canvas.SetPixel(x,y,randint(1,255),randint(1,255),randint(1,255))
        matrix.SwapOnVSync(offscreen_canvas)
        time.sleep(0.01)
        
    time.sleep(2)
    
    # Move the squares with the controllers for a few seconds
    square_1 = [20,16]
    square_2 = [43,16]
    draw_players(square_1,square_2)
    for i in range(1000):    
        for event in pygame.event.get():
            xa = control_one.get_axis(0)
            xb = control_one.get_axis(1)        
            if xa<-0.5:
                square_1[0]-=1
            elif xa>0.5:
                square_1[0]+=1
            if xb<-0.5:
                square_1[1]-=1
            elif xb>0.5:
                square_1[1]+=1
            xa = control_two.get_axis(0)
            xb = control_two.get_axis(1)        
            if xa<-0.5:
                square_2[0]-=1
            elif xa>0.5:
                square_2[0]+=1
            if xb<-0.5:
                square_2[1]-=1
            elif xb>0.5:
                square_2[1]+=1
            draw_players(square_1,square_2)
        # We use the PyGame clock instead of "time.sleep" here so that
        # joystick events still come in
        clock.tick(100)