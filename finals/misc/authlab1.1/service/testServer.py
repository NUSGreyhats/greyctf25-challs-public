import pickle
from pickletools import *
from base64 import b64encode
import socket

from pickleassem import PickleAssembler

def testInput(pa):
    payload = pa.assemble()
    payload_b64 = b64encode(payload)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost',33401))  

    sock.recv(1024).decode()
    sock.send("e\n".encode())
    sock.recv(1024).decode()

    sock.send(payload_b64+b'\n')
    print(sock.recv(1000).decode())
    sock.close()

# should fail

# using open
print("[DEBUG] Testing open")
pa = PickleAssembler(proto=4)
pa.push_global('builtins','exit')
pa.push_global('builtins','set')
pa.push_global('builtins','open')

INJECTION = 'server.py'
pa.push_short_binunicode(INJECTION)
pa.build_tuple1()       # (INJECTION,)
pa.build_reduce()       # open(INJECTION)
pa.build_tuple1()
pa.build_reduce()
pa.build_tuple1()
pa.build_reduce()
testInput(pa)


# using help
print("[DEBUG] Testing help")
pa = PickleAssembler(proto=4)
pa.push_global('builtins','help')
pa.push_empty_tuple()
pa.build_reduce()
testInput(pa)

# using breakpoint
print("[DEBUG] Testing breakpoint")
pa = PickleAssembler(proto=4)
pa.push_global('builtins','breakpoint')
pa.push_empty_tuple()
pa.build_reduce()
testInput(pa)