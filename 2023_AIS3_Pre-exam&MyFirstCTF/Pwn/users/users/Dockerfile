FROM ubuntu:jammy-20230425

RUN apt update && apt install -y socat

WORKDIR /app
COPY ./home/ ./

CMD socat \
    -dd \
    TCP-LISTEN:5000,reuseaddr,fork \
    EXEC:"./run",stderr
