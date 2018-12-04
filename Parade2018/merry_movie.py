from pixel_sign import SignFrame
import pixel_text

with open('merryGEN.txt','w') as ps:
    
    y_merry = -26
    y_christ = 17 
    
    for _ in range(18):        
        frame = SignFrame()
        pixel_text.draw_string('simple7x13',frame,12,y_merry,'Merry',[1,2,3,4,5],0)
        pixel_text.draw_string('simple7x13',frame,1,y_christ,'Christmas',[6,7,8,9,10,11,12,13,14],0)        
        ps.write(frame.to_string())
        
        if y_merry<-10:
            y_merry += 1
        if y_christ>4:
            y_christ -= 1
        
    for _ in range(64*5):
        ps.write(frame.to_string())
        