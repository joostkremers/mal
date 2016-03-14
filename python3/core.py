import mal_types as mal


def mal_add(*args):
    """Sum numbers.

    If ARGS contains only one element, it is returned. If ARG is empty, the
    return value is 0.

    """
    return mal.Int(sum(map(lambda arg: arg.value, args)))


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

    return mal.Int(first)


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

    return mal.Int(first)


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
            return mal.Error("Arithmetic error", "Division by zero")
        first //= n.value

    return mal.Int(first)


def mal_list(*args):
    return mal.List(list(args))


def mal_listp(arg):
    if arg.type == "list":
        return mal.Boolean(True)
    else:
        return mal.Boolean(False)


def mal_emptyp(arg):
    if arg.type in ["list", "vector"]:
        if arg.value == []:
            return mal.Boolean(True)
        else:
            return mal.Boolean(False)
    else:
        return mal.Error("ArgError",
                         "Wrong type argument: "
                         "expected list, got {}".format(arg.type))


def mal_count(arg):
    if arg.type in ["list", "vector"]:
        return mal.Int(len(arg.value))
    elif arg.type == "nil":
        return mal.Int(0)
    else:
        return mal.Error("ArgError",
                         "Wrong type argument: "
                         "expected list, got {}".format(arg.type))


def mal_equal(*args):
    first = args[0]
    for arg in args[1:]:
        if arg != first:
            return mal.Boolean(False)

    return mal.Boolean(True)


def mal_less(*args):
    for i in range(len(args)-1):
        if args[i].type != "integer":
            return mal.Error("ArgError",
                             "Wrong type argument: "
                             "expected number, got {}".format(args[i].type))
        if not args[i].value < args[i+1].value:
            return mal.Boolean(False)
    return mal.Boolean(True)


def mal_less_or_equal(*args):
    for i in range(len(args)-1):
        if args[i].type != "integer":
            return mal.Error("ArgError",
                             "Wrong type argument: "
                             "expected number, got {}".format(args[i].type))
        if not args[i].value <= args[i+1].value:
            return mal.Boolean(False)
    return mal.Boolean(True)


def mal_greater(*args):
    for i in range(len(args)-1):
        if args[i].type != "integer":
            return mal.Error("ArgError",
                             "Wrong type argument: "
                             "expected number, got {}".format(args[i].type))
        if not args[i].value > args[i+1].value:
            return mal.Boolean(False)
    return mal.Boolean(True)


def mal_greater_or_equal(*args):
    for i in range(len(args)-1):
        if args[i].type != "integer":
            return mal.Error("ArgError",
                             "Wrong type argument: "
                             "expected number, got {}".format(args[i].type))
        if not args[i].value >= args[i+1].value:
            return mal.Boolean(False)
    return mal.Boolean(True)


# core namespace
ns = {'+':      mal.Function(mal_add),
      '-':      mal.Function(mal_substract),
      '*':      mal.Function(mal_multiply),
      '/':      mal.Function(mal_divide),
      'list':   mal.Function(mal_list),
      'list?':  mal.Function(mal_listp),
      'empty?': mal.Function(mal_emptyp),
      'count':  mal.Function(mal_count),
      '=':      mal.Function(mal_equal),
      '<':      mal.Function(mal_less),
      '<=':     mal.Function(mal_less_or_equal),
      '>':      mal.Function(mal_greater),
      '>=':     mal.Function(mal_greater_or_equal)}
