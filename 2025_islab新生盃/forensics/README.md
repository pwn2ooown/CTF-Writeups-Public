# Forensics

## File Stealer

把 partition 2 打開翻一翻就有 flag 了

## File Stealer Revenge

把 partition 2 整陀去 xor `is1ab` (因為理論上 partition 要有一堆 null byte 卻被塞了一堆 is1ab 就有可能是 xor)

找出一張 qrcode 會有 flag

## File Stealer Revenge Revenge

把 partition 2 整陀去 xxd

`xxd partition2.raw | grep -v '0000 0000 0000 0000 0000 0000 0000 0000'`

然後根據觀察就能發現

```
00206000: 0050 4e47 0d0a 1a0a 0000 000d 4948 4452  .PNG........IHDR
00206010: 0000 0480 0000 0288 0803 0000 003f f571  .............?.q
00206020: 3f00 0000 0861 6354 4c00 0000 0200 0000  ?....acTL.......
00206030: 00f3 8d93 7000 0002 fd50 4c54 45fe fefe  ....p....PLTE...
...
00208800: d045 3770 592b cc33 abf2 3c1f 27a7 81e7  .E7pY+.3..<.'...
00208810: cbd4 9efa 272c 78a9 cf59 279a 529f c0d2  ....',x..Y'.R...
00208820: 3997 eb7f 6fef 537b 3f44 2fbc 86c7 9af4  9...o.S{?D/.....
00208830: 5ee9 ecda 5c6a c3b7 87af 5ab3 355c dd8f  ^...\j....Z.5\..
00208840: e2ff 0190 4f6d 1203 e7e6 2400 0000 0049  ....Om....$....I
00208850: 454e 44ae 4260 8200 0000 0000 0000 0000  END.B`..........
```

這應該是一張 PNG

把它抽出來 (修好 magic bytes) 後去 https://ezgif.com/apng-maker 把第二個 frame 抽出來就有 flag 了

## 這裡有人壞壞

找到有一個 process creation 的紀錄

`0:32:37.1922800","net1.exe","6976","Process Start","","SUCCESS","Parent PID: 2776, Command line: C:\Windows\system32\net1  user root Nimda@CYAdmin /add`
