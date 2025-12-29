FROM ubuntu:24.04@sha256:4fdf0125919d24aec972544669dcd7d6a26a8ad7e6561c73d5549bd6db258ac2 AS base
WORKDIR /app
COPY --chmod=555 chall run
RUN echo "FLAG{dummy}" > flag.txt
RUN mv flag.txt flag-$(md5sum flag.txt | awk '{print $1}').txt

FROM pwn.red/jail
COPY --from=base / /srv
ENV JAIL_TIME=300 JAIL_CPU=100 JAIL_MEM=10M
