import mal_types as mtype
import printer
import reader


# Arithmetic functions


def mal_add(*args):
    """Sum numbers.

    If ARGS contains only one element, it is returned. If ARG is empty, the
    return value is 0.

    """
    try:
        res = sum(args)
    except TypeError:
        return mtype.Error("ArgError", "'+': Wrong type argument")

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
        return mtype.Error("ArgError", "'-': Wrong type argument")

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
        return mtype.Error("ArgError", "'*': Wrong type argument")

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
        return mtype.Error("ArithmeticError", "Division by zero")
    except TypeError:
        return mtype.Error("ArgError", "'/': Wrong type argument")

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
            return mtype.Error("ArgError",
                               "Wrong type argument: "
                               "expected number, got {}".format(type(args[i])))
        if not args[i] < args[i+1]:
            return False
    return True


def mal_less_or_equal(*args):
    for i in range(len(args)-1):
        if not isinstance(args[i], int):
            return mtype.Error("ArgError",
                               "Wrong type argument: "
                               "expected number, got {}".format(type(args[i])))
        if not args[i] <= args[i+1]:
            return False
    return True


def mal_greater(*args):
    for i in range(len(args)-1):
        if not isinstance(args[i], int):
            return mtype.Error("ArgError",
                               "Wrong type argument: "
                               "expected number, got {}".format(type(args[i])))
        if not args[i] > args[i+1]:
            return False
    return True


def mal_greater_or_equal(*args):
    for i in range(len(args)-1):
        if not isinstance(args[i], int):
            return mtype.Error("ArgError",
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
    if isinstance(arg, mtype.Vector):
        arg = arg.value
    if not isinstance(arg, list):
        return mtype.Error("ArgError",
                           "Wrong type argument: "
                           "expected list or vector, got {}".format(type(arg)))

    if arg == []:
        return True
    else:
        return False


def mal_count(arg):
    if isinstance(arg, mtype.Nil):
        return 0
    if isinstance(arg, mtype.Vector):
        arg = arg.value
    if not isinstance(arg, list):
        return mtype.Error("ArgError",
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
    return mtype.Nil()


def mal_println(*args):
    print(" ".join([printer.pr_str(arg, False) for arg in args]))
    return mtype.Nil()


# file functions


def mal_slurp(filename):
    try:
        f = open(filename, 'r')
        conts = f.read()
    except FileNotFoundError:
        return mtype.Error("FileError", "File not found")
    return conts


# core namespace
ns = {'+':           mtype.Builtin(mal_add),
      '-':           mtype.Builtin(mal_substract),
      '*':           mtype.Builtin(mal_multiply),
      '/':           mtype.Builtin(mal_divide),

      '=':           mtype.Builtin(mal_equal),
      '<':           mtype.Builtin(mal_less),
      '<=':          mtype.Builtin(mal_less_or_equal),
      '>':           mtype.Builtin(mal_greater),
      '>=':          mtype.Builtin(mal_greater_or_equal),

      'list':        mtype.Builtin(mal_list),
      'list?':       mtype.Builtin(mal_listp),
      'empty?':      mtype.Builtin(mal_emptyp),
      'count':       mtype.Builtin(mal_count),

      'pr-str':      mtype.Builtin(mal_pr_str),
      'str':         mtype.Builtin(mal_str),
      'prn':         mtype.Builtin(mal_prn),
      'println':     mtype.Builtin(mal_println),

      'read-string': mtype.Builtin(reader.read_str),
      'slurp':       mtype.Builtin(mal_slurp)}
