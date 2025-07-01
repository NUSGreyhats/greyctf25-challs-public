# WE CANNOT HANDLE SWITCH CASES
# WE CANNOT HANDLE FUNCTIONS WITH NO STACK SPACE (we end up clobbering stuff at lower address than RSP)

from pwn import rol, ror
import re
import capstone
import sys
import keystone
import random

# FIELDS TO CHANGE
START = 0x1369
END = 0x227e
ENTRY = 0x2117
TAIL = 0x22289
UNOBFUSCATED = open("./a.out", "rb").read()[START:END]
OBFUSCATED = []

def is_call_internal(insn, START, END):
    """
    Check if instruction is a call to an address between START and END (inclusive)

    Args:
        insn: Capstone instruction object
        START: Start address of internal range
        END: End address of internal range

    Returns:
        bool: True if it's a call to an address within [START, END]
    """
    # First check if it's a call instruction
    if not insn.group(capstone.CS_GRP_CALL):
        return False

    # Check operands for the target address
    for op in insn.operands:
        target_addr = None

        if op.type == capstone.x86.X86_OP_IMM:
            # Direct call with immediate address
            target_addr = op.imm

        elif op.type == capstone.x86.X86_OP_MEM and op.mem.base == capstone.x86.X86_REG_RIP:
            # RIP-relative call (call [rip + offset])
            target_addr = insn.address + insn.size + op.mem.disp

        # Check if target is within range
        if target_addr is not None and START <= target_addr <= END:
            return True

    return False

def has_rip_relative(insn):
    """Check if instruction has RIP-relative addressing"""
    if not insn.operands:
        return False

    for op in insn.operands:
        if op.type == capstone.x86.X86_OP_MEM:
            if op.mem.base == capstone.x86.X86_REG_RIP:
                return True
    return False

# init keystone & capstone

ks = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
cs.detail = True

# define obfuscation constants

registers = [
    'rax', 'rbx', 'rcx', 'rdx', 
    'rsi', 'rdi', 'rbp',
    'r8', 'r9', 'r10', 'r11', 
    'r12', 'r13', 'r14', 'r15'
]

obfs_head = "popfq; popfq; "
# instruction will be here (after head, before prologue)
obfs_pro = "pushfq; pushfq; call here; .byte {value}; here:; push {reg}; movabs {reg}, {value2}; " # value = rand 8-bit, value2 = rand 64-bit
obfs_body = [("add {reg}, {value}; ", lambda x, y: (x + y) & 0xffffffffffffffff), # value = rand 32-bit
             ("sub {reg}, {value}; ", lambda x, y: (x - y) & 0xffffffffffffffff), # value = rand 32-bit
             ("xor {reg}, {value}; ", lambda x, y: (x ^ y) & 0xffffffffffffffff), # value = rand 32-bit
             ("rol {reg}, {value}; ", lambda x, y: rol(x, y, 64)), # value = rand {0, 8}
             ("ror {reg}, {value}; ", lambda x, y: ror(x, y, 64))] # value = rand {0, 8}
obfs_epi = "pop {reg}; ret"

# obfuscation starts here

final_instructions = [] # this stores the final set of obfuscated assembly
instructions_map = {} # {old_address: (new_address, instruction)} | this is important for finding relocs later

# shuffle original set of instructions

instructions = list(cs.disasm(UNOBFUSCATED, START))
random.shuffle(instructions)

rip = START
need_fixups = [] # (address, orig_insn) | addresses to revisit in second-pass for fixups
obfs_body_fixups = [] # address (max_size = 50)
MAX_OBFS_SIZE = 80
entry_hole = False

# first-pass: map all instructions into an address

for i in instructions:

    if (rip > ENTRY - 0x20) and entry_hole == False:
        final_instructions += list(random.randbytes(0x40))
        rip += 0x40
        entry_hole = True

    # insert random bytes hehe
    rand_bytes = list(random.randbytes(random.randint(0, 40)))
    final_instructions += rand_bytes
    rip += len(rand_bytes)

    # this is where our new instruction starts
    instructions_map[i.address] = (rip, i)

    # append instructions head (popf)
    insn_head_bytes = ks.asm(obfs_head)[0]
    final_instructions += insn_head_bytes
    rip += len(insn_head_bytes)

    # append instruction itself
    if i.group(capstone.CS_GRP_CALL) and not is_call_internal(i, START,END):
        final_instructions += ks.asm(f"{i.mnemonic} {i.op_str}", addr=rip)[0] # for calls that do not need reloc
    else:
        final_instructions += list(i.bytes)

    if i.group(capstone.CS_GRP_JUMP) or has_rip_relative(i) or is_call_internal(i, START, END):
        need_fixups.append((rip, i))
        final_instructions += b"\x90"*4
        rip += 4

    rip += len(i.bytes)

    # if i.group(capstone.CS_GRP_JUMP) or is_call_internal(i, START, END):
    #     final_instructions += list(random.randbytes(10))
    #     rip += 10
    # else:
    final_instructions += [0 for _ in range(MAX_OBFS_SIZE)]
    obfs_body_fixups.append((rip, i))
    rip += MAX_OBFS_SIZE

    assert (rip == START + len(final_instructions))

