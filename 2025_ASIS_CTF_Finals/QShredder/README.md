# QShredder

Credit: @ElChals

## Short Writeup

1. Use oob write to overwrite the buf len to 0xff
2. Dump the OOB chunk data (encrypted using xor with 4 PRNGs) and recover the chunk to get heap leak 
3. Use oob write to overwrite function pointer