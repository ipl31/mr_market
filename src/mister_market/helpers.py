

def get_public_methods(object):
    methods = []
    for method_name in dir(object):
        if method_name.startswith("__"):
            continue
        if method_name.startswith("_"):
            continue
        if callable(getattr(object, method_name)):
            methods.append(str(method_name))
    return methods
