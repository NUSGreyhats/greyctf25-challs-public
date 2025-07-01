import zlib
import math

text = open("./container.py", "rb").read()

p1 = open("./minified.py", "rb").read()
p1 = zlib.compress(p1)

parts = ["(a:=[])"]
chunk_size = math.ceil(len(p1)/30)
for x in range(0, len(p1), chunk_size):
    parts.append("a.append('" + str(p1[x:x+chunk_size].hex()) + "')")
parts.append("exec(__import__('zlib').decompress(bytes.fromhex(''.join(a))))")
out = b""
hide_prev = False
count = 0
N = 300
acc = b""
for line in text.splitlines():
    if line[:2] == b"  ":
        if acc:
            if len(acc) > N and count < len(parts):
                acc = acc[:(len(acc)//4)*3] + b"{"+parts[count].encode() +b"}"+acc[(len(acc)//4)*3:] +b"\n"
                count += 1
                print(count)
            out += acc + b"\n"
        out += line + b" "
        acc = b""
    else:
        acc += line.strip() + b" "
        

runner = open("./runner.py", "rb").read()
out = out.replace(b"X2", f"exec(bytes.fromhex('{runner.hex()}'))".encode())

with open("./out2.py", "wb") as f:
    f.write(out)