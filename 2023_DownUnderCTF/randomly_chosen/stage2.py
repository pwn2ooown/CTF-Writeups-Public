import random

goal = "bDacadn3af1b79cfCma8bse3F7msFdT_}11m8cicf_fdnbssUc{UarF_d3m6T813Usca?tf_FfC3tebbrrffca}Cd18ir1ciDF96n9_7s7F1cb8a07btD7d6s07a3608besfb7tmCa6sasdnnT11ssbsc0id3dsasTs?1m_bef_enU_91_1ta_417r1n8f1e7479ce}9}n8cFtF4__3sef0amUa1cmiec{b8nn9n}dndsef0?1b88c1993014t10aTmrcDn_sesc{a7scdadCm09T_0t7md61bDn8asan1rnam}sU"
print(goal)
random.seed(252)
flag = "DUCTF{" + 'is_r4nd0mn3ss_d3t3rm1n1st1c?_cba67ea78f19bcaefd9068f1a' + '}'
assert len(flag) == 305 // 5
out = ''.join(random.choices(flag, k=len(flag)*5))
print(out)
assert len(goal) == len(out)
for i in range(len(goal)):
	if(goal[i] != out[i]):
		print(i,goal[i],out[i])
print(flag)
# { [50, 225, 268]
# } [32, 86, 198, 200, 232, 302]