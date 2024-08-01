import sys
chars = ""
from fileinput import input
for line in input():
  chars += line

lookup1 = "\n \"#()*+/1:=[]abcdefghijklmnopqrstuvwxyz"
lookup2 = "ABCDEFGHIJKLMNOPQRSTabcdefghijklmnopqrst"

out = ""

prev = 0
for char in chars:
  cur = lookup1.index(char)
  print(f"cur: {cur}, prev: {prev}")
  print(f"cur - prev: {(cur - prev) % 40}")
  out += lookup2[(cur - prev) % 40]
  prev = cur
  print(f"prev is now: {prev}")

sys.stdout.write(out)
