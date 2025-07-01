fail = False
try:
    with open("./flag.txt", "rb") as f:
        b = f.read()
        b = b.strip()
        if b[:5] != b"grey{":
            fail = True
        if b[-1] != ord('}'):
            fail = True
        b = b[5:-1]
except:
    fail = True
if len(b) != 16:
    fail = True

if not fail:
    b = bytes(reversed([x ^ 42 for x in b]))

    with open("./flag.txt", "wb") as f:
        f.write(b)