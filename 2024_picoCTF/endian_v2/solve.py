with open("challengefile","rb") as f:
    res = f.read()
    count = 0
    for i in range(0, len(res), 4):
        count += 1
        print(res[i:i+4][::-1])
        with open("challengefile2","ab") as f:
            f.write(res[i:i+4][::-1])

