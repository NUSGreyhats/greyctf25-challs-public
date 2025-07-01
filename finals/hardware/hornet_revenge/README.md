### Hornet Revenge

# Details

I want revenge.

Stop the backend and run this in the Thonny REPL to start the challenge.

```python
from hornet_revenge import *
```

# Author

Hackin7

# Solution


```python
Adafruit CircuitPython 9.2.7 on 2025-04-01; Raspberry Pi Pico 2 with rp2350a

>>> from challenge.hornet_revenge_source import *
FutureWarning: Display moved from displayio to busdisplay
FutureWarning: Display renamed BusDisplay
FutureWarning: FourWire moved from displayio to fourwire
Initialising FPGA...
585728 bytes uploaded in 9459 ms (61 kB/s)
There are 4 functions to run, qna1(), qna2(), qna3(), qna4()
>>> qna1()
Type in full
What is the mcu of the device?
0. STM32F103C8T6
1. ATMEGA328P
2. RP2350
3. ESP32
Answer: 2

What does the P in PIO stand for?
Answer: programmable

What is an FPGA? Answer with F???? P??????????? G??? A???? 
Answer: field programmable gate array

What are FPGAs 'coded' in? Answer with ????l??
Answer: verilog

What is the FPGA chip on here? Answer with ?????-??F-6BG256?
Answer: lfe5u-25f-6bg256c
Success: Here's the 1st part of the flag:
grey{for_last_greyctf_
>>> qna2()
connect GP27 of the RP to GND
2nd part of the flag
i_was_
>>> qna3()
Next, we need to extract the key from the FPGA
I've imported the libraries busio and board for you.
Gimme some code to initialise uart at baud rate 9600 on board GP8 and GP9: uart = busio.UART(board.GP8, board.GP9, baudrate=9600, timeout=0.1)
Send the string '@---------------A@' excluding quotes to the uart: uart.write("@---------------A@")
Gimme some code to retrieve the key from the FPGA: print(uart.read())
b"{hi_i'm_your_army}"
Run qna4()
>>> qna4()
Enter the key you got from qna3(): {hi_i'm_your_army}
3rd part of the flag
holding_back...but_this_greyctf_i'm_no_longer_sleep_deprived}
>>> 
```


# Flag

```
grey{for_last_greyctf_i_was_holding_back...but_this_greyctf_i'm_no_longer_sleep_deprived}
```