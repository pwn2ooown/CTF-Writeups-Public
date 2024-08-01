import codecs
src='''#coding: punycode
def _(): pass
('Correct!' if ('Enter the flag: ') == 'DUCTF{%s}' % _.____ else 'Wrong!')-gdd7dd23l3by980a4baunja1d4ukc3a3e39172b4sagce87ciajq2bi5atq4b9b3a3cy0gqa9019gtar0ck'''
res = codecs.decode(src, 'punycode')

print(res)
# import string

# def is_printable(char):
#     return char in string.printable
# for i in res:
# 	if is_printable(i):
# 		print(i,end='')
