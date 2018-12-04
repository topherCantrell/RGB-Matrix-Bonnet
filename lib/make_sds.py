import pixel_sign

color_cursor = 0

def readLines(filename):
    with open(filename,"r") as f:
        lines = f.read().split("\n")
        ret = []
        for line in lines:
            if ';' in line:
                i = line.index(';')
                line = line[0:i]
            if len(line)>0:
                ret.append(line)    
        return ret

def parse_color_spec(spec):
    global color_cursor
    spec = spec.replace('_','').strip()
    if '@' in spec:
        i = spec.index('@')
        crs = spec[i+1:].strip()
        spec = spec[0:i].strip()
        color_cursor = int(crs,16)
    if color_cursor>255:
        raise Exception('Exceeded 256 colors')
    g = color_cursor
    color_cursor += 1
    
    if spec.startswith('rgb'):
        i = spec.index('(')
        j = spec.rindex(')')
        frags = spec[i+1:j].split(',')
        spec = '00'+frags[1].strip()+frags[0].strip()+frags[2].strip()
    
    return g,int(spec,16)    
    
def readMovie(filename):    
    global color_cursor
    color_cursor = 0
    ret = {
        "colors" : [0]*256, 
        "delay"  : 0, 
        "frames" : [], 
        "name"   : ''
    }
    
    i = filename.rindex('/')
    g = filename[i+1:]
    i = g.index(".")
    ret["name"] = g[0:i]    
    
    if len(ret["name"])>15:
        raise Exception("Name must be less than 16 characters: "+ret["name"])
    lines = readLines(filename)
    pos = 0
    while True:
        g = lines[pos]
        pos += 1
        if g[0]=='%':
            break
        if g[0]=='#':
            cps,col = parse_color_spec(g[1:])
            #print(":"+hex(cps)+":"+hex(col))
            ret['colors'][cps] = col
        if g.startswith("delay "):
            ret["delay"] = int(g[6:])
            
    fs = ''
    while True:
        if pos==len(lines) or lines[pos][0]=='%':            
            ret["frames"].append(pixel_sign.SignFrame(fs))            
            fs = ''
            pos+=1
        if pos>len(lines):
            break
        fs = fs + lines[pos]
        pos += 1
        
    return ret            
        
def fourByteNumber(number):    
    by = [number & 0xFF, 
          (number>>8) & 0xFF, 
          (number>>16) & 0xFF,
          (number>>24) & 0xFF
         ]
    return bytes(by)
        

if __name__=='__main__':
    
    ROOT = "../Parade2018"
            
    master = readLines("%s/master.txt" % (ROOT,))
    
    movies = []
    for m in master:
        movies.append(readMovie("%s/%s" % (ROOT,m)))
        
    binA = open("%s/a.bin" % (ROOT,),"wb")   
    
    preA = b'2018\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
    binA.write(preA)
        
    currentSector = 1
    for ent in range(0,31):   
        dt = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        if ent < len(movies):
            m = movies[ent]
            dt = b''
            for x in range(0,12):
                if x<len(m["name"]):
                    dt = dt + bytes(m["name"][x].encode('ascii'))
                else:
                    dt = dt + b'\x00'
            dt = dt + fourByteNumber(currentSector);        
            currentSector = currentSector + 3 + len(m["frames"])*2;    
        binA.write(dt)
                
    for m in movies:
        # Write 1 sector info NUMFRAMES,DELAY
        dt = fourByteNumber(len(m["frames"]))
        binA.write(dt)
        
        dt = fourByteNumber(m["delay"])
        binA.write(dt);
           
        for x in range(0,512-8):
            binA.write(b'\x00');            
        
        # Write 2 sectors colors
        for x in range(0,256):
            if x<len(m["colors"]):
                dt = fourByteNumber(m["colors"][x])
            else:
                dt = fourByteNumber(0)
            binA.write(dt);            
            
        for f in m["frames"]:
            d = f.get_binary()
            if len(d)!=2048:
                raise Exception("Size")
            binA.write(d)          
    
    binA.flush()
    binA.close()    
