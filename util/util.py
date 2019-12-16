def is_int(s):
    """check whether input string can be converted to an integer"""
    try:
        int(s)
        return True
    except:
        return False


def is_float(s):
    """check whether input string can be converted to a float"""
    try:
        float(s)
        return True
    except:
        return False


def translate_value(s):
    """translate string to integer or float if applicable"""
    if is_int(s):
        return int(s)
    elif is_float(s):
        return float(s)
    else:
        return s
