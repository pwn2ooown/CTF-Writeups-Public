import sys

# encoded_text = "DLSeGAGDgBNJDQJDCFSFnRBIDjgHoDFCFtHDgJpiHtGDmMAQFnRBJKkBAsTMrsPSDDnEFCFtIbEDtDCIbFCFtHTJDKerFldbFObFCFtLBFkBAAAPFnRBJGEkerFlcPgKkImHnIlATJDKbTbFOkdNnsgbnJRMFnRBNAFkBAAAbrcbTKAkOgFpOgFpOpkBAAAAAAAiClFGIPFnRBaKliCgClFGtIBAAAAAAAOgGEkImHnIl"
encoded_text = input()
encoded_text = encoded_text[::-1]
lookup1 = "\n \"#()*+/1:=[]abcdefghijklmnopqrstuvwxyz"
lookup2 = "ABCDEFGHIJKLMNOPQRSTabcdefghijklmnopqrst"



decoded_text = ""
prev = 0
cur_list = []
for char in encoded_text:
    cur = lookup2.index(char)
    # print("prev: {}, cur: {}".format(prev, cur))
    out_index = (cur + prev) % 40
    # print("out_index: {}".format(out_index))
    # print(cur)
    cur_list.append(cur)
    decoded_text += lookup1[out_index]
    prev = cur
    # print("prev is now",prev)
cur_list = cur_list[::-1]
# print(cur_list)

prev = 0
ooo = ""
for char in cur_list:
  cur  = (char + prev) % 40
  ooo += lookup1[cur]
  prev = cur
sys.stdout.write(ooo)
