import codecs
src=open('wtf.py').read()
print(codecs.encode(src, 'punycode').decode())