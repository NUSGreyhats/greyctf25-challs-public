FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install socat -y
RUN useradd -m pwn

COPY ./go_chan ./go_chan
RUN ln -s /bin/bash /app/sh


RUN chown -R root:root /app
RUN chmod -R 555 /app

CMD bash -c "socat TCP-LISTEN:5000,reuseaddr,fork EXEC:./go_chan,stderr"

