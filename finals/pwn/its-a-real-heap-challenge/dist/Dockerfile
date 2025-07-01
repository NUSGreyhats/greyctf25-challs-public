FROM ubuntu:22.04

ENV user ctf

RUN apt-get -y update
RUN apt-get install -y python3 socat && rm -rf /var/lib/apt/lists/*

RUN useradd $user
WORKDIR /home/$user

COPY ./chall /home/$user/chall
COPY ./flag.txt /home/$user/flag.txt
COPY ./run.py /home/$user/run.py
RUN chmod +x chall
RUN chmod +x run.py

USER $user

CMD socat TCP-LISTEN:5000,reuseaddr,fork EXEC:/home/$user/run.py,stderr