final_instructions = bytearray(final_instructions)

# second-pass: fixup instructions with rel addressing

for i in need_fixups:
    new_addr, insn = i

    if insn.group(capstone.CS_GRP_JUMP) or is_call_internal(insn, START, END):
        if '0x' not in insn.op_str:
            print("we cannot handle register jmps/calls", insn)
            sys.exit(-1)
        else:
            if insn.address == 0x1218:
                breakpoint()
            new_loc = instructions_map[int(insn.op_str, 16)][0]
            # skip the popf popf if we are doing a jmp/call
            new_insn_bytes = ks.asm(f"{insn.mnemonic} {hex(new_loc+2)}", addr=new_addr)[0]
            # print(f"{hex(new_addr)}: {insn.mnemonic} {hex(new_loc)}", len(insn.bytes), len(new_insn_bytes))
            assert len(new_insn_bytes) <= 10 # we only made space for 10 bytes
            final_instructions[new_addr-START:new_addr-START+len(new_insn_bytes)] = new_insn_bytes
    elif has_rip_relative(insn):
        cap = re.search(r"0x[0-9a-f]+", insn.op_str)[0]
        rel_value = int(cap, 16)
        ref = insn.address + len(insn.bytes) + rel_value
        new_rel_value = ref - new_addr - len(insn.bytes)
        new_insn = insn.mnemonic + " " + insn.op_str.replace(cap, hex(new_rel_value))
        new_insn_bytes = ks.asm(new_insn, addr=new_addr)[0]
        final_instructions[new_addr-START:new_addr-START+len(new_insn_bytes)] = new_insn_bytes

# final-pass generate transformation for control flow obfs

for i in obfs_body_fixups:

    cur_addr, insn = i
    obfs_transformations = []

    next_insn_addr = insn.address + len(insn.bytes)
    try:
        new_next_insn_addr = instructions_map[next_insn_addr][0]
        register = random.choice(registers)
        start_value = int.from_bytes(random.randbytes(8), 'big')
        cur_value = start_value

        insn_prologue_bytes = ks.asm(obfs_pro.format(value=f'0x{random.randbytes(1).hex()}',
                                                     reg=register,
                                                     value2=hex(start_value)))[0]

        obfs_transformations += insn_prologue_bytes
        offset = new_next_insn_addr - (cur_addr+7) # 6 is the size of 'pushf; call $+5'

        num_transformations = random.randint(1, 5)
        transformations = random.sample(obfs_body, num_transformations)
        for t in transformations:
            tasm_fmt, tfunc = t

            if tasm_fmt[0] == 'r': # ror/rol
                v = random.randint(0, 255)
                tasm = tasm_fmt.format(reg=register, value=v)
                cur_value = tfunc(cur_value, v)
            else:
                v = random.randint(0x0, 0x7fffffff)
                tasm = tasm_fmt.format(reg=register, value = hex(v))
                cur_value = tfunc(cur_value, v)

            obfs_transformations += ks.asm(tasm)[0]
            # print(tasm)
            # print(cur_value)


        remaining_registers = registers[:]
        remaining_registers.remove(register)
        second_register = random.choice(remaining_registers)
        last_transformation = random.choice(obfs_body[:2])

        if last_transformation[0][:3] == "add":
            last_tvalue = (offset - cur_value) & 0xffffffffffffffff
        elif last_transformation[0][:3] == "sub":
            last_tvalue = (-1*(offset - cur_value)) & 0xffffffffffffffff

        tasm = f"push {second_register};  movabs {second_register}, {last_tvalue}; "
        tasm += last_transformation[0].format(reg=register, value=second_register)
        tasm += f"pop {second_register}; "
        tasm += f"add [rsp+8], {register}; "
        tasm += f"pop {register}; ret"
        obfs_transformations += ks.asm(tasm)[0]

        # obfs_transformations += ks.asm(obfs_epi.format(reg=register))[0]

        obfs_transformations += list(random.randbytes(MAX_OBFS_SIZE - len(obfs_transformations)))
        final_instructions[cur_addr-START:cur_addr-START+MAX_OBFS_SIZE] = obfs_transformations

    except Exception as e:
        print("this should be the last instruction:", insn)
        # print(e)

with open("./a.out", "rb") as f:
    x = bytearray(f.read())

NEW_ENTRY = instructions_map[ENTRY]
new_insn = ks.asm(f"jmp {NEW_ENTRY[0]+2}", addr=ENTRY)[0]
final_instructions[ENTRY-START:ENTRY-START+len(new_insn)] = new_insn
x[START:START+len(final_instructions)] = final_instructions

final_instructions += bytearray(random.randbytes(TAIL - len(final_instructions)))

with open("./a.out.obfs", "wb") as f:
    f.write(x)

print(hex(len(final_instructions)))
