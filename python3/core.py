import mal_types as mal
import printer


# Arithmetic functions


def mal_add(*args):
    """Sum numbers.

    If ARGS contains only one element, it is returned. If ARG is empty, the
    return value is 0.

    """
    try:
        res = sum(args)
    except TypeError:
        return mal.Error("ArgError", "'+': Wrong type argument")

    return res


def mal_substract(*args):
    """Substract numbers.

    If ARG contains just a single element, it is negated. If ARG is empty, the
    return value is 0.

    """
    if len(args) > 1:
        first = args[0]
        args = args[1:]
    else:
        first = 0

    try:
        for n in args:
            first -= n
    except TypeError:
        return mal.Error("ArgError", "'-': Wrong type argument")

    return first


def mal_multiply(*args):
    """Multiply numbers.

    If args contains only one element, it is returned. If ARG is empty, the
    return value is 1.

    """
    if len(args) > 1:
        first = args[0]
        args = args[1:]
    else:
        first = 1

    try:
        for n in args:
            first *= n
    except TypeError:
        return mal.Error("ArgError", "'*': Wrong type argument")

    return first


def mal_divide(*args):
    """Divide numbers.

    If ARGS contains zero or one element(s), the return value is 0.

    """
    if len(args) > 1:
        first = args[0]
        args = args[1:]
    else:
        first = 0

    try:
        for n in args:
            first //= n
    except ZeroDivisionError:
        return mal.Error("ArithmeticError", "Division by zero")
    except TypeError:
        return mal.Error("ArgError", "'/': Wrong type argument")

    return first


# comparison functions


def mal_equal(*args):
    first = args[0]
    for arg in args[1:]:
        if arg != first:
            return False

    return True


def mal_less(*args):
    for i in range(len(args)-1):
        if not isinstance(args[i], int):
            return mal.Error("ArgError",
                             "Wrong type argument: "
                             "expected number, got {}".format(type(args[i])))
        if not args[i] < args[i+1]:
            return False
    return True


def mal_less_or_equal(*args):
    for i in range(len(args)-1):
        if not isinstance(args[i], int):
            return mal.Error("ArgError",
                             "Wrong type argument: "
                             "expected number, got {}".format(type(args[i])))
        if not args[i] <= args[i+1]:
            return False
    return True


def mal_greater(*args):
    for i in range(len(args)-1):
        if not isinstance(args[i], int):
            return mal.Error("ArgError",
                             "Wrong type argument: "
                             "expected number, got {}".format(type(args[i])))
        if not args[i] > args[i+1]:
            return False
    return True


def mal_greater_or_equal(*args):
    for i in range(len(args)-1):
        if not isinstance(args[i], int):
            return mal.Error("ArgError",
                             "Wrong type argument: "
                             "expected number, got {}".format(type(args[i])))
        if not args[i] >= args[i+1]:
            return False
    return True


# list / vector functions


def mal_list(*args):
    return list(args)


def mal_listp(arg):
    if isinstance(arg, list):
        return True
    else:
        return False


def mal_emptyp(arg):
    if isinstance(arg, mal.Vector):
        arg = arg.value
    if not isinstance(arg, list):
        return mal.Error("ArgError",
                         "Wrong type argument: "
                         "expected list or vector, got {}".format(type(arg)))

    if arg == []:
        return True
    else:
        return False


def mal_count(arg):
    if isinstance(arg, mal.Nil):
        return 0
    if isinstance(arg, mal.Vector):
        arg = arg.value
    if not isinstance(arg, list):
        return mal.Error("ArgError",
                         "Wrong type argument: "
                         "expected list or vector, got {}".format(type(arg)))

    return len(arg)


# printing functions


def mal_pr_str(*args):
    return " ".join([printer.pr_str(arg, True) for arg in args])


def mal_str(*args):
    return "".join([printer.pr_str(arg, False) for arg in args])


def mal_prn(*args):
    print(" ".join([printer.pr_str(arg, True) for arg in args]))
    return mal.Nil()


def mal_println(*args):
    print(" ".join([printer.pr_str(arg, False) for arg in args]))
    return mal.Nil()


# core namespace
ns = {'+':      mal.Function(mal_add),
      '-':      mal.Function(mal_substract),
      '*':      mal.Function(mal_multiply),
      '/':      mal.Function(mal_divide),

      '=':      mal.Function(mal_equal),
      '<':      mal.Function(mal_less),
      '<=':     mal.Function(mal_less_or_equal),
      '>':      mal.Function(mal_greater),
      '>=':     mal.Function(mal_greater_or_equal),

      'list':   mal.Function(mal_list),
      'list?':  mal.Function(mal_listp),
      'empty?': mal.Function(mal_emptyp),
      'count':  mal.Function(mal_count),

      'pr-str': mal.Function(mal_pr_str),
      'str': mal.Function(mal_str),
      'prn': mal.Function(mal_prn),
      'println': mal.Function(mal_println)}
