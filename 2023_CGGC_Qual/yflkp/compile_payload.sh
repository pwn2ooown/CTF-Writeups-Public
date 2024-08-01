#!/bin/bash

musl-gcc exp.c -o exp -static
cat exp | base64 > ooo.bin