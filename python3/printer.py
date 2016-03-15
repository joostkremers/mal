import mal_types as mtype


def pr_str(object, print_readably=False):
    if isinstance(object, list):
        str_list = [pr_str(s, print_readably) for s in object]
        return '(' + ' '.join(str_list) + ')'

    elif isinstance(object, mtype.Vector):
        str_list = [pr_str(s, print_readably) for s in object.value]
        return '[' + ' '.join(str_list) + ']'

    elif isinstance(object, bool):
        if object is True:
            return "true"
        else:
            return "false"

    elif isinstance(object, str):
        string = object
        if print_readably:
            string = string.replace('\\', r'\\')
            string = string.replace('\n', r'\n')
            string = string.replace('"', r'\"')
            string = '"' + string + '"'
        return string

    else:
        return str(object)
