### CatCore

# Details

Here at GreyCatTheFlag we have experience managing cats of different types. We have elmocat, we have jrocat, we have GPMGcat, and much more. 
You can now leverage our year of experience with CatCore Hyper, the latest version of our Hardware Coprocessor, specifically designed for managing cats.

Worried about security? No worries, being cat experts we have made sure that no one can anyhow mobilise your cats or show the white flag.
Only we can do it lmao.

# Author

Hackin7

# Solution

This is a datasheet + shorting challenge

1. Short CS pin of the FPGA flash to GND to trigger dev mode
2. Run DevMode Commands to leak the memory
    - Short the NC pin (pin A3) on the datasheet to GND
3. Brute force all possible keys of XORing with the desired flag read instruction


# Flag

```
grey{lmao_sandbox}
```