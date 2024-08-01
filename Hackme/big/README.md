# Big Writeup

```bash
time xzcat big.xz | grep -v "THISisNOT"
FLAG{Redacted}
xzcat big.xz  26.49s user 5.80s system 95% cpu 33.828 total
grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn,.idea,.tox} -v   23.03s user 3.57s system 78% cpu 33.828 total
```

Unzip the file two times.

Notice that the second file is 16GB, since there's a lot of garbage at the beginning of the file.(most of the file are "THISisNOTFLAG{}")

TODO: modify xz file to ignore the garbage at the beginning of the zip.
