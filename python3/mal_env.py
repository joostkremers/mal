import mal_types


def mal_add(*args):
    """Sum numbers.

    If ARGS contains only one element, it is returned. If ARG is empty, the
    return value is 0.

    """
    return mal_types.MalInt(sum(map(lambda arg: arg.value, args)))


def mal_substract(*args):
    """Substract numbers.

    If ARG contains just a single element, it is negated. If ARG is empty, the
    return value is 0.

    """
    if len(args) > 1:
        first = args[0].value
        args = args[1:]
    else:
        first = 0

    for n in args:
        first -= n.value

    return mal_types.MalInt(first)


def mal_multiply(*args):
    """Multiply numbers.

    If args contains only one element, it is returned. If ARG is empty, the
    return value is 1.

    """
    if len(args) > 1:
        first = args[0].value
        args = args[1:]
    else:
        first = 1

    for n in args:
        first *= n.value

    return mal_types.MalInt(first)


def mal_divide(*args):
    """Divide numbers.

    If ARGS contains zero or one element(s), the return value is 0.

    """
    if len(args) > 1:
        first = args[0].value
        args = args[1:]
    else:
        first = 0

    for n in args:
        if n.value == 0:
            return mal_types.MalError("Arithmetic error", "Division by zero")
        first //= n.value

    return mal_types.MalInt(first)


repl_env = {'+': mal_types.MalFunction(mal_add),
            '-': mal_types.MalFunction(mal_substract),
            '*': mal_types.MalFunction(mal_multiply),
            '/': mal_types.MalFunction(mal_divide)}
