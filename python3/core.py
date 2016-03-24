import copy
import time
import numbers

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
        if not isinstance(args[i], numbers.Number):
            return mtype.Error("ArgError",
                               "Wrong type argument: "
                               "expected number, got {}".format(type(args[i])))
        if not args[i] < args[i+1]:
            return False
    return True


def mal_less_or_equal(*args):
    for i in range(len(args)-1):
        if not isinstance(args[i], numbers.Number):
            return mtype.Error("ArgError",
                               "'<=': Wrong type argument: "
                               "expected number, got {}".format(type(args[i])))
        if not args[i] <= args[i+1]:
            return False
    return True


def mal_greater(*args):
    for i in range(len(args)-1):
        if not isinstance(args[i], numbers.Number):
            return mtype.Error("ArgError",
                               "'>': Wrong type argument: "
                               "expected number, got {}".format(type(args[i])))
        if not args[i] > args[i+1]:
            return False
    return True


def mal_greater_or_equal(*args):
    for i in range(len(args)-1):
        if not isinstance(args[i], numbers.Number):
            return mtype.Error("ArgError",
                               "'>=': Wrong type argument: "
                               "expected number, got {}".format(type(args[i])))
        if not args[i] >= args[i+1]:
            return False
    return True


# list / vector functions
def mal_cons(obj, lst):
    if type(lst) is mtype.Vector:
        lst = lst.value
    if type(lst) is not list:
        return mtype.Error("ArgError", "'cons': Wrong type argument: "
                           "expected list or vector, got {}".format(type(lst)))
    return [obj] + lst


def mal_concat(*args):
    res = []
    for arg in args:
        if type(arg) is mtype.Vector:
            res.extend(arg.value)
        elif type(arg) is list:
            res.extend(arg)
        else:
            return mtype.Error("ArgError", "'concat': Wrong type argument: "
                               "expected list or vector, got {}".
                               format(type(arg)))

    return res


def mal_conj(seq, *elems):
    """Add ELEMS to SEQ (a list or vector).

    If SEQ is a list, the elements in ELEMS are added to the front of the list
    in reverse order. If SEQ is a vector, the elements are added to the end.

    """
    if not isinstance(seq, (list, mtype.Vector)):
        return mtype.Error("ArgError", "'conj': Wrong type argument:"
                           "expected list or vector, received {}".
                           format(type(seq)))

    if type(seq) is list:
        return list(elems)[::-1] + seq

    if type(seq) is mtype.Vector:
        return mtype.Vector(seq.value + list(elems))


def mal_nth(arg, index):
    if not isinstance(arg, (list, mtype.Vector)):
        return mtype.Error("ArgError", "'nth': Wrong type argument:"
                           "expected list or vector, received {}".
                           format(type(arg)))
    if index >= len(arg):
        return mtype.Error("IndexError", "Index out of range")

    return arg[index]


def mal_first(arg):
    if not isinstance(arg, (list, mtype.Vector, mtype.Nil)):
        return mtype.Error("ArgError", "'nth': Wrong type argument:"
                           "expected list or vector, received {}".
                           format(type(arg)))

    if type(arg) is mtype.Nil or len(arg) == 0:
        return mtype.Nil()

    return arg[0]


def mal_rest(arg):
    if not isinstance(arg, (list, mtype.Vector, mtype.Nil)):
        return mtype.Error("ArgError", "'nth': Wrong type argument:"
                           "expected list or vector, received {}".
                           format(type(arg)))

    if type(arg) is mtype.Nil:
        return []

    return arg[1:]


def mal_list(*args):
    return list(args)


def mal_listp(arg):
    if type(arg) is list:
        return True
    else:
        return False


def mal_emptyp(arg):
    if type(arg) is mtype.Vector:
        arg = arg.value
    if type(arg) is not list:
        return mtype.Error("ArgError",
                           "'empty?': Wrong type argument: "
                           "expected list or vector, got {}".format(type(arg)))

    if arg == []:
        return True
    else:
        return False


def mal_count(arg):
    if type(arg) is mtype.Nil:
        return 0
    if type(arg) is mtype.Vector:
        arg = arg.value
    if type(arg) is not list:
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


