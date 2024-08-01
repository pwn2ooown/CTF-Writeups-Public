candidates = []
for i in range(-507,508):
	for j in range(-507,508):
		if i*i+j*j == 256325:
			candidates.append([i,j])
for candidate in candidates:
	x, y = candidate[0], candidate[1]
	z = y ** 3 - 3 ** x
	if x * z == y * 13910 + 441:
		print(x, y, z)
		print(y ** x % z)