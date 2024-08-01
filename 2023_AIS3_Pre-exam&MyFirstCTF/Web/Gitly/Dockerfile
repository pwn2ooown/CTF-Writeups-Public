FROM alpine:3 as builder

RUN apk add --no-cache gcc musl-dev make git sassc sqlite-dev

WORKDIR /tmp
RUN git clone https://github.com/vlang/v --depth=1 && cd v && make
RUN git clone https://github.com/vlang/gitly.git --depth=1 && \
    cd gitly && \
    sassc src/static/css/gitly.scss > src/static/css/gitly.css && \
    /tmp/v/v install pcre markdown && \
    /tmp/v/v .

COPY readflag.c .
RUN gcc readflag.c -o readflag

FROM alpine:3

RUN apk add --no-cache git sqlite-dev curl
COPY --from=builder /tmp/gitly /tmp/gitly
COPY --from=builder /tmp/readflag /readflag
RUN chmod 4755 /readflag

WORKDIR /tmp/gitly
RUN chown -R nobody:nobody .

COPY ./gitly.sqlite .
RUN chown root:root ./gitly.sqlite && \
    chmod 444 ./gitly.sqlite

USER nobody
RUN mkdir -p ./repos/admin && \
    git clone --bare https://github.com/vlang/gitly.git ./repos/admin/gitly
CMD ["./gitly"]
