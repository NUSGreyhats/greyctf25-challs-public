All participants are provided with a TP-Link WN722N which can be set to monitor mode to sniff network traffic.

This opens up many new attack vectors for wireless network communications.

1. Wifi Router Setup
    - Set a strong admin password (prevent griefing)
    - Set a weak WiFi password from rockyou.txt
    - Enabled Protected Management Frames (PMF)
        - This prevents griefing via deauth attacks
    - Enabled hidden SSID to prevent discovery of network
    - WiFi should not be internet connected (noisy network)
2. Setup a web server behind a nginx proxy that is only accessible by visiting `camera.home`
    - Web server mimics an IoT authentication portal that prompts for a password
    - Password should be a strong password
    - Password hint is "who do i love?"
    - After authentication, the flag is given.
3. Setup a DNS server without the network
    - Configure `camera.home` to `<ip_address_of_web_server>`
4. Setup a server that runs a python script to emit network requests
    - This probe request will broadcast saved SSIDs (provides the password for the auth portal)
    - This mimics the neighbour accidentally leaking his saved SSIDs on his device
    - We also emit DNS requests to the DNS server to query for `camera.home`, for the participants to sniff.

The logical solution path would be:

1. Participants can sniff nearby network packets to identify a device called `Tom` sending a probe request with a saved network `I love gr3y_k17713s`. This will be useful later on.
2. Participants identify the hidden SSID by scanning in monitor mode.
3. Do a PMKID attack to dump pre-shared key password hash. Brute-force this to authenticate to the network.
4. Sniffing within the network reveals a DNS server and a DNS request for `camera.home`. We can set the domain and IP in our `/etc/hosts` to access the webpage.
5. Webpage prompts for a username and password, we can set the password to `gr3y_k17713s` to authenticate and get the flag.

Essentially, this challenge brings across a few points

1. Tom uses a weak wifi password, leading to his wifi being compromised
2. He saves network SSIDs that reveal sensitive information.
3. Sniffing DNS requests can help you identify local endpoints.
4. Accessing a web server behind proxy by setting the appropriate domain name.

Learning objectives:

- WPA2 is vulnerable to offline brute-force attack, so please use secure passwords.
- Your device leaks saved SSIDs, do not use any sensitive SSID name.
- Hidden SSIDs can be found easily.
- DNS requests are send unencrypted within the network.
