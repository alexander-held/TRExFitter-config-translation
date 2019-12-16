def is_int(s):
    try:
        int(s)
        return True
    except:
        return False

def is_float(s):
    try:
        float(s)
        return True
    except:
        return False

def translate_value(s):
    if is_int(s):
        return int(s)
    elif is_float(s):
        return float(s)
    else:
        return s
