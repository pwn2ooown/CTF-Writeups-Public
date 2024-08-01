#!/bin/sh

xortool xor -b
cd xortool_out
cat *.out | grep -a -o -E 'FLAG\{[^}]+\}' --color=never