
import itertools
from Crypto.Util.number import long_to_bytes

# List of prime divisors
prime_divisors = [2,3,19,31,83,3331,165219437,550618493,66969810339969829,1168302403781268101731523384107546514884411261]



goal = 6954494065942554678316751997792528753841173212407363342283423753536991947310058248515278

tmp = 1

# Sanity check

for div in prime_divisors:
	tmp *= div
assert tmp == goal
# Step 1: Enumerate the multiplication of factors
factor_combinations = []
for r in range(1, len(prime_divisors) + 1):
    factor_combinations.extend(itertools.combinations(prime_divisors, r))

results = []
for factors in factor_combinations:
    result = 1
    for factor in factors:
        result *= factor
    results.append(result)

# Step 2: Convert the result to bytes using long_to_bytes
byte_results = []
for result in results:
    byte_result = long_to_bytes(result)
    byte_results.append(byte_result)

# Step 3: Check if "DUCTF{" is in the factor
for i, byte_result in enumerate(byte_results):
    if b"DUCTF{" in byte_result:
        print("Found 'DUCTF{' in one of the factors:", byte_result.decode('utf-8', 'ignore'))
        print("Factors of the corresponding number:", results[i])
        print("The rest of flag is:",long_to_bytes(goal // results[i]))
        break

# 2*3*19*31*83*3331*165219437*550618493 * 66969810339969829*1168302403781268101731523384107546514884411261