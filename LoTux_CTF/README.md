# Some random writeups

[https://lotuxctf.com/](https://lotuxctf.com/)

Flag Format : `LoTuX{.*}`

I won't share the flag here. And if the official writeup is released, I won't show the details here.

## Welcome

### Welcome

Walkthrough all the blocks to show all the blocks.

By some code auditing, there's actually a cheating function in the code. We can get the flag by input `autoMove()` in the console.

Right click and F12 is banned, how can we open developer tools? Find it out by yourself!

### Discord

Join the discord server and get the flag.

## Pwn

### ASAP

Simple pwntools practice.

[WP](https://hackmd.io/@LoTuX-CTF/ASAP_EN)

### Tears of the Kingdom (Lite)

Simple buffer overflow.

### Skewer Shop

Stack pivoting. Learned a lot of details from writeup. Nice problem.

Notice that the place of fake stack has to be big enough, otherwise when you are calling system, you'll reach somewhere cannot write value and dies.

Or you can use one gadget (My first solution after I found out I cannot call `system('/bin/sh')`). Shell out.

I'll share my script later

[WP](https://hackmd.io/@LoTuX-CTF/Skewer_Shop_EN)

## Crypto

I don't know how to solve crypto problems. I'm so weak.

### How Is Your Math

I just read the writeup.

[WP](https://hackmd.io/@LoTuX-CTF/How_Is_Your_Math_EN)

### Ultra Easy RSA

Just use [this](https://github.com/RsaCtfTool/RsaCtfTool/tree/master).

[WP](https://hackmd.io/@LoTuX-CTF/Ultra_Easy_RSA_EN)

### Secure Store GPT

Reading WP again.

[WP](https://hackmd.io/@LoTuX-CTF/Secure_Store_GPT_EN)

## Reverse

### rev C 1

Too easy.

[WP](https://hackmd.io/@LoTuX-CTF/RevC1_EN)

### rev C 2

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char v4[4]; // [rsp+28h] [rbp-58h] BYREF
  char v5[30]; // [rsp+2Ch] [rbp-54h] BYREF
  char FLAG_prefix[6]; // [rsp+4Ah] [rbp-36h] BYREF
  int v7[18]; // [rsp+50h] [rbp-30h] BYREF
  int v8; // [rsp+98h] [rbp+18h] BYREF
  char tmp_char; // [rsp+9Eh] [rbp+1Eh]
  char a_char_from_FLAG; // [rsp+9Fh] [rbp+1Fh]
  FILE *FLAG; // [rsp+A0h] [rbp+20h]
  FILE *Stream; // [rsp+A8h] [rbp+28h]
  int m; // [rsp+B0h] [rbp+30h]
  int k; // [rsp+B4h] [rbp+34h]
  int j; // [rsp+B8h] [rbp+38h]
  int i; // [rsp+BCh] [rbp+3Ch]

  _main();
  puts("====FLAG GENERATOR====");
  puts("Menu:\n(1) create an fake flag.txt\n(2) generate flag");
  scanf("%d", &v8);
  if ( v8 != 1 && v8 != 2 )
    return 0;
  if ( v8 == 1 )
  {
    Stream = fopen("flag.txt", "w");
    fwrite("AAAAAAAAAAAAAAAAAA", 1ui64, 022ui64, Stream);
    fclose(Stream);
    puts("Generated!");
    scanf("%d", v4);
    return 0;
  }
  else
  {
    FLAG = fopen("flag.txt", "r");
    memset(v7, 0, sizeof(v7));
    v7[0] = 5;
    v7[1] = 13;
    v7[3] = 12;
    v7[4] = 1;
    v7[5] = 16;
    v7[6] = 3;
    v7[7] = 2;
    v7[8] = 8;
    v7[9] = 7;
    v7[10] = 15;
    v7[11] = 4;
    v7[12] = 6;
    v7[13] = 17;
    v7[14] = 11;
    v7[15] = 10;
    v7[16] = 9;
    qmemcpy(FLAG_prefix, "LoTuX{", sizeof(FLAG_prefix));
    for ( i = 0; ; ++i )
    {
      a_char_from_FLAG = fgetc(FLAG);
      if ( a_char_from_FLAG == -1 )
        break;
      v5[i + 4] = a_char_from_FLAG;
    }
    fclose(FLAG);
    for ( j = 0; j <= 17; ++j )
    {
      tmp_char = v5[j + 4];
      v5[j + 4] = v5[v7[j] + 4];
      v5[v7[j] + 4] = tmp_char;
    }
    for ( k = 0; k <= 5; ++k )
      putchar(FLAG_prefix[k]);
    for ( m = 0; m <= 17; ++m )
      putchar(v5[m + 4]);
    putchar('}');
    scanf("%d", v5);
    return 0;
  }
}
```

Some swapping algorithm. So you can enter ABCDEFGHIJKLMNOPQR to view the result of swapping and restore the original flag.

### rev C 3

A username and password checker. Username is easy to find out. (That is the first part of flag.)

Password is not important, just patch it. After the password it will restore the flag by many complicated function calls. Wait for it and print the real flag. 

### Heart Jack's Quiz

Writeup time. Nice unity problem.

[WP](https://hackmd.io/@LoTuX-CTF/HeartJacksQuiz_EN)

### BlockNinja

The game is impossible to pass, we need to cheat by dnspy. Data->Managed->Assembly-CSharp.dll

I patched the isGrounded to true so that I can jump infinitely. And I add the speed `this.moveSpeed = 20f;`. The most important part is patch `OnCollisionEnter2D` to always destroy the gameObject when touching the object. (remove if condition) Finally, you can pass the game and get the flag. The flag is falling from the sky quickly so I use screen recording and replay to get the flag.

## Web

### HTML

Easy.

[WP](https://hackmd.io/@LoTuX-CTF/HTML_EN)

### Useful Tools

Easy. Just use the tools.

Learn more about curl 

curl -I -X H1DD3N_HT7P_ME7H0D http://lotuxctf.com:20001/cur1_ch4ll3nge
I for head only
X for method and OPTIONS to view all methods
v for verbose

Curl uses User-Agent: curl/7.81.0

Python request modifies user agent to something like python-requests/2.18.4 Just modify it

So this challenge can all be done using burp by modifying the UA.

[WP](https://hackmd.io/@LoTuX-CTF/Useful_Tools_EN)

### THE EYE 2

From the `robots.txt`, we know where is the source code.

```python
from flask import Flask, session, redirect, render_template
import os

DATABASE = 'EYE.db'

app = Flask(__name__)
app.secret_key = os.urandom(3)

@app.route('/admin')
def admin():
    if not 'username' in session:
        return redirect('/')
    if session['username'] != 'admin':
        return redirect('/')
    return render_template('admin.html')
```

Brute force the secret key ($256^3$) and forge a fake cookie session to get the flag.

## Misc

### ChatBot

There 3 parts of flag.

First part: Description of bot says say `hello` to it, we have

```text
How can I help you? 
(A)Are you a robot? (B)What can you do? (C)Give me the flag!
```

Be creative, we can input `E` to get the first part of flag. (We guess there's an extra option)

Second part: The bot description says `Please be polite.`, please?

We can get the second part of flag by input `please`.

Third part is according to the hint: Who can give me the sauce cord?

source code! We can get the third part of flag by input `source code`.

### GameBot

There are two levels in this challenge. The first level is easy.

Second part our character and destination is much longer than ten steps, so we can't arrive the destination in 10 steps?

Accoring to hint:

```python
if(max_vote != 0):
	if(max_vote == vote_arr[i][0]):
		result += 'w'
	if(max_vote == vote_arr[i][1]):
		result += 's'
	if(max_vote == vote_arr[i][2]):
		result += 'a'
	if(max_vote == vote_arr[i][3]):
		result += 'd'
```

The vulnerability is obvious: if a step has the max vote more than two kinds, all of them will be added to result. Like if d and s has same vote in the first step, result will walk two steps in the first step.

### THE EYE 1

First blood!

Second part of flag is in the session data after login using sql injection. What about the second part? Why this is in the misc challenge?

Misc... picture problem? The first part is actually a steganography challenge. Use stegsolve to get the first part of flag from the picture on the website.

### 吾有一圖

Notice that if your zip is broken after binwalk, use winrar to fix it. `zip -FF` won't work.

[WP](https://hackmd.io/@LoTuX-CTF/%E5%90%BE%E6%9C%89%E4%B8%80%E5%9C%96_EN)
