python3 -c "import sys,base64;data=base64.b64decode(open('NOTflag.txt','rb').read());sys.stdout.buffer.write(bytes([b^0xFF for b in data]))"
