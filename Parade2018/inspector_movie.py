from pixel_sign import SignFrame
import pixel_text

with open('inspectorGEN.txt','w') as ps:
    
    x_toy = 64
    x_insp = -63
    
    for _ in range(64):
        frame = SignFrame()
        pixel_text.draw_string('FreeSerif9pt7b',frame,x_toy,12,'Toy',[1,2,3])
        pixel_text.draw_string('simple7x13',frame,x_insp,4,'Inspector',[4,5,6,7,8,9,10,11,12],0)
        
        if x_toy>15:
            x_toy -=1
        x_insp +=1
        ps.write(frame.to_string())
        
    for _ in range(64*5):
        ps.write(frame.to_string())
    
            