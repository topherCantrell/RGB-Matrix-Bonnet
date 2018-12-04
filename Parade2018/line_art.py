from pixel_sign import SignFrame
from bresenham import bresenham

DIV = 4

def draw_line(x0,y0,x1,y1,color,frame):
    coords = list(bresenham(x0,y0,x1,y1))
    for c in coords:
        frame.set_pixel(c[0],c[1],color)
        
def draw_box(x0,y0,color,frame,a,b,c,d):
    for i in range(0,32,DIV):
        if a:
            draw_line(x0+i,y0,x0+31,y0+i,color,frame)
        if b:
            draw_line(x0+31,y0+i,x0+31-i,y0+31,color,frame)
        if c:
            draw_line(x0+31-i,y0+31,x0,y0+31-i,color,frame)
        if d:
            draw_line(x0,y0+31-i,x0+i,y0,color,frame)
        
with open('artGEN.txt','w') as ps:
        
    frame = SignFrame()        
    
    draw_box(0,0,1,frame,False,True,False,True)    
    
    ps.write(frame.to_string())