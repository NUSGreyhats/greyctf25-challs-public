import board
import digitalio
import time
import hardware.fpga

hardware.hw_state["fpga_overlay"].deinit()
if input("type something to update fpga: ") != "":
    h = hardware.fpga.upload_bitstream("/hardware/bitstreams/main.bit")
    h.deinit()

fpga_interconnect_pins = [board.GP8, board.GP9, board.GP10, board.GP11,	board.GP12, board.GP13, board.GP14, board.GP15]
### FPGA Interconnect
def overlay_interconnect_pins():
    dio = []
    for p in fpga_interconnect_pins:
        d = digitalio.DigitalInOut(p)
        d.direction = digitalio.Direction.OUTPUT
        dio.append(d)
    return dio

interconnect = overlay_interconnect_pins()

fpga_mode = [0, 1, 0]
interconnect[7].value = 0
interconnect[6].value = 1
interconnect[5].value = 0


### Insert your remaining code here