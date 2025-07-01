import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost',33301))

sock.recv(1024).decode()
sock.send("F\n".encode())
ct = sock.recv(1024).decode()[17:50]
print("Target:\n" + ct + "\n")
sock.shutdown(0)

chars = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789}"
ind = 0
flag = "grey{"
while flag[-1] != "}":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost',33301))
    sock.recv(1024).decode()
    sock.send("M\n".encode())
    sock.recv(1024).decode()

    sock.send((flag + chars[ind] + "\n").encode())
    t = sock.recv(1024).decode()[17:18+len(flag)]
    if ct.startswith(t):
        print(f'{t:<{len(ct)}} | {flag}')
        flag += chars[ind]
        ind = 0
        continue
    ind += 1
    if ind == len(chars):
        break
    sock.shutdown(0)

print(f'Flag is {flag}')
# grey{pR3t7y_5urE_c4n_8rUT3_f0rC3}