from pixel_sign import SignFrame
import random

def make_square():
    width = random.randint(4,50)
    height = random.randint(4,50)
    color = random.randint(1,10)
    x = random.randint(0,64+width*2)-width
    y = random.randint(0,32+height*2)-height
    timer = random.randint(50,80)
    return {
        'x' : x,
        'y' : y,
        'color' : color,
        'width' : width,
        'height' : height,
        'timer' : timer
    }
    
def draw_square(s,frame):
    for i in range(s['width']):
        frame.set_pixel(s['x']+i,s['y'],s['color'])
        frame.set_pixel(s['x']+i,s['y']+s['height']-1,s['color'])
    for j in range(s['height']):
        frame.set_pixel(s['x'],s['y']+j,s['color'])
        frame.set_pixel(s['x']+s['width']-1,s['y']+j,s['color'])

with open('squaresGEN.txt','w') as ps:    
    
    left_to_make = 200
    max_alive = 50
    
    squares = [make_square()]
    
    while left_to_make>0 or len(squares)>0:
    
        frame = SignFrame()
        
        for i in range(len(squares)-1,-1,-1):
            s = squares[i]
            draw_square(s,frame)    
            s['timer'] -= 1
            if s['timer'] <= 0:
                del(squares[i])
        ps.write(frame.to_string())
        
        if len(squares)<max_alive:
            if left_to_make>0:
                squares.append(make_square())
                left_to_make -= 1