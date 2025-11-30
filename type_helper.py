def to_int(object):
    try:
        return int(object)
    except ValueError:
        print(f"[Error 1] | Faild to convert {type(object)} to int")
        return object
def to_list(object):
    try:
        return list(object)
    except ValueError:
        print(f"[Error 1] | Faild to convert {type(object)} to list")
        return object
def to_bool(object):
    try:
        return bool(object)
    except ValueError:
        print(f"[Error 1] | Faild to convert {type(object)} to bool")
        return object
def to_str(object):
    try:
        return str(object)
    except ValueError:
        print(f"[Error 1] | Faild to convert {type(object)} to str")
        return object

def is_callable(object):
    b = callable(object)
    if not b:
        print(f"[Error 1] | {type(object)} is not callable")
    return b
