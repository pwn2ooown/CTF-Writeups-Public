```c
struct node {
    char  data[0x60]; 
    struct node *next;  
    uint64_t len;
};
```

Overflow data buffer overwrite next to modprobe_path 