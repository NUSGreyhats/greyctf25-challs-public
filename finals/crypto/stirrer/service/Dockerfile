FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    socat 

RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install pycryptodome

COPY server.py /server.py
COPY run.sh /run.sh
COPY flag.txt /flag.txt
COPY encrypt.c /encrypt.c

RUN chmod 555 /server.py
RUN chmod 555 /run.sh
RUN chmod 444 /flag.txt
RUN chmod 444 /encrypt.c
RUN gcc -O3 encrypt.c -o encrypt

CMD socat TCP-LISTEN:5000,reuseaddr,fork EXEC:/run.sh,stderr
