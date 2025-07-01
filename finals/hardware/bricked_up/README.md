# Bricked Up

# Details
Hardware/Reverse

A classic game of brick! 

# Author
fieash
# Solution
- change the mpy bytecode header to python header
- decompile with mpy-tool.py -d
- find out the sequence is
up up down down left right left right B A
- triggers the multiplier that does 1000x score
- play the tetris and score 10000 points or higher, via a 4 line clear/clear 10 single lines (combo implementation rewards more line clears).
- grey{go_do_this_on_stage} will be printed, replicate the challenge on the stage and get the flag

# Flag

```
grey{c4ts_h4v3_30_1iv3s!}
```