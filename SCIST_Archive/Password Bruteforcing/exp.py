import hashlib

wordlist = open('password_list', 'r').read().splitlines()

target = "cc3ecde41ff425296f9ea008b8a8ba3a2282fc042672f77ab2681426ea9dbabc"

for word in wordlist:
    if hashlib.sha256(word.encode()).hexdigest() == target:
        print("SCIST{" + word + "}")
        break