encrypted = [
    0x8A,
    0x50,
    0x92,
    0xC8,
    0x06,
    0x3D,
    0x5B,
    0x95,
    0xB6,
    0x52,
    0x1B,
    0x35,
    0x82,
    0x5A,
    0xEA,
    0xF8,
    0x94,
    0x28,
    0x72,
    0xDD,
    0xD4,
    0x5D,
    0xE3,
    0x29,
    0xBA,
    0x58,
    0x52,
    0xA8,
    0x64,
    0x35,
    0x81,
    0xAC,
    0x0A,
    0x64,
    0x00,
]
print(len(encrypted))
cnt = 0
for i in range(len(encrypted)):
    for j in range(128):
        # print(i,j,(((i ^ (j)) << ((i ^ 9) & 3)) | ((i ^ (j)) >> (8 - ((i ^ 9) & 3)))) + 8)
        if (
            encrypted[i]
            == (
                ((i ^ (i + j)) << ((i ^ 9) & 3))
                | ((i ^ (i + j)) >> (8 - ((i ^ 9) & 3)))
            )
            % 256
            + 8
        ):
            print(chr(i + j), end="")
            cnt += 1
print("\nLen = ", cnt)

"""
$ python3 solve.py
35
AIS30ld_Ch@1_R3V1_fr@m_AIS32016!}
Len =  33
Can guess the flag is AIS3{0ld_Ch@1_R3V1_fr@m_AIS32016!}
"""
