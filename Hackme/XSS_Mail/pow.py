import hashlib
import sys

target = "00000"
prefix = sys.argv[1]

counter = 0
while True:
    data = prefix + str(counter)
    hash_value = hashlib.md5(data.encode()).hexdigest()
    if hash_value[:len(target)] == target:
        break
    counter += 1

print(counter)