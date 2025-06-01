# Solution

Essentially the executable is reads and runs custom bytecode. The custom bytecode will encrypt given file using hill cipher and a simple xor loop

Information about hill cipher can be found here:
https://en.wikipedia.org/wiki/Hill_cipher

firstly, xor all the bytes using a xor loop using the key "googoogaga"

From there to reverse the Hill Cipher, will have to obtain the adjoint of the key matrix which is a 2x2 matrix containing the byte values for the string "sDda". From there, will have to obtain the modular inverse of the number of values  which is 256 and the determinent. From there obtain the inverse of the matrix and do matrix multiplication to obtain the original file 
