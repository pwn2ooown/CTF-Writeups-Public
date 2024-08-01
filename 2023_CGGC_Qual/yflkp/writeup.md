這題的 vulnerable ko file 的 read / write 長度都是無限的，所以當然 ROP 最簡單粗暴。
有開 smep 跟 smap 但是沒有 kaslr，所以簡單了一點(但是因為我們有無限 leak 所以有沒有 kaslr 其實沒差)。
要注意 kernel 6.2 之後不能再用 `commit_creds(prepare_kernel_cred(0))` 來提權了，要用 `modprobe_path` 來提權。
最後就是找 gadget 把 modprobe_path 蓋掉之後用 `kpti_trampoline` 回到 user space 執行一個 invalid elf，and we're root。
要注意用 ropper 找出來的 gadget 有一大堆都是在沒有執行權限的 segment 上，所以要手動篩選一下。
`kbti_trampoline` 在 `swapgs_restore_regs_and_return_to_usermode` 不過 offset 不是 22 (網路上教學都是跳到 + 22)，但是比對一下兩邊的 code 就可以找到相同的部分了。
用 musl-gcc 編譯 exploit，因為體積比較小。
然後最麻煩的是上傳，因為 terminal buffer 的關係導致沒辦法一次複製貼上，所以我採用 base64 + 分段上傳的方式。
Pwntools 的 IO 會怪怪的，要開 debug mode 才看的到。
整體來說觀念不難，但是實作要注意的地方很多，所以還是有點難度。
BTW, yflkp 應該是指 your first linux kernel pwn。
