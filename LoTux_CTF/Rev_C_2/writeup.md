```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char v4[4]; // [rsp+28h] [rbp-58h] BYREF
  char v5[30]; // [rsp+2Ch] [rbp-54h] BYREF
  char FLAG_prefix[6]; // [rsp+4Ah] [rbp-36h] BYREF
  int v7[18]; // [rsp+50h] [rbp-30h] BYREF
  int v8; // [rsp+98h] [rbp+18h] BYREF
  char tmp_char; // [rsp+9Eh] [rbp+1Eh]
  char a_char_from_FLAG; // [rsp+9Fh] [rbp+1Fh]
  FILE *FLAG; // [rsp+A0h] [rbp+20h]
  FILE *Stream; // [rsp+A8h] [rbp+28h]
  int m; // [rsp+B0h] [rbp+30h]
  int k; // [rsp+B4h] [rbp+34h]
  int j; // [rsp+B8h] [rbp+38h]
  int i; // [rsp+BCh] [rbp+3Ch]

  _main();
  puts("====FLAG GENERATOR====");
  puts("Menu:\n(1) create an fake flag.txt\n(2) generate flag");
  scanf("%d", &v8);
  if ( v8 != 1 && v8 != 2 )
    return 0;
  if ( v8 == 1 )
  {
    Stream = fopen("flag.txt", "w");
    fwrite("AAAAAAAAAAAAAAAAAA", 1ui64, 022ui64, Stream);
    fclose(Stream);
    puts("Generated!");
    scanf("%d", v4);
    return 0;
  }
  else
  {
    FLAG = fopen("flag.txt", "r");
    memset(v7, 0, sizeof(v7));
    v7[0] = 5;
    v7[1] = 13;
    v7[3] = 12;
    v7[4] = 1;
    v7[5] = 16;
    v7[6] = 3;
    v7[7] = 2;
    v7[8] = 8;
    v7[9] = 7;
    v7[10] = 15;
    v7[11] = 4;
    v7[12] = 6;
    v7[13] = 17;
    v7[14] = 11;
    v7[15] = 10;
    v7[16] = 9;
    qmemcpy(FLAG_prefix, "LoTuX{", sizeof(FLAG_prefix));
    for ( i = 0; ; ++i )
    {
      a_char_from_FLAG = fgetc(FLAG);
      if ( a_char_from_FLAG == -1 )
        break;
      v5[i + 4] = a_char_from_FLAG;
    }
    fclose(FLAG);
    for ( j = 0; j <= 17; ++j )
    {
      tmp_char = v5[j + 4];
      v5[j + 4] = v5[v7[j] + 4];
      v5[v7[j] + 4] = tmp_char;
    }
    for ( k = 0; k <= 5; ++k )
      putchar(FLAG_prefix[k]);
    for ( m = 0; m <= 17; ++m )
      putchar(v5[m + 4]);
    putchar('}');
    scanf("%d", v5);
    return 0;
  }
}
```

ABCDEFGHIJKLMNOPQR
LoTuX{BEHGLQDJIAKOMRNPFC}
LoTuX{E4sy_C_eXe_for_you}
LoTuX{4_e_foyeXE__ouryCs}
