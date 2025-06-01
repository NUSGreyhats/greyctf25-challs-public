from PIL import Image
import numpy as np
import itertools

img = Image.open("distrib/subGB.png")
npar = np.asarray(img)
pix = npar.tolist()

for row in range(len(pix)):
    # remove alpha values from data
    pix[row] = list(itertools.accumulate(pix[row],lambda x,y: (x[:3] if len(x)==4 else x)+y[:3]))[-1]

for row in pix:
    for col  in row:
        if col == 255: print("*",end="")
        else: print(" ",end="")
    print()

# grey{Su6_P1x3m4L_m3s5A9iNg}

"""
# if screen width is small

for s,e in [(0,59),(60,114),(115,180)]:
    for row in pix:
        for col in row[s:e]:
            if col == 255: print("*",end="")
            else: print(" ",end="")
        print()
    print("\n\n\n")
"""


