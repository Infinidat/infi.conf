def assign_path(conf, path, value):
    path, key = path.rsplit(".", 1)
    conf = get_path(conf, path)
    conf[key] = value

def assign_path_expression(conf, expr, deduce_type=False):
    path, value = expr.split("=", 1)
    if deduce_type:
        leaf_type = type(get_path(conf, path))
    else:
        leaf_type = str
    assign_path(conf, path, leaf_type(value))

def get_path(conf, path):
    returned = conf
    path = path.split(".")
    for p in path:
        returned = returned[p]
    return returned
