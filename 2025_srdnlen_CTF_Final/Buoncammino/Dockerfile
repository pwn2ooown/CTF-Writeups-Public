FROM ubuntu:24.04

RUN apt-get update
RUN apt-get install -y socat libstdc++6 libseccomp-dev 

WORKDIR /chal

COPY ./test /chal/test
COPY ./flag.txt /chal/flag.txt

RUN chmod 755 /chal/test
RUN chmod 744 flag.txt

USER ubuntu

ENTRYPOINT ["socat", "-t", "300", "-T", "30", "TCP4-LISTEN:1920,reuseaddr,nodelay,fork", "EXEC:/chal/test"]
EXPOSE 1920
#ENTRYPOINT [ "/chal/test" ]