FROM ubuntu:22.04

ENV user ctf
RUN useradd -m $user
WORKDIR /home/$user

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install socat -y
RUN rm -rf /var/lib/apt/lists/*

COPY ./aircon ./aircon
COPY ./flag.txt ./flag.txt
RUN chmod +x aircon

USER $user

CMD ["socat", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:./aircon"]
