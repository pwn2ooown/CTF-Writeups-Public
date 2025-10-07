'''
Shellcode loader
Main verification function
__int64 __fastcall sub_228EC4F0000(__int64 a1)
{
  int v2; // [rsp+14h] [rbp-BCh]
  int i; // [rsp+18h] [rbp-B8h]
  int j; // [rsp+1Ch] [rbp-B4h]
  int k; // [rsp+20h] [rbp-B0h]
  int m; // [rsp+24h] [rbp-ACh]
  int n; // [rsp+28h] [rbp-A8h]
  _QWORD v8[5]; // [rsp+30h] [rbp-A0h] BYREF
  int v9; // [rsp+58h] [rbp-78h]
  _QWORD v10[5]; // [rsp+60h] [rbp-70h] BYREF
  int v11; // [rsp+88h] [rbp-48h]
  _QWORD v12[5]; // [rsp+90h] [rbp-40h]
  int v13; // [rsp+B8h] [rbp-18h]
  char v14; // [rsp+BCh] [rbp-14h]

  memset(v8, 0, sizeof(v8));
  v9 = 0;
  memset(v10, 0, sizeof(v10));
  v11 = 0;
  for ( i = 0; i <= 42; i += 2 )
  {
    *((_BYTE *)v8 + i) = *(_BYTE *)(i + 1LL + a1);
    *((_BYTE *)v8 + i + 1) = *(_BYTE *)(i + a1);
  }
  for ( j = 0; j <= 43; j += 4 )
  {
    v2 = 0;
    for ( k = 0; k <= 3; ++k )
      v2 = (v2 << 8) | *((unsigned __int8 *)v8 + j + k);
    for ( m = 3; m >= 0; --m )
      *((_BYTE *)v10 + 3 - m + j) = (((2 * v2) ^ 0x94E590u) + 20) >> (8 * m);
  }
  v12[0] = 0x6E6732F63277168ALL;
  v12[1] = 0x426306DC420BFEF2LL;
  v12[2] = 0x5A5BFCC65C8956D8LL;
  v12[3] = 0x62397CD2602358EALL;
  v12[4] = 0x42230CD8142F2AE6LL;
  v13 = 0x6E1FF4C8;
  v14 = 0;
  for ( n = 0; n <= 43; ++n )
  {
    if ( *((_BYTE *)v10 + n) != *((_BYTE *)v12 + n) )
      return 0;
  }
  return 1;
}
'''

import struct

v12 = [
    0x6E6732F63277168A,
    0x426306DC420BFEF2,
    0x5A5BFCC65C8956D8,
    0x62397CD2602358EA,
    0x42230CD8142F2AE6,
    0x6E1FF4C8
]

target_bytes = b''.join(struct.pack('<Q', x) for x in v12)
target_bytes = target_bytes[:44]

input_bytes = bytearray(44)

for j in range(0, 44, 4):
    v10_chunk = int.from_bytes(target_bytes[j:j+4], 'big')
    temp = (v10_chunk - 20) & 0xFFFFFFFF
    temp ^= 0x94E590
    v2 = temp >> 1
    input_bytes[j:j+4] = v2.to_bytes(4, 'big')

for i in range(0, 44, 2):
    input_bytes[i], input_bytes[i+1] = input_bytes[i+1], input_bytes[i]

print(bytes(input_bytes).decode())