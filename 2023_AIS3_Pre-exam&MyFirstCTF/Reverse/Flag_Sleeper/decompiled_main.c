__int64 __fastcall main(int a1, char **argv, char **a3)
{
  int v4; // eax
  int v5; // [rsp+1Ch] [rbp-364h]
  int index; // [rsp+20h] [rbp-360h]
  int v7; // [rsp+24h] [rbp-35Ch]
  int v8[52]; // [rsp+30h] [rbp-350h]
  int v9[52]; // [rsp+100h] [rbp-280h]
  int v10[52]; // [rsp+1D0h] [rbp-1B0h]
  int v11[54]; // [rsp+2A0h] [rbp-E0h] BYREF
  unsigned __int64 v12; // [rsp+378h] [rbp-8h]

  v12 = __readfsqword(0x28u);
  if ( a1 == 2 && strlen(argv[1]) == 52 )
  {
    v8[0] = 10;
    v8[1] = 12;
    v8[2] = 28;
    v8[3] = 7;
    v8[4] = 38;
    v8[5] = 31;
    v8[6] = 47;
    v8[7] = 44;
    v8[8] = 42;
    v8[9] = 35;
    v8[10] = 48;
    v8[11] = 30;
    v8[12] = 21;
    v8[13] = 11;
    v8[14] = 17;
    v8[15] = 16;
    v8[16] = 34;
    v8[17] = 40;
    v8[18] = 33;
    v8[19] = 39;
    v8[20] = 41;
    v8[21] = 9;
    v8[22] = 22;
    v8[23] = 4;
    v8[24] = 6;
    v8[25] = 20;
    v8[26] = 19;
    v8[27] = 46;
    v8[28] = 23;
    v8[29] = 45;
    v8[30] = 26;
    v8[31] = 0;
    v8[32] = 15;
    v8[33] = 3;
    v8[34] = 8;
    v8[35] = 43;
    v8[36] = 14;
    v8[37] = 5;
    v8[38] = 2;
    v8[39] = 27;
    v8[40] = 49;
    v8[41] = 1;
    v8[42] = 51;
    v8[43] = 36;
    v8[44] = 37;
    v8[45] = 24;
    v8[46] = 25;
    v8[47] = 50;
    v8[48] = 32;
    v8[49] = 13;
    v8[50] = 29;
    v8[51] = 18;
    v9[0] = 212;
    v9[1] = 232;
    v9[2] = 164;
    v9[3] = 28;
    v9[4] = 253;
    v9[5] = 132;
    v9[6] = 194;
    v9[7] = 47;
    v9[8] = 46;
    v9[9] = 150;
    v9[10] = 96;
    v9[11] = 216;
    v9[12] = 121;
    v9[13] = 216;
    v9[14] = 140;
    v9[15] = 164;
    v9[16] = 49;
    v9[17] = 219;
    v9[18] = 147;
    v9[19] = 252;
    v9[20] = 201;
    v9[21] = 28;
    v9[22] = 9;
    v9[23] = 188;
    v9[24] = 155;
    v9[25] = 79;
    v9[26] = 133;
    v9[27] = 255;
    v9[28] = 104;
    v9[29] = 20;
    v9[30] = 87;
    v9[31] = 64;
    v9[32] = 147;
    v9[33] = 143;
    v9[34] = 68;
    v9[35] = 147;
    v9[36] = 142;
    v9[37] = 96;
    v9[38] = 165;
    v9[39] = 244;
    v9[40] = 62;
    v9[41] = 58;
    v9[42] = 119;
    v9[43] = 25;
    v9[44] = 61;
    v9[45] = 56;
    v9[46] = 71;
    v9[47] = 182;
    v9[48] = 7;
    v9[49] = 37;
    v9[50] = 1;
    v9[51] = 154;
    v10[0] = 237;
    v10[1] = 217;
    v10[2] = 212;
    v10[3] = 40;
    v10[4] = 149;
    v10[5] = 219;
    v10[6] = 165;
    v10[7] = 112;
    v10[8] = 29;
    v10[9] = 241;
    v10[10] = 8;
    v10[11] = 189;
    v10[12] = 13;
    v10[13] = 224;
    v10[14] = 211;
    v10[15] = 149;
    v10[16] = 5;
    v10[17] = 184;
    v10[18] = 255;
    v10[19] = 207;
    v10[20] = 162;
    v10[21] = 122;
    v10[22] = 86;
    v10[23] = 199;
    v10[24] = 170;
    v10[25] = 122;
    v10[26] = 240;
    v10[27] = 206;
    v10[28] = 9;
    v10[29] = 102;
    v10[30] = 102;
    v10[31] = 1;
    v10[32] = 163;
    v10[33] = 188;
    v10[34] = 119;
    v10[35] = 225;
    v10[36] = 239;
    v10[37] = 3;
    v10[38] = 246;
    v10[39] = 153;
    v10[40] = 9;
    v10[41] = 115;
    v10[42] = 10;
    v10[43] = 70;
    v10[44] = 94;
    v10[45] = 103;
    v10[46] = 52;
    v10[47] = 137;
    v10[48] = 97;
    v10[49] = 29;
    v10[50] = 109;
    v10[51] = 208;
    memset(v11, 0, 208uLL);
    v5 = 0;
    v4 = time(0LL);
    srand(v4 + 0x303030);
    while ( v5 != 52 )
    {
      index = rand() % 52;
      v7 = v8[index];
      if ( argv[1][v7] != (v10[index] ^ v9[index]) )
      {
        puts(&fail_banner);
        return 1LL;
      }
      if ( !v11[v7] )
        ++v5;
      ++v11[v7];
      sleep(1u);
    }
    puts(&byte_2041);
    return 0LL;
  }
  else
  {
    puts(&fail_banner);
    return 1LL;
  }
}