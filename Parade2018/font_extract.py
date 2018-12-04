
with open('7x13.txt','r') as f:
    g = f.readlines()
    
pos = 0
while not g[pos]=='STARTCHAR space\n':
    pos+=1

data = ''

print('Bitmaps = [')
for _ in range(32*3-1):
    for i in range(13):
        print('  0x'+g[pos+6+i][0:2]+', ',end='')
    print('')        
    pos+=20
print(']')
print('')

# offs,width,height,adv_cursor,x_ofs,y_ofs

print('Glyphs = [')
for c in range(32*3-1):
    print('  ['+str(c*13)+', 8, 13, 7, 0, 13],')
print(']')
    
