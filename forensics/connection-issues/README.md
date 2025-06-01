# Details

One of our employees was browsing the web when he suddenly lost connection! Can you help him figure out why?

# Author

jovantanyk

# Solution

Apply filter `arp.opcode == 2 && arp.src.hw_mac == bc:24:11:78:c8:64 && arp.src.proto_ipv4 == 192.168.100.1` in wireshark. Flag is hidden as Base64 in the padding bytes in chunks of 4.

# Learning objectives

Learn to use wireshark filters, identify arp poisoning through malicious ARP reply packets.

# Flag

`grey{d1d_1_jus7_ge7_p01son3d}`