# file functions
def mal_slurp(filename):
    try:
        f = open(filename, 'r')
        conts = f.read()
    except FileNotFoundError:
        return mtype.Error("FileError", "File not found")
    return conts


# readline
def mal_readline(prompt):
    try:
        line = input(prompt)
    except EOFError:
        return mtype.Nil()
    return line


# atom functions
def mal_atom(object):
    return mtype.Atom(object)


def mal_atomp(object):
    if type(object) is mtype.Atom:
        return True
    else:
        return False


def mal_deref(atom):
    if type(atom) is not mtype.Atom:
        return mtype.Error("TypeError",
                           "Expected atom, received {}".format(type(atom)))
    else:
        return atom.value


def mal_reset(atom, value):
    if type(atom) is not mtype.Atom:
        return mtype.Error("TypeError",
                           "Expected atom, received {}".format(type(atom)))
    else:
        atom.set(value)
        return value


# throw
def mal_throw(arg):
    return mtype.Error("UserError", arg)


# functional functions
def mal_apply(fn, *args):
    if not isinstance(fn, (mtype.Builtin, mtype.Function)):
        return mtype.Error("TypeError", "Expected function,"
                           " received {}".format(type(args[-1])))

    lastarg = args[-1]
    if type(lastarg) is mtype.Vector:
        lastarg = lastarg.value

    if not isinstance(lastarg, list):
        return mtype.Error("TypeError", "Expected list or vector,"
                           " received {}".format(type(args[-1])))

    allargs = list(args[:-1]) + lastarg

    return fn.fn(*allargs)


def mal_map(fn, lst):
    if not isinstance(fn, (mtype.Builtin, mtype.Function)):
        return mtype.Error("TypeError", "Expected function,"
                           " received {}".format(type(fn)))

    if type(lst) is mtype.Vector:
        lst = lst.value
    if type(lst) is not list:
        return mtype.Error("TypeError", "Expected list or vector,"
                           " received {}".format(type(lst)))

    res = []
    for elem in lst:
        evalled = fn.fn(elem)
        if type(evalled) is mtype.Error:
            return evalled
        res.append(evalled)

    return res


# type functions
def mal_symbol(arg):
    if type(arg) is not str:
        return mtype.Error("TypeError",
                           "Wrong type argument: "
                           "expected string, received {}".format(type(arg)))
    return mtype.Symbol(arg)


def mal_keyword(arg):
    if type(arg) is mtype.Keyword:
        return arg
    if type(arg) is not str:
        return mtype.Error("TypeError",
                           "Wrong type argument: "
                           "expected string, received {}".format(type(arg)))
    return mtype.Keyword(arg)


def mal_vector(*args):
    return mtype.Vector(list(args))


def mal_seq(arg):
    """Turn ARG into a list.

    If ARG is nil or an empty list, vector or string, return nil. If ARG is a
    non-empty list, return it unchanged; if ARG is a non-empty vector, convert
    it to a list; if ARG is a non-empty string, return a list of characters.

    """
    if type(arg) is mtype.Nil:
        return mtype.Nil()

    if len(arg) == 0:
        return mtype.Nil()

    if type(arg) is list:
        return arg

    if type(arg) is mtype.Vector:
        return arg.value

    if type(arg) is str:
        return list(arg)

    # if all fails, return an error
    return mtype.Error("ArgError", "'seq': Wrong type argument: "
                       "expected sequence, received {}".format(type(arg)))


# type predicates
def mal_nilp(arg):
    return (type(arg) is mtype.Nil)


def mal_truep(arg):
    return (arg is True)


def mal_falsep(arg):
    return (arg is False)


def mal_symbolp(arg):
    return (type(arg) is mtype.Symbol)


def mal_keywordp(arg):
    return (type(arg) is mtype.Keyword)


def mal_vectorp(arg):
    return (type(arg) is mtype.Vector)


def mal_mapp(arg):
    return (type(arg) is dict)


def mal_sequentialp(arg):
    return isinstance(arg, (list, mtype.Vector))


def mal_stringp(arg):
    return (type(arg) is str)


# hash functions
def mal_hashmap(*args):
    return reader.create_hash(args)


