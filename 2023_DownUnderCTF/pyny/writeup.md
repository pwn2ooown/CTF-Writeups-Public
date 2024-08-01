We see that it uses direct comparison so we believe that it must store the real flag somewhere. (Just guessing)

Set breakpoint at write and reach before it output corrrect or not.

And use 

```bash
pwndbg> search -t bytes DUCTF{
Searching for value: 'DUCTF{'
[heap]          0x555555bc9d57 "DUCTF{%s}' % _.____ else 'Wrong!')-gdd7dd23l3by980a4baunja1d4ukc3a3e39172b4sagce87ciajq2bi5atq4b9b3a3cy0gqa9019gtar0ck"
[heap]          0x555555bdea58 "DUCTF{%s}' % _.____ else 'Wrong!')-gdd7dd23l3by980a4baunja1d4ukc3a3e39172b4sagce87ciajq2bi5atq4b9b3a3cy0gqa9019gtar0ck"
[heap]          0x555555bf4bf5 0x73257b4654435544 ('DUCTF{%s')
[anon_7ffff7582] 0x7ffff75990a0 'DUCTF{%s}'
[anon_7ffff7582] 0x7ffff75a4075 0x73257b4654435544 ('DUCTF{%s')
[anon_7ffff7582] 0x7ffff777fd71 "DUCTF{%s}'"
[anon_7ffff7582] 0x7ffff779533c 0x73257b4654435544 ('DUCTF{%s')
[anon_7ffff7582] 0x7ffff785ff80 'DUCTF{python_warmup}'
```

Done. WTF is this problem...

Bonus: before the last breakpoint, I see the result `'DUCTF{gl17ch_m3_n07_' + chr(0x39) + chr(0x63) + chr(0x34) + chr(0x32) + chr(0x61) + chr(0x34) + chr(0x35) + chr(0x64) + '}'`. Hmm, where does this come from? (Actually it's `DUCTF{gl17ch_m3_n07_9c42a45d}`, but that's not the flag.)