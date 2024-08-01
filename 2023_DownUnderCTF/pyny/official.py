f = open('./pyny.py', 'rb').read()
print(f.replace(b'#coding: punycode',b'').decode('punycode'))