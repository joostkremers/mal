import re


def pr_str(object, print_readably=False):
    if isinstance(object, list):
        str_list = [pr_str(s, print_readably) for s in object]
        return '(' + ' '.join(str_list) + ')'

    elif isinstance(object, bool):
        if object is True:
            return "true"
        else:
            return "false"

    elif isinstance(object, str):
        if print_readably:
            return object.__str__()
        else:
            string = object.__repr__()
            if string[0] == '"':
                return string
            else:
                string = re.sub(r"\'", r"'", string)
                string = re.sub(r'"', r'\"', string)
                return '"' + object[1:-1] + '"'

    else:
        return str(object)
