from pixel_sign import SignFrame as FRAME_TYPE

MAX_COLORS = 256

color_cursor = 0 # Used to auto-number colors

colors_used = [False]*MAX_COLORS

def read_lines(filename):
    '''Read lines and ignore comments and blank lines
    '''
    with open(filename,"r") as f:
        lines = f.readlines()        
        ret = []
        for line in lines:
            if ';' in line:
                i = line.index(';')
                line = line[0:i]
            line = line.strip()
            if len(line)>0:
                ret.append(line)    
        return ret

def parse_color_spec(spec):
    global color_cursor, colors_used
    spec = spec.replace('_','').strip()
    if '@' in spec:
        # The spec includes the color number
        i = spec.index('@')
        crs = spec[i+1:].strip()
        spec = spec[0:i].strip()
        color_cursor = int(crs,16)
    if color_cursor>=MAX_COLORS:
        raise Exception('Exceeded {max} colors'.format(max=MAX_COLORS))
    if colors_used[color_cursor]:
        raise Exception('Color {num} already has a value'.format(num=color_cursor))
    colors_used[color_cursor] = True
    g = color_cursor    
    color_cursor += 1
    
    if spec.startswith('rgb'):
        i = spec.index('(')
        j = spec.rindex(')')
        frags = spec[i+1:j].split(',')
        if len(frags)!=3:
            raise Exception('Expected 3 (RGB) color values in: {0}'.format(spec))
        for i in range(3):
            while len(frags[i])<2:
                frags = '0'+frags
            # TODO work with these as numbers 0..255
        spec = '00'+frags[1].strip()+frags[0].strip()+frags[2].strip()
    
    return g,int(spec,16)    
    
def readMovie(filename):    
    global color_cursor, colors_used
    color_cursor = 0
    colors_used = [False]*MAX_COLORS
    ret = {
        'colors' : [0]*MAX_COLORS, 
        'delay'  : 0, 
        'frames' : [], 
        'name'   : ''
    }
    
    # Strip the path off the name
    i = filename.rindex('/')
    g = filename[i+1:]
    if '.' in g:
        i = g.index('.')
        ret['name'] = g[0:i]    
    
    if len(ret['name'])>15:
        raise Exception("Name must be less than 16 characters '{0}'".format(ret['name']))
    
    # Read the colors off the top
    lines = read_lines(filename)
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
        if g.strip().startswith('delay '):
            ret['delay'] = int(g[6:].strip())
            
    fs = ''
    while True:
        if pos==len(lines) or lines[pos][0]=='%':            
            ret['frames'].append(FRAME_TYPE(fs))            
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
        
def make_bin(file_root):
    
    # TODO number of files, size of frames comes from the TYPE
    master = read_lines('{0}/master.txt'.format(file_root))
    
    movies = []
    for m in master:
        movies.append(readMovie('{0}/{1}'.format(file_root,m)))
        
    binA = open('{0}/a.bin'.format(file_root),'wb')   
    
    # TODO the number on the end is the file number index
    preA = b'2018\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    binA.write(preA)
    
    currentSector = 1
    for ent in range(0,31):   
        dt = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        if ent < len(movies):
            m = movies[ent]
            dt = b''
            for x in range(0,12):
                if x<len(m['name']):
                    dt = dt + bytes(m['name'][x].encode())
                else:
                    dt = dt + b'\x00'
            dt = dt + fourByteNumber(currentSector)        
            # TODO 4 per frame is type-specific
            # We deal with 512-byte sectors because that's what the propeller
            # uses with SD cards.
            currentSector = currentSector + 1 + 2 + len(m['frames'])*(2048/512)    
        binA.write(dt)
                
    for m in movies:
        # Write 1 sector info NUMFRAMES,DELAY
        dt = fourByteNumber(len(m['frames']))
        binA.write(dt)
        
        dt = fourByteNumber(m['delay'])
        binA.write(dt)
           
        for x in range(0,512-8):
            binA.write(b'\x00')            
        
        # Write 2 sectors colors
        for x in range(0,256):
            if x<len(m["colors"]):
                dt = fourByteNumber(m['colors'][x])
            else:
                dt = fourByteNumber(0)
            binA.write(dt)            
            
        for f in m['frames']:
            d = f.get_binary()
            if len(d)!=2048:
                raise Exception('Size')
            binA.write(d)          
    
    binA.flush()
    binA.close()  

if __name__=='__main__':
    
    make_bin('../Parade2018')
