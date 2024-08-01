Use black to format the code.

There are tones of similiar structure. We want to find the difference.

We see that we have this suspicious snippet:

```python
.__getitem__(17106 ^ 17105)
.__pow__(8)
.__eq__(11716593810022656)
```

We may guess maybe it's actually `pow(flag[__getitem__data],__pow__data) = __eq__data`? In this case we have `flag[3] = 102 = ord('f')` and the `flag[3]` is `f`. Yeah!

Finally we use regex to extract out all the data like that, extract them out and solve this challenge. You can extract them out manually since there's only 51 characters XD.

`ictf{pYthOn_obFuScAtION_iS_N0_M4TCH_f0r_U_9e1b23f9}`