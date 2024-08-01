FROM ubuntu:22.04
MAINTAINER LJP-TW

ENV DEBAIN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3 socat

COPY flag /flag
COPY readflag /readflag

RUN chown root:root /flag && chmod 400 /flag
RUN chown root:root /readflag && chmod 4755 /readflag

RUN useradd -m ctf

USER ctf

CMD socat tcp-listen:1338,reuseaddr,fork exec:/home/ctf/run.py,pty,echo=0,raw,iexten=0
