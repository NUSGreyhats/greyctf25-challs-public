# Challenge List

### Pwn

| Done? | Name                  | Challenge Details                              | Estimated Difficulty (1-5) | Port Number |
| ----- | --------------------- | ---------------------------------------------- | -------------------------- | ----------- |
| yes   | pwn the toilet        | Heap overflow and UAF                          | 2-3                        | 35127        |
| yes   | real heap challenge | .bss OOB vulnerability exploited via heap spray | 3                        | 35128 |
| yes   | rat2libzz             | ARM return/jump oriented programming to custom shared object           | 2-3                        | 35129       |
| yes | aircon | Integer Overflow | 1 | 35130 |
| yes  | Sand Castles | heap overflow to get AAW and AAR | ? | 35131 |

### Blockchain

| Done? | Name                  | Challenge Details                              | Estimated Difficulty (1-5) | Port Number |
| ----- | --------------------- | ---------------------------------------------- | -------------------------- | ----------- |
| yes | locker | ? | ? | 34221, 34222 |
| yes | race | ? | ? | 34223, 34224 |

### Web

| Done? | Name         | Challenge Details                                      | Estimated Difficulty (1-5) | Port Number |
| ----- | ------------ | ------------------------------------------------------ | -------------------------- | ----------- |
| yes   | kitty        | Insufficient sanitization when handling globs          | 3                          | 33334        |
| yes   | oops-blog    | XSS via markdown injection                             | 2                          | 33335        |
| yes   | English or Spanish   | Javascript imports bad                             | 2                          | 33336        |
| yes   | A4 Toilet Paper   | Date() objects are non-enumerable                            | 2                          | 33337        |
| yes   | hopefully good sourceless web   | Captured variables in NextJs server actions are sent over the network                            | 3                          | 33338        |

### Crypto

| Done? | Name                     | Challenge Details                                                                                                       | Estimated Difficulty (1-5) | Port Number |
| ----- | ------------------------ | ----------------------------------------------------------------------------------------------------------------------- | -------------------------- | ----------- |
| yes   | meow-log-meow-log-meow   | Franklin-Reiter with big public exponent                                                                                | 2                          | -           |
| yes | Blind Mouse Challenge | use encryption oracle to "decrypt" flag | 1 | 33301 |
| yes | stirrer | slide attack + weak encryption breaking | 4 | 33302 |
| yes | dlog24 | zmod instead of gf, generalisation of hensel lifting | 5 | - |
| yes | safe-xor | ternary lfsr becomes mod 3 | 2-3 | - |

### RE

| Done? | Name         | Challenge Details                                                                              | Estimated Difficulty (1-5) | Port Number |
| ----- | ------------ | ---------------------------------------------------------------------------------------------- | -------------------------- | ----------- |
| yes | puzzled | heavily obfuscated (control flow obfuscation, scattered instructions) program that implements a rubiks cube game | 4                          | 35123           |
| yes | go-chan | 3D pipes game implemented using Golang channels                                                                  | 3                          | 35124           |
| yes | serpentine | Python encryption malware but the value of integers has been altered                                                                  | 3                          | -           |

### Misc

| Done? | Name | Challenge Details | Estimated Difficulty (1-5) | Port Number |
| ----- | ---- | ----------------- | -------------------------- | ----------- |
| yes | AuthLab | Insecure pickle deserialization, code execution vulnerability | 1 | 33401 |
| yes | greyhats-server | Priviledge escalation using vulnerability in authd for oauth logins | 3 | 31022 |
| yes | AuthLab1.1 | Insecure pickle deserialization, with limited module | 2 | 33402 |
| yes | suspicious neighbour | hidden ssid discovery, pmkid attack into wpa2 wifi, sniffing to identify dns server, modify /etc/hosts to access web service, default credentials to access 'iot camera' to get flag | 3 | - |
| yes | lpmc | java RE + java deserialization vuln | 4 | 35565, 38081 |
| yes | Elden Ring | DFIR | 3 | - |
| yes | Formula 739137 | IDAT/CRC Manipulation in PNG | 2 | - |
| yes | brrrrrr | Demodulate a PSK signal | 3 | - |

### Hardware

| Done? | Name | Challenge Details | Estimated Difficulty (1-5) | Port Number |
| ----- | ---- | ----------------- | -------------------------- | ----------- |
| yes | Hornet Revenge | Q&A, Shorting, Circuitpython UART Read/Write    | 1 | ----------- |
| yes | Bricked Up | mpy reverse + tetris    | 2 | ----------- |
| yes | Leaky Pin | Read Flag from PIO    | 3 | ----------- |
| yes | Shooting Flags | Reading Verilog & Badge LEDs to get the flag    | 2-3 | ----------- |
| yes | Secure Memory | Memory Race Condition Timing Attack              | 3 | ----------- |
| yes | CatCore | Reading DataSheet, Tracing Circuit, Memory Window Attack| 3 | ----------- |

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

