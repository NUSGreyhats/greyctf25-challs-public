### Secure Memory

# Details

It's security at the hardware level so it must be secure right?

# Author

Hackin7

# Solution

```python
import board
import digitalio
import time
import hardware.fpga

hardware.hw_state["fpga_overlay"].deinit()
if input("type something to update fpga: ") != "":
    h = hardware.fpga.upload_bitstream("/hardware/bitstreams/main.bit")
    h.deinit()

fpga_interconnect_pins = [board.GP8, board.GP9, board.GP10, board.GP11,	board.GP12, board.GP13, board.GP14, board.GP15]
rp2350_pmod_pins = [board.GP27, board.GP16, board.GP23, board.GP25, board.GP26, board.GP28, board.GP22, board.GP24]

### FPGA Interconnect
def overlay_interconnect_pins():
    dio = []
    for p in fpga_interconnect_pins:
        d = digitalio.DigitalInOut(p)
        d.direction = digitalio.Direction.OUTPUT
        dio.append(d)
    return dio

def pmod_pins():
    dio = []
    for p in rp2350_pmod_pins:
        if p == None: pass
        d = digitalio.DigitalInOut(p)
        d.direction = digitalio.Direction.INPUT
        dio.append(d)
    return dio


interconnect = overlay_interconnect_pins()
pmod = pmod_pins()

fpga_mode = [0, 1, 0]
interconnect[7].value = 0
interconnect[6].value = 1
interconnect[5].value = 0

def read_char():
    value = 0
    for p in range(len(pmod)):
        if pmod[p] == None: pass
        value |= pmod[p].value << p;
    return chr(value)

def set_address(addr):
    addr_bits = [0, 0, 0, 0, 0]
    addr_val = addr
    for i in range(len(addr_bits)):
        addr_bits[i] = addr_val % 2
        addr_val = addr_val // 2
    print("Address:",addr, addr_bits)
    for v in range(len(addr_bits)):
        interconnect[v].value = addr_bits[v]
    

def enumerate_addresses(): # Never wait for clock cycle
    for i in range(32):
        set_address(i)
        c = read_char()
        print(c, ord(c))
        
def enumerate_addresses_wait():
    for i in range(32):
        set_address(i)
        time.sleep(0.2)
        c = read_char()
        print(c, ord(c))
        
def enumerate_addresses_wait_and_bypass():
    out = ""
    for i in range(32):
        set_address(i)
        time.sleep(0.15)
        set_address(31)
        c = read_char()
        print(c, ord(c))
        out += c
    print("Out:", out)
    return out
        
enumerate_addresses_wait_and_bypass()
```

The RP PMOD might not have enough pins but they can just use the JTAG pins lmao

# Flag

```
grey{race_flag}
```