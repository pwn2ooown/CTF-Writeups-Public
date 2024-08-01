# Micro-CMS v1


So it provided a website that user can create markdown posts. With 4 hidden flags.

## Flag 1

The script tag is disabled. However, there are many ways to bypass it to make XSS attack. [Ref](https://stackoverflow.com/questions/37435077/execute-javascript-for-xss-without-script-tags)

So we can use `<img src=0 onerror=alert(1)>`, boom! This is correct. We inject the title and context and after popping the alert window, we can get the flag by clicking Go Home button.

## Flag 2

We see the source of the created page, and the image tag has been modified: `<img src=0 flag=... onerror=alert(1)>`.
## Flag 3

We observe that when we edit, the directory became `.../page/edit/[some number]`, and we can enumerate the number to 6 and find a hidden post edit.

## Flag 4

So far I have no idea, I tried to get shell(?) but it's not that east.
I read the editorial and found out that the `.../page/edit/[some number]` can lead to sql injection. And the payload is `.../page/edit/[some number]'` (with a quotation mark)

## Postscript

I have to say, the website sucks! The preparing time for sandbox is too long and has some weird bug!(Fail to open the website sometimes)


Hmm, I think the source code of this website is really cool... Detect XSS, detect SQL injection...
