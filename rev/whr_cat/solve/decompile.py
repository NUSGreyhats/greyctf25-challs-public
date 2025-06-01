import sys
import re
import struct

output_name = ""
input_name = ""

mapping = {32: ('mov', [1, 1]), 33: ('movb', [1, 1]), 34: ('movi', [1, 4]), 35: ('movabs', [1, 8]), 56: ('jmp', [8]), 57: ('jg', [8, 1, 1]), 58: ('jl', [8, 1, 1]), 59: ('jge', [8, 1, 1]), 60: ('jle', [8, 1, 1]), 61: ('je', [8, 1, 1]), 62: ('jne', [8, 1, 1]), 63: ('call', [8]), 64: ('retn', []), 16: ('add', [1, 1]), 17: ('sub', [1, 1]), 18: ('mul', [1, 1]), 19: ('div', [1, 1]), 20: ('divf', [1, 1]), 21: ('or', [1, 1]), 22: ('and', [1, 1]), 23: ('xor', [1, 1]), 24: ('push', [1]), 25: ('pop', [1]), 153: ('syscall', [1])}

reg_mapping = {65: 'r1', 66: 'r2', 67: 'r3', 68: 'r4', 69: 'r5', 70: 'r6', 71: 'r7', 72: 'r8', 73: 'r9', 74: 'r10', 75: 'r11', 76: 'r12', 77: 'r13', 78: 'r14', 79: 'r15', 80: 'r16', 96: 'r17', 97: '[r1]', 98: '[r2]', 99: '[r3]', 100: '[r4]', 101: '[r5]', 102: '[r6]', 103: '[r7]', 104: '[r8]', 105: '[r9]', 106: '[r10]', 107: '[r11]', 108: '[r12]', 109: '[r13]', 110: '[r14]', 111: '[r15]', 112: '[r16]', 113: '[r17]', 81: 'rbp', 82: 'rsp', 83: 'rip'}

f = open("chall.sad","rb")
f.read(16)

num_of_strings = int.from_bytes(f.read(4),"little")
strings = {}

for i in range(num_of_strings):
    offset = f.tell()
    size = int.from_bytes(f.read(4),"little")
    strings[offset] = f.read(size).replace(b"\x00",b"").decode()

code = f.read()
code_size = len(code)
i = 0
lines = {}
lines_jump = []
not_reg_op = ["movb","movi","movabs"]
offset = 0
while i < code_size:
    print(offset)
    offset = i
    op, arg_sizes = mapping[code[i]]
    print(op)
    line = op
    i += 1
    if op == "syscall":
        line += " " + hex(code[i])
        i += 1
    else:
        for x in range(len(arg_sizes)):
            size = arg_sizes[x]
            if x == 0:
                print(size)
                if size == 1:
                    line += " " + reg_mapping[code[i]]
                else:
                    line += " " + hex(offset + struct.unpack("<q",code[i:i+size])[0])
            elif op in not_reg_op:
                line += " " + hex(int.from_bytes(code[i:i+size],"little"))
            else:
                line += " " + reg_mapping[code[i]]
            i += size

    lines[offset] = line
for x in lines:
    print(f"0x{hex(x)}: {lines[x]}")




    


