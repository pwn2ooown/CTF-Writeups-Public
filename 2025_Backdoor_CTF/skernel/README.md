# skernel

Credit to @ElChals and @nirvanaK!

## Short Writeup

Bug:

```c
case 0x13371338:                          // IOCTL free
    memset(kern_buf, 0, sizeof(kern_buf));
    v5 = allocated_objects[(int)idx];
    if ( v5 )
    {
        kfree(v5);
        copy_from_user(kern_buf, usr_buf, 64);// race condition, fallocate blocks here
                                            // spray pipe_buffer
                                            // immediately write (UAF on pipe_buffer)
        allocated_objects[(int)idx] = 0;
    }
    break;
```

1. Use [Extending Kernel Race Windows Using '/dev/shm'](https://faith2dxy.xyz/2025-11-28/extending_race_window_fallocate/)
2. Spray pipe buffer and use UAF write to write a null byte to `struct page *page; ` ([PageJack](https://i.blackhat.com/BH-US-24/Presentations/US24-Qian-PageJack-A-Powerful-Exploit-Technique-With-Page-Level-UAF-Thursday.pdf))
3. Backdoor `/bin/busybox` binary