#!/usr/local/bin/python

l = """
░█████╗░███████╗░██████╗░██╗░██████╗ Jail Final
██╔══██╗██╔════╝██╔════╝░██║██╔════╝
███████║█████╗░░██║░░██╗░██║╚█████╗░
██╔══██║██╔══╝░░██║░░╚██╗██║░╚═══██╗
██║░░██║███████╗╚██████╔╝██║██████╔╝ Type "hint" to see source!
╚═╝░░╚═╝╚══════╝░╚═════╝░╚═╝╚═════╝░ The secret is in flag.txt"""
print(l)
limit = 70

i = input("AEGIS> ")[:71]
if 'hint' in i:
    print(__import__('os').system('cat jail.py'))
    exit()
if len(i)>limit:
    print(f"You've entered too many characters. The maximum limit is {limit}.")
    exit()
try:
    print(eval(i, {"__builtins__": {}}, {"__builtins__": {}}))
except Exception as e:
    print("Good luck next time!", e)
exit()

# I think the solution is to find a class with shorter escape path that can read flag.txt file.
# I forget which class, this was solved by Vincent55