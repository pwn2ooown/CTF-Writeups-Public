#!/bin/sh

echo 314159265 | ./helloworld | grep -aEo 'FLAG\{[^}]+\}' --color=never
