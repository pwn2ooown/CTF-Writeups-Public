FROM ubuntu:22.04
MAINTAINER lys0829

RUN apt-get update && \
    DEBAIN_FRONTEND=noninteractive apt-get install -qy xinetd

RUN useradd -m eert
RUN chown -R root:root /home/eert
RUN chmod -R 755 /home/eert

CMD ["/usr/sbin/xinetd", "-dontfork"]