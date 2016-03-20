# System imports
import readline  # so input() uses editable input
import sys

# Local imports
import reader
import printer
import mal_types as mtype
import mal_env as menv
import core

repl_env = None


def READ(line):
    return reader.read_str(line)


def EVAL(ast, env):
    while True:
        if isinstance(ast, mtype.Error):
            return ast
        elif not isinstance(ast, list):
            return eval_ast(ast, env)
        else:
            # import pdb; pdb.set_trace()
            if len(ast) == 0:
                return ast
            if isinstance(ast[0], mtype.Symbol):
                symbol = ast[0].name
                # Special forms
                if symbol == "def!":
                    return mal_def(env, ast[1], ast[2])
                elif symbol == "let*":
                    ast, env = mal_let(env, ast[1], ast[2])
                    continue
                elif symbol == "do":
                    evalled = eval_ast(ast[1:-1], env)
                    if isinstance(evalled, mtype.Error):
                        return evalled
                    ast = ast[-1]
                    continue
                elif symbol == "if":
                    ast = mal_if(env, ast[1:])
                    continue
                elif symbol == "fn*":
                    return mal_fn(env, ast[1], ast[2])
                elif symbol == "quote":
                    return ast[1]
                elif symbol == "quasiquote":
                    ast = mal_quasiquote(ast[1])
                    continue

        # If the list does not start with a symbol or if the symbol is not a
        # special form, we evaluate and apply:
        evalled = eval_ast(ast, env)
        if isinstance(evalled, mtype.Error):
            return evalled
        elif isinstance(evalled[0], mtype.Builtin):
            return evalled[0].fn(*evalled[1:])
        elif isinstance(evalled[0], mtype.Function):
            ast = evalled[0].ast
            env = menv.MalEnv(outer=evalled[0].env,
                              binds=evalled[0].params,
                              exprs=evalled[1:])
            continue
        else:
            return mtype.Error("ApplyError",
                               "'{}' is not callable".format(evalled[0]))


# Special forms


def mal_def(environment, symbol, value):
    evalled = EVAL(value, environment)
    environment.set(symbol.name, evalled)
    return evalled


def mal_let(environment, bindings, body):
    if not isinstance(bindings, (list, mtype.Vector)):
        return (mtype.Error("LetError", "Invalid bind form"), None)
    if (len(bindings.value) % 2 != 0):
        return (mtype.Error("LetError", "Insufficient bind forms"), None)

    new_env = menv.MalEnv(outer=environment)
    # Note: bindings may be a list or an mtype.Vector.
    if isinstance(bindings, mtype.Vector):
        bindings = bindings.value
    for i in range(0, len(bindings), 2):
        if not isinstance(bindings[i], mtype.Symbol):
            return (mtype.Error("LetError", "Attempt to bind to non-symbol"),
                    None)

        evalled = EVAL(bindings[i+1], new_env)
        if isinstance(evalled, mtype.Error):
            return (evalled, None)

        new_env.set(bindings[i].name, evalled)

    return (body, new_env)


def mal_if(environment, args):
    if len(args) < 2:
        return mtype.Error("ArgError",
                           "'if' requires 2-3 arguments, "
                           "received {}".format(len(args)))

    condition = EVAL(args[0], environment)
    if (condition is not False) and (not isinstance(condition, mtype.Nil)):
        return args[1]
    else:
        if len(args) == 3:
            return args[2]
        else:
            return mtype.Nil()


def mal_fn(environment, syms, body):
    if isinstance(syms, mtype.Vector):
        syms = syms.value

    if '&' in syms:
        if syms.index('&') != len(syms) - 2:
            return mtype.Error("BindsError", "Illegal binds list")

    def mal_closure(*params):
        new_env = menv.MalEnv(outer=environment, binds=syms, exprs=params)
        return EVAL(body, new_env)

    return mtype.Function(mal_closure, syms, body, environment)


def is_pair(arg):
    """Return True if ARG is a non-empty list or vector."""

    if isinstance(arg, (list, mtype.Vector)) and len(arg) > 0:
        return True
    else:
        return False


def mal_quasiquote(ast):
    # not a list (or empty list)
    if not is_pair(ast):
        return list((mtype.Symbol("quote"), ast))

    # unquote
    elif isinstance(ast[0], mtype.Symbol) and ast[0].name == "unquote":
        return ast[1]

    # splice-unquote
    elif (is_pair(ast[0]) and
          isinstance(ast[0][0], mtype.Symbol) and
          ast[0][0].name == "splice-unquote"):
        first = mtype. Symbol("concat")
        second = ast[0][1]
        rest = mal_quasiquote(ast[1:])
        return list((first, second, rest))

    # otherwise
    else:
        first = mtype.Symbol("cons")
        second = mal_quasiquote(ast[0])
        rest = mal_quasiquote(ast[1:])
        return list((first, second, rest))


def PRINT(data):
    return printer.pr_str(data, print_readably=True)


def eval_ast(ast, env):
    if isinstance(ast, mtype.Symbol):
        # print(ast.__repr__())
        return env.get(ast.name)

    elif isinstance(ast, list):
        return eval_list(ast, env)

    elif isinstance(ast, mtype.Vector):
        return mtype.Vector(eval_list(ast.value, env))

    elif isinstance(ast, dict):
        res = {}
        for key, val in ast.items():
            newval = EVAL(val, env)
            if isinstance(newval, mtype.Error):
                return newval
            res[key] = newval
        return res

    else:
        return ast


def eval_list(ast, env):
    res = []
    for elem in ast:
        val = EVAL(elem, env)
        if isinstance(val, mtype.Error):
            return val
        res.append(val)
    return res


# These builtins are defined here and not in core.py because they call EVAL:
def mal_eval(ast):
    global repl_env
    return EVAL(ast, repl_env)


def mal_swap(atom, fn, *args):
    global repl_env

    if not isinstance(atom, mtype.Atom):
        return mtype.Error("TypeError",
                           "Expected atom, received {}".format(type(atom)))

    call_list = [fn, atom.value] + list(args)
    evalled = EVAL(call_list, repl_env)
    atom.set(evalled)
    return evalled


def rep(line, env):
    ast = READ(line)
    result = EVAL(ast, env)
    return PRINT(result)


def Mal(args=[]):
    print("MAL in Python3 7.0")
    print("Based on Make-a-Lisp")
    print("Copyright (c) 2016 Joost Kremers")
    print()

    global repl_env
    repl_env = menv.MalEnv()

    for sym in core.ns:
        repl_env.set(sym, core.ns[sym])

    # Add eval and swap! to repl_env:
    repl_env.set("eval", mtype.Builtin(mal_eval))
    repl_env.set("swap!", mtype.Builtin(mal_swap))

    # Add the command line arguments to repl_env:
    repl_env.set("*ARGV*", list(args[1:]))

    # Add a language-defined 'not' function:
    rep("(def! not (fn* (a) (if a false true)))", repl_env)

    # Add a 'load-file' function:
    rep("(def! load-file (fn* (f)"
        "(eval (read-string (str \"(do \" (slurp f) \")\")))))", repl_env)

    if len(args) >= 1:
        rep("(load-file {})".format(args[0]), repl_env)
        sys.exit(0)

    while True:
        try:
            line = input("user> ")
        except EOFError:
            print("\n\nBye")
            break
        if line == "quit":
            print("\n\nBye")
            break
        result = rep(line, repl_env)
        print(result)

if __name__ == '__main__':
    Mal(sys.argv[1:])