def mal_assoc(hashmap, *args):
    if type(hashmap) is not dict:
        return mtype.Error("TypeError",
                           "Wrong type argument:"
                           " expected hash, received {}".format(type(hashmap)))
    orig = hashmap.copy()

    new = reader.create_hash(list(args))
    if type(new) is mtype.Error:
        return new

    orig.update(new)
    return orig


def mal_dissoc(hashmap, *keys):
    if type(hashmap) is not dict:
        return mtype.Error("TypeError",
                           "Wrong type argument:"
                           " expected hash, received {}".format(type(hashmap)))

    new = hashmap.copy()
    for key in keys:
        new.pop(key, None)

    return new


def mal_get(hashmap, key):
    if hashmap == mtype.Nil():
        hashmap = {}
    if type(hashmap) is not dict:
        return mtype.Error("TypeError",
                           "Wrong type argument:"
                           " expected hash, received {}".format(type(hashmap)))
    if key in hashmap:
        return hashmap[key]
    else:
        return mtype.Nil()


def mal_containsp(hashmap, key):
    if type(hashmap) is not dict:
        return mtype.Error("TypeError",
                           "Wrong type argument:"
                           " expected hash, received {}".format(type(hashmap)))
    return (key in hashmap)


def mal_keys(hashmap):
    if type(hashmap) is not dict:
        return mtype.Error("TypeError",
                           "Wrong type argument:"
                           " expected hash, received {}".format(type(hashmap)))
    return list(hashmap.keys())


def mal_vals(hashmap):
    if type(hashmap) is not dict:
        return mtype.Error("TypeError",
                           "Wrong type argument:"
                           " expected hash, received {}".format(type(hashmap)))
    return list(hashmap.values())


# metadata
def mal_meta(obj):
    try:
        data = obj.meta
    except AttributeError:
        return mtype.Nil()
    return data


def mal_with_meta(obj, data):
    new_obj = copy.copy(obj)
    try:
        new_obj.meta = data
    except AttributeError:
        return obj
    return new_obj


# time
def mal_time_ms():
    """Return the current time as miliseconds since the epoch.

    Note that depending on the system, this function may only provide an
    accuracy of 1 second.

    """
    return time.time() * 1000


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
      'conj':        mtype.Builtin(mal_conj),
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

      'read-string': mtype.Builtin(reader.read_str),
      'slurp':       mtype.Builtin(mal_slurp),

      'readline':    mtype.Builtin(mal_readline),

      'atom':        mtype.Builtin(mal_atom),
      'atom?':       mtype.Builtin(mal_atomp),
      'deref':       mtype.Builtin(mal_deref),
      'reset!':      mtype.Builtin(mal_reset),

      'throw':       mtype.Builtin(mal_throw),

      'apply':       mtype.Builtin(mal_apply),
      'map':         mtype.Builtin(mal_map),

      'symbol':      mtype.Builtin(mal_symbol),
      'keyword':     mtype.Builtin(mal_keyword),
      'vector':      mtype.Builtin(mal_vector),
      'seq':         mtype.Builtin(mal_seq),

      'nil?':        mtype.Builtin(mal_nilp),
      'true?':       mtype.Builtin(mal_truep),
      'false?':      mtype.Builtin(mal_falsep),
      'symbol?':     mtype.Builtin(mal_symbolp),
      'keyword?':    mtype.Builtin(mal_keywordp),
      'vector?':     mtype.Builtin(mal_vectorp),
      'map?':        mtype.Builtin(mal_mapp),
      'sequential?': mtype.Builtin(mal_sequentialp),
      'string?':     mtype.Builtin(mal_stringp),

      'hash-map':    mtype.Builtin(mal_hashmap),
      'assoc':       mtype.Builtin(mal_assoc),
      'dissoc':      mtype.Builtin(mal_dissoc),
      'get':         mtype.Builtin(mal_get),
      'contains?':   mtype.Builtin(mal_containsp),
      'keys':        mtype.Builtin(mal_keys),
      'vals':        mtype.Builtin(mal_vals),

      'meta':        mtype.Builtin(mal_meta),
      'with-meta':   mtype.Builtin(mal_with_meta),

      'time-ms':     mtype.Builtin(mal_time_ms)}
