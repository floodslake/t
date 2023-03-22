BASE_ALPH = tuple("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
BASE_DICT = dict((c, v) for v, c in enumerate(BASE_ALPH))
BASE_LEN = len(BASE_ALPH)

def base_decode(string):
    num = 0
    for char in string:
        num = num * BASE_LEN + BASE_DICT[char]
    return num

def base_encode(num):
    if not num:
        return BASE_ALPH[0]

    encoding = ""
    while num:
        num, rem = divmod(num, BASE_LEN)
        encoding = BASE_ALPH[rem] + encoding
    return encoding

def convert(num, base=2):
    assert base <= len(BASE_ALPH), f"Unable to convert to base {base}"
    converted = ""
    while num > 0:
        converted += BASE_ALPH[num % base]
        num //= base

    if len(converted) == 0:
        return "0"
    return converted[::-1]

def unix2base62():
    import time
    ms = int( time.time() )
    return base_encode(ms)

def timename():
    return unix2base62()