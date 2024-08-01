FROM python:3-alpine

RUN apk add --no-cache curl

COPY ./flag/flag /flag
COPY ./flag/readflag /readflag
RUN chown root:root /flag && chmod 0400 /flag
RUN chown root:root /readflag && chmod 4755 /readflag

USER nobody
WORKDIR /app
COPY ./src .

CMD ["python3", "server.py"]
