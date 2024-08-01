res = [
        n
        for n in ().__class__.__base__.__subclasses__()
        if "rni" in n.__name__ and n.__name__ == n.__name__.lower()
    ]
print(res)