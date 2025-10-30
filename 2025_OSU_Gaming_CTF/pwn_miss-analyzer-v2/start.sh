#!/bin/sh
docker container rm -f miss-analyzer
docker run -d -p7273:1337 --restart=always --name=miss-analyzer --privileged miss-analyzer
