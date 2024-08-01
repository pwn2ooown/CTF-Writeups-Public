import random

# seed = 252

for i in range(0, 1337):
	random.seed(i)
	flag = "DUCTF{" + 'A' * 54 + '}'
	assert len(flag) == 305 // 5
	out = ''.join(random.choices(flag, k=len(flag)*5))
	# print(out)
	# { [50, 225, 268]
	# } [32, 86, 198, 200, 232, 302]
	if out[50] == '{' and out[225] == '{' and out[268] == '{' and out[32] == '}' and out[86] == '}' and out[198] == '}' and out[200] == '}' and out[232] == '}' and out[302] == '}':
		print(i)