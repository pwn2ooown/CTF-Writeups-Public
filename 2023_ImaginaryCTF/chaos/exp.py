# firstline = input().split(' ')
# secondline = input()
# thirdline = input()
# assert len(firstline) == 3
# assert firstline[1] == '^'
# firstnum = int(firstline[0]) ^ int(firstline[2])
# secondnum = int(secondline)
# thirdnum = int(thirdline)
# print(chr(round(thirdnum**(1/secondnum))))
flag = [None for _ in range(51)]
for i in range(51):
    firstline = input().split(' ')
    secondline = input()
    thirdline = input()
    assert len(firstline) == 3
    assert firstline[1] == '^'
    firstnum = int(firstline[0]) ^ int(firstline[2])
    secondnum = int(secondline)
    thirdnum = int(thirdline)
    assert flag[firstnum] is None
    flag[firstnum] = round(thirdnum**(1/secondnum))
print(''.join(chr(i) for i in flag))
