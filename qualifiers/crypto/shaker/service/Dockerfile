FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    socat

COPY shaker.py /run.py
COPY run.sh /run.sh
COPY flag.txt /flag.txt

RUN chmod 555 /run.py
RUN chmod 555 /run.sh
RUN chmod 444 /flag.txt

CMD socat TCP-LISTEN:5000,reuseaddr,fork EXEC:/run.sh,stderr