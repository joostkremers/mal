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
                               "'<=': Wrong type argument: "
                               "expected number, got {}".format(type(args[i])))
        if not args[i] <= args[i+1]:
            return False
    return True


def mal_greater(*args):
    for i in range(len(args)-1):
        if not isinstance(args[i], int):
            return mtype.Error("ArgError",
                               "'>': Wrong type argument: "
                               "expected number, got {}".format(type(args[i])))
        if not args[i] > args[i+1]:
            return False
    return True


def mal_greater_or_equal(*args):
    for i in range(len(args)-1):
        if not isinstance(args[i], int):
            return mtype.Error("ArgError",
                               "'>=': Wrong type argument: "
                               "expected number, got {}".format(type(args[i])))
        if not args[i] >= args[i+1]:
            return False
    return True


# list / vector functions
def mal_cons(obj, lst):
    if isinstance(lst, mtype.Vector):
        lst = lst.value
    if not isinstance(lst, list):
        return mtype.Error("ArgError", "'cons': Wrong type argument: "
                           "expected list or vector, got {}".format(type(lst)))
    return [obj] + lst


def mal_concat(*args):
    res = []
    for arg in args:
        if isinstance(arg, mtype.Vector):
            res.extend(arg.value)
        elif isinstance(arg, list):
            res.extend(arg)
        else:
            return mtype.Error("ArgError", "'concat': Wrong type argument: "
                               "expected list or vector, got {}".format(type(args[i])))

    return res


def mal_nth(arg, index):
    if not isinstance(arg, (list, mtype.Vector)):
        return mtype.Error("ArgError", "'nth': Wrong type argument:"
                           "expected list or vector, received {}".format(type(arg)))
    if index > len(arg):
        return mtype.Error("IndexError", "Index out of range")

    return arg[index]


def mal_first(arg):
    if not isinstance(arg, (list, mtype.Vector, mtype.Nil)):
        return mtype.Error("ArgError", "'nth': Wrong type argument:"
                           "expected list or vector, received {}".format(type(arg)))

    if isinstance(arg, mtype.Nil) or len(arg) == 0:
        return mtype.Nil()

    return arg[0]


def mal_rest(arg):
    if not isinstance(arg, (list, mtype.Vector, mtype.Nil)):
        return mtype.Error("ArgError", "'nth': Wrong type argument:"
                           "expected list or vector, received {}".format(type(arg)))

    if isinstance(arg, mtype.Nil) or len(arg) == 0:
        return mtype.Nil()

    return arg[1:]


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
                           "'empty?': Wrong type argument: "
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
                           "'count': Wrong type argument: "
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


def mal_descr(fn):
    if not isinstance(fn, mtype.Function):
        return mtype.Error("ArgError",
                           "'descr': Wrong type argument: "
                           "expected function, received {}".format(type(fn)))
    return fn.ast.__str__()


# file functions
def mal_slurp(filename):
    try:
        f = open(filename, 'r')
        conts = f.read()
    except FileNotFoundError:
        return mtype.Error("FileError", "File not found")
    return conts


# atom functions
def mal_atom(object):
    return mtype.Atom(object)


def mal_atomp(object):
    if isinstance(object, mtype.Atom):
        return True
    else:
        return False


def mal_deref(atom):
    if not isinstance(atom, mtype.Atom):
        return mtype.Error("TypeError",
                           "Expected atom, received {}".format(type(atom)))
    else:
        return atom.value


def mal_reset(atom, value):
    if not isinstance(atom, mtype.Atom):
        return mtype.Error("TypeError",
                           "Expected atom, received {}".format(type(atom)))
    else:
        atom.set(value)
        return value


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

      'cons':        mtype.Builtin(mal_cons),
      'concat':      mtype.Builtin(mal_concat),
      'nth':         mtype.Builtin(mal_nth),
      'first':       mtype.Builtin(mal_first),
      'rest':        mtype.Builtin(mal_rest),
      'list':        mtype.Builtin(mal_list),
      'list?':       mtype.Builtin(mal_listp),
      'empty?':      mtype.Builtin(mal_emptyp),
      'count':       mtype.Builtin(mal_count),

      'pr-str':      mtype.Builtin(mal_pr_str),
      'str':         mtype.Builtin(mal_str),
      'prn':         mtype.Builtin(mal_prn),
      'println':     mtype.Builtin(mal_println),

      'descr':       mtype.Builtin(mal_descr),

      'read-string': mtype.Builtin(reader.read_str),
      'slurp':       mtype.Builtin(mal_slurp),

      'atom':        mtype.Builtin(mal_atom),
      'atom?':       mtype.Builtin(mal_atomp),
      'deref':       mtype.Builtin(mal_deref),
      'reset!':      mtype.Builtin(mal_reset)}
