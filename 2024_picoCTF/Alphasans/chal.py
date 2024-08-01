#!/usr/bin/python3

from pwn import *
from time import sleep
import re


b = process(executable="/usr/bin/bash", argv=[], stdin=PTY)

while True:
  user_in = input("SansAlpha$ ")
  if user_in[-1] != "\n":
    user_in += "\n"
  alpha_filter_result = re.search("[a-zA-Z]", user_in)
  slash_filter_result = re.search("\\\\", user_in)
  if user_in == "exit\n":
    break
  if alpha_filter_result != None or slash_filter_result != None:
    print("SansAlpha: Unknown character detected")
    continue
  cmd = user_in.encode()
  b.send(cmd)
  sleep(0.5)
  o = b.recv(timeout=0.5)
  if o != b"":
    for line in o.decode().split('\n'):
      print(line)