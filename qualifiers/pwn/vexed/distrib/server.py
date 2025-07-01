#!/usr/local/bin/python3
import mmap
import ctypes
import base64
from capstone import *
from capstone.x86 import *

def check(code: bytes) -> bool:
    if len(code) > 0x300:
        return False

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    for insn in md.disasm(code, 0):
        # Check if instruction is AVX2
        if not (X86_GRP_AVX2 in insn.groups):
            raise ValueError("AVX2 Only!")
        
        name = insn.insn_name()
        
        # No reading memory
        if "mov" in name.lower():
            raise ValueError("No movs!")

    return True

def run(code: bytes):
    # Allocate executable memory using mmap
    mem = mmap.mmap(-1, len(code), prot=mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC)
    mem.write(code)
    
    # Create function pointer and execute
    func = ctypes.CFUNCTYPE(ctypes.c_void_p)(ctypes.addressof(ctypes.c_char.from_buffer(mem)))
    func()
    
    exit(1)


def main():
    code = input("Shellcode (base64 encoded): ")
    try:
        code = base64.b64decode(code.encode())
        if check(code):
            run(code)
    except:
        print("Invalid base64!")
        exit(1)


if __name__ == "__main__":
    main()
