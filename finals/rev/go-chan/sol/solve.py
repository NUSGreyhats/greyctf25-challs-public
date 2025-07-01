import re
from pipe_solver import PipePuzzleSolver
lines = open("./decomp.c", "r").readlines()
grid =[[[None for _ in range(4)] for _ in range(4)] for _ in range(4)]


faces1 = ["Front", "Right", "Back", "Left"]
faces2 = ["Top", "Bottom"]

def get_face_name(chan_ops, name):
    if len(chan_ops) == 4:
        faces = faces1
    elif len(chan_ops) == 2:
        faces = faces2
    else:
        raise ValueError("Invalid chanops", chan_ops)
    for i, x in enumerate(chan_ops):
        if "=" not in x:
            continue
        if name in x.split("=")[0]:
            return faces[i]
    assert 0, "Not found"

start = False

chan_ops = []
chan_ops_2 = []

idx = 0
for i in range(len(lines)):
    line = lines[i]
    if "os_Getenv" in line:
        start = True
        continue
    if not start:
        continue
    if "runtime_chanrecv1" in lines[i-1]:
        chan_ops.append(line)
    if "if" in line and chan_ops:
        chan_ops_2.append(chan_ops)
        chan_ops = []
    if "main_LinkChannels" in line:
        chan_ops_2.append(chan_ops)
        m = re.search(r"main_LinkChannels\((.+), (.+)\)", line)
        config = (get_face_name(chan_ops_2[0], m.group(1)), get_face_name(chan_ops_2[1], m.group(2)))
        grid[idx//16][(idx % 16)//4][idx % 4] = config
        chan_ops_2 = []
        chan_ops = []
        idx += 1
    if "runtime_newobject" in line:
        break


# 2. Prepare the solver
end_pipe = grid[-1][-1][-1]
end_entry_face = end_pipe[1] if end_pipe[0] == "Bottom" else end_pipe[0]
end_pos = (tuple(len(grid)-1 for _ in range(3)), end_entry_face)

# 3. Create and run the solver
solver = PipePuzzleSolver(grid, ((0,0,0), "Top"), end_pos, [(0,0,0), (len(grid)-1,len(grid)-1,len(grid)-1)])
solver.solve()
points = [list(x[0]) for x in solver.path] + [end_pos[0]]
print("Points:",points)

commands = []
for i, step in enumerate(solver.path):
    coord = step[0]
    rots = step[-1]
    if not rots:
        continue
    rots = rots[1]
    for rot in rots:
        commands.extend(coord)
        if rot == "U":
            commands.append(0)
        else:
            commands.append(2)
commands = [len(commands)//4] + commands
print(commands)

from pwn import *

p = process("./go_chan")
p.recvuntil(b"number of moves")
for c in commands:
    p.sendline(str(c).encode())
p.interactive()