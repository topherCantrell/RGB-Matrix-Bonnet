'''
Each row has one orbiter 8 to 24 long. Each created orbiter has a random wait to appear (as below)
All orbiters travel right at speeds: 3,4, or 5.
Orbiters scroll on and off.
When orbiter dies, wait random 8 frames and create a new one, but only create 100 total orbiters.
Continue moving until all orbiters are done

Can also show

Color pattern:

1234 44444 5678

'''

import random
from pixel_sign import SignFrame

TOTAL_ORBITERS = 64
ORBIT_DIRECTION = 1

RANDOM_ORBITER_WAIT   = [ 4, 10]
RANDOM_ORBITER_SPEED  = [ 3,  6]
RANDOM_ORBITER_TTL    = [25, 40]
RANDOM_ORBITER_LENGTH = [ 8, 24]
RANDOM_ORBITER_COLOR  = [ 0,  7] # 8 levels of each color ... multiply by 8

def make_orbiter(y):
    ret = {}
    ret['wait'] = random.randint(RANDOM_ORBITER_WAIT[0],RANDOM_ORBITER_WAIT[1])
    ret['speed'] = random.randint(RANDOM_ORBITER_SPEED[0],RANDOM_ORBITER_SPEED[1])
    ret['ttl'] = random.randint(RANDOM_ORBITER_TTL[0],RANDOM_ORBITER_TTL[1])
    ret['length'] = random.randint(RANDOM_ORBITER_LENGTH[0],RANDOM_ORBITER_LENGTH[1])
    ret['x'] = random.randint(0,64)
    ret['y'] = y
    ret['color'] = random.randint(RANDOM_ORBITER_COLOR[0],RANDOM_ORBITER_COLOR[1])*8
    ret['state'] = 'growing' # or running or shrinking
    ret['current_length'] = 0
    return ret

orbiters = []
for i in range(32):
    orbiters.append({'ttl':0,'y':i})

with open('orbitGEN.txt','w') as ps:
    
    while len(orbiters)>0:
        
        frame = SignFrame()
        
        for i in range(len(orbiters)-1,-1,-1):
            orbit = orbiters[i]
            if orbit['ttl'] <= 0:
                if TOTAL_ORBITERS>0:
                    TOTAL_ORBITERS -= 1
                    orbiters[i] = make_orbiter(orbit['y'])
                    continue
                else:
                    del orbiters[i]
                
            if orbit['wait']>0:
                orbit['wait'] -= 1
            else:                   
                orbit['ttl'] -= 1            
                
                if orbit['state'] == 'growing':
                    orbit['current_length'] += orbit['speed']
                    orbit['x'] += ORBIT_DIRECTION * orbit['speed'] 
                    if orbit['current_length']>=orbit['length']:
                        orbit['state'] = 'running'
                elif orbit['state'] == 'shrinking':                 
                    orbit['current_length'] -= orbit['speed']
                    if orbit['current_length']<1:
                        orbit['current_length'] = 1
                else:
                    orbit['x'] += ORBIT_DIRECTION * orbit['speed']
                    if orbit['ttl'] <= orbit['length']/orbit['speed']:
                        orbit['state'] = 'shrinking'
            
           
            for j in range(orbit['current_length']):
                # TODO color changes over the length
                color_offset = orbit['current_length']-j-1
                if color_offset > 4:
                    color_offset = color_offset-orbit['current_length']+8
                    if color_offset<4:
                        color_offset = 4
                #if color_offset>4:
                #    color_offset = color_offset -
                # 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15  n-len+8  = 13-15+8
                # 0 1 2 3 4 4 4 4 4 4  4  4  4  5  6  7  
                frame.set_pixel(orbit['x']-j,orbit['y'],orbit['color']+color_offset)
                
        ps.write(frame.to_string())
        
    