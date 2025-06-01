# Challenge List

### ezpz

_a collection of BEGINNER-FRIENDLY challenges_

| Done? | Name                  | Challenge Details                              | Estimated Difficulty (1-5) | Port Number |
| ----- | --------------------- | ---------------------------------------------- | -------------------------- | ----------- |
| yes | Reversing 101 | simple RE challenge, q&a style | 1 | 33000 |
| yes | babyweb | simple reflected xss using location.href | 1 | 33001 |
| yes | baby\_bytes | Arbitrary read+write. Overwrite saved retaddr in stack with addr of win function. | 1 | 33002 |
| yes | Tung Tung Tung Tung Tung Tung Tung Sahur | Reverse the arithmetic operations then iroot and long_to_bytes | 1 | - |

### pwn

| Done? | Name                  | Challenge Details                              | Estimated Difficulty (1-5) | Port Number |
| ----- | --------------------- | ---------------------------------------------- | -------------------------- | ----------- |
| yes   | vexed                 | shellcoding chall, only accepts non-mov AVX2   | 3                          | 33101 |
| yes   | infinite connect four | buffer overflow to ret2win                     | 1-2                        | 33102 |
| yes   | Adversarial Beaver    | craft a turing machine to perform your exploit | 2-3                        | 33103 |

### Web

| Done? | Name         | Challenge Details                                      | Estimated Difficulty (1-5) | Port Number |
| ----- | ------------ | ------------------------------------------------------ | -------------------------- | ----------- |
| yes   | hft          | Race condition when selling $FLAG                      | 2                          | 33201 |
| yes   | sgrpc        | gRPC reflection mechanism                              | 2                          | 33202 |
| yes   | c2           | curl Gopher SSRF + CGO file include to exfiltrate flag | 5                          | 33203 |
| yes   | Rainbow Road | Keep websocket open and bypass javascript checks       | 3                          | 33204 |

### Crypto

| Done? | Name                     | Challenge Details                                                                                                       | Estimated Difficulty (1-5) | Port Number |
| ----- | ------------------------ | ----------------------------------------------------------------------------------------------------------------------- | -------------------------- | ----------- |
| yes   | uwusignatures            | Schnorr signature value reuse                                                                                           | 2                          | 33301 |
| yes   | Not a Permutation Matrix | Solve a system of equations in the group [Q8 x\| D4](https://people.maths.bris.ac.uk/~matyd/GroupNames/61/Q8s5D4.html). | 5                          | -     |
| yes   | idk                      | ZK F reuse + non-deterministic sqrt                                                                                     | 3                          | -     |
| yes   | shaker                   | funny custom XEX thing                                                                                                  | 1                          | 33302 |

### RE

| Done? | Name         | Challenge Details                                                                              | Estimated Difficulty (1-5) | Port Number |
| ----- | ------------ | ---------------------------------------------------------------------------------------------- | -------------------------- | ----------- |
| yes   | meow-ware    | decrypt malware traffic pcap given upx-packed c2 client that is upx-packed but upx is stripped | 3                          | -           |
| yes   | where cat    | custom bytecode used to encrypt a file.                                                        | 4                          | -           |
| yes   | The Cat Shop | Password checker in gameboy binary                                                             | 3                          | -           |
| yes   | sksksk       | Flag checker using only sk combinators. Characters are encoded in ascii as church numerals     | 2/3                        | -           |

### Forensics

| Done? | Name              | Challenge Details                                                                                                         | Estimated Difficulty (1-5) | Port Number |
| ----- | ----------------- | ------------------------------------------------------------------------------------------------------------------------- | -------------------------- | ----------- |
| yes   | layer cake | File conversion and analysis                                                         | 1                          | -           |
| yes   | connection issues | Network analysis/PCAP challenge to identify ARP poisoning attacks                                                         | 1                          | -           |
| yes   | notsus.exe        | Using Bkcrack to perform ZipCrypto known plaintext attack using common DOS Stub Header, then simple PyInstaller reversing | 2                          | -           |

_if there is insufficient forensics challenges, we will merge with misc_

### Misc

| Done? | Name                    | Challenge Details                                                                               | Estimated Difficulty (1-5) | Port Number |
| ----- | ----------------------- | ----------------------------------------------------------------------------------------------- | -------------------------- | ----------- |
| yes   | Countle Training Centre | (pyjail) code inject to excepthook, and inspect global vars outside curr function scope         | 3-4                        | 33401 |
| yes   | subGB                   | Subpixel Text Encoding used to hide flag in image, guessy                                       | 1                          | - |
| yes   | Elijah's Sequential CTF                   | Dynamic Programming / Just remember last 3 highest scores that ended with 0/1/2 | 1                          | 33402 |
| yes   | Secret Development Kit | PCB Tracing/ Reversing from Production Gerbers | 2 | - |

### OSINT

| Done? | Name              | Challenge Details                                                                                                         | Estimated Difficulty (1-5) | Port Number |
| ----- | ----------------- | ------------------------------------------------------------------------------------------------------------------------- | -------------------------- | ----------- |
| yes   | By the banana tree      | Geolocation without street view                                                         | 2                          | -           |
| yes   | Red Flag Recon          | Find private commits containing the flag that is accidentally leaked into a public repo | 2                          | -           |
| yes   | Like Comment Subscribe  | Hex to String conversion in greyctf reel                                                | 1                          | -           |

### Blockchain

| Done? | Name              | Challenge Details                                                                                                         | Estimated Difficulty (1-5) | Port Number |
| ----- | ----------------- | ------------------------------------------------------------------------------------------------------------------------- | -------------------------- | ----------- |
| yes   | launchpad | ? | ? | 33501, 33502 |
| yes   | rational | ? | ? | 33503, 33504 |


### README Templates

Essentially, all **README.md** files should contain the following information

| Things to include               | Example                                                                   |
| ------------------------------- | ------------------------------------------------------------------------- |
| Challenge Details               | `Caesar thought of the perfect cipher. Can you break it?`                 |
| Possible hints                  | `Hint: What Caesar Cipher?`                                               |
| Key concepts                    | `Scripting`                                                               |
| Solution (Can also be a script) | `Write a script to brute force all the combinations of the caesar cipher` |
| Learning objectives             | `Learn about the Caesar Cipher`                                           |
| Flag                            | `grey{salad_is_great_but_cipher_is_not}`                                  |

