
#!/usr/bin/env python3
import numpy as np
from PIL import Image
import pytesseract
import string
h, w = 100, 600
arr = np.zeros([h,w])
for i in range(h):
    for j in range(w):
        arr[i][j] = 0
coor_list = open('coordinates.txt', 'r').read().splitlines()
for coor in coor_list:
	arr[int(coor.split(" ")[1])][int(coor.split(" ")[0])] = 255
img = Image.fromarray(np.uint8(arr),"L")
text = pytesseract.image_to_string(img, lang='eng',config='--psm 6')
print(text)
img.save("flag.png")