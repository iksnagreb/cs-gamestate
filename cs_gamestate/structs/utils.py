# Tests whether an object is either None or an instance of type cls
def none_or_isinstance(obj, cls):
    return obj is None or isinstance(obj, cls)
