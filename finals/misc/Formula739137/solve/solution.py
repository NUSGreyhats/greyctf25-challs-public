#!/usr/bin/env python3

import struct

f = open('task.png', 'rb')
f.read(8)   # read PNG signature

txt = []
while True:
    l,t = struct.unpack('>I4s', f.read(8))
    d = f.read(l)
    c, = struct.unpack('>I', f.read(4))
    
    if t == b"IDAT":
        char_code = c & 0xFF
        if (9 <= char_code <= 13) or (32 <= char_code <= 126):
            txt.append(chr(char_code))
    if t == b'IEND':
        break
        
print("".join(txt))