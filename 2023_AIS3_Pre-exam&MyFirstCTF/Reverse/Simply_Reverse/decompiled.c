_BOOL8 __fastcall verify(__int64 a1) {
  int i;  // [rsp+14h] [rbp-4h]

  for (i = 0; *(_BYTE *)(i + a1); ++i) {
    if (encrypted[i] != ((unsigned __int8)((i ^ *(unsigned __int8 *)(i + a1))
                                           << ((i ^ 9) & 3)) |
                         (unsigned __int8)((i ^ *(unsigned __int8 *)(i + a1)) >>
                                           (8 - ((i ^ 9) & 3)))) +
                            8)
      return 0LL;
  }
  return i == 34;
}