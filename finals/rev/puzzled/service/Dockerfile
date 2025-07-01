FROM ubuntu:22.04 AS app

ENV user ctf

RUN apt-get -y update
RUN apt-get install -y socat && rm -rf /var/lib/apt/lists/*

RUN useradd $user
WORKDIR /home/$user

COPY ./chall /home/$user/chall
COPY ./flag.txt /home/$user/flag.txt
RUN chmod +x chall

USER ctf

CMD socat TCP-LISTEN:5000,reuseaddr,fork EXEC:/home/$user/chall,stderr
