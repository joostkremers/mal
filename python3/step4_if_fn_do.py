import readline  # so input() uses editable input
import reader
import printer
import mal_types as mal
import mal_env as env
import core


def READ(line):
    return reader.read_str(line)


def EVAL(ast, env):
    if isinstance(ast, list) and len(ast) > 0:
        if isinstance(ast[0], mal.Symbol):
            symbol = ast[0].name
            # Note: def! and let* can only take a single form.
            if symbol == "def!":
                return mal_def(env, ast[1], ast[2])
            elif symbol == "let*":
                return mal_let(env, ast[1], ast[2])
            elif symbol == "do":
                return mal_do(env, ast[1:])
            elif symbol == "if":
                return mal_if(env, ast[1:])
            elif symbol == "fn*":
                return mal_fn(env, ast[1], ast[2])

        # Either the list does not start with a symbol, or the symbol is not a
        # special form
        evalled = eval_ast(ast, env)
        if isinstance(evalled, mal.Error):
            return evalled
        elif not isinstance(evalled[0], mal.Function):
            return mal.Error("ApplyError",
                             "'{}' is not a function object".
                             format(evalled[0]))
        else:
            return evalled[0].value(*evalled[1:])
    else:  # not a list
        return eval_ast(ast, env)


# Special forms


def mal_def(environment, symbol, value):
    evalled = EVAL(value, environment)
    environment.set(symbol.name, evalled)
    return evalled


def mal_let(environment, bindings, body):
    if bindings.type not in ["list", "vector"]:
        return mal.Error("LetError", "Invalid bind form")
    if (len(bindings.value) % 2 != 0):
        return mal.Error("LetError", "Insufficient bind forms")

    new_env = env.MalEnv(outer=environment)
    # Note: bindings may be a list or a mal.Vector.
    if isinstance(bindings, mal.Vector):
        bindings = bindings.value
    for i in range(0, len(bindings), 2):
        if not isinstance(bindings[i], mal.Symbol):
            return mal.Error("LetError", "Attempt to bind to non-symbol")

        evalled = EVAL(bindings[i+1], new_env)
        if isinstance(evalled, mal.Error):
            return evalled

        new_env.set(bindings[i].name, evalled)

    return EVAL(body, new_env)


def mal_do(environment, forms):
    evalled = eval_ast(forms, environment)
    if isinstance(evalled, mal.Error):
        return evalled
    else:
        return evalled[-1]

# The alternative (original) implementation of `mal_do', which runs through the
# list itself, may be bad because of the environment: I use a dictionary to
# implement it, which is passed by reference, so that if an argument of `do`
# modifies it, the modifications are visible by later arguments. Depending on
# the language and the implenetation of the environment, this may not always be
# the case, however.


# def mal_do(environment, forms):
#     for form in forms:
#         evalled = EVAL(form, environment)
#         if evalled.type == "error":
#             break
#     return evalled


def mal_if(environment, args):
    if len(args) < 2:
        return mal.Error("ArgError",
                         "'if' expects 2-3 arguments, "
                         "received {}".format(len(args)))

    condition = EVAL(args[0], environment)
    if (condition is not False) and (not isinstance(condition, mal.Nil)):
        return EVAL(args[1], environment)
    else:
        if len(args) == 3:
            return EVAL(args[2], environment)
        else:
            return mal.Nil()


def mal_fn(environment, syms, body):
    if isinstance(syms, mal.Vector):
        syms = syms.value

    if '&' in syms:
        if syms.index('&') != len(syms) - 2:
            return mal.Error("BindsError", "Illegal binds list")

    def mal_closure(*params):
        new_env = env.MalEnv(outer=environment, binds=syms, exprs=params)
        return EVAL(body, new_env)

    return mal.Function(mal_closure)


def PRINT(data):
    return printer.pr_str(data, print_readably=True)


def eval_ast(ast, env):
    if isinstance(ast, mal.Symbol):
        return env.get(ast.name)

    elif isinstance(ast, list):
        return eval_list(ast, env)

    elif isinstance(ast, mal.Vector):
        return mal.Vector(eval_list(ast.value, env))

    elif isinstance(ast, dict):
        res = {}
        for key, val in ast.items():
            newval = EVAL(val, env)
            if isinstance(newval, mal.Error):
                return newval
            res[key] = newval
        return res

    else:
        return ast


def eval_list(ast, env):
    res = []
    for elem in ast:
        val = EVAL(elem, env)
        if isinstance(val, mal.Error):
            return val
        res.append(val)
    return res


def rep(line, env):
    ast = READ(line)
    result = EVAL(ast, env)
    return PRINT(result)


def Mal():
    print("MAL in Python3")
    print()

    repl_env = env.MalEnv()

    for sym in core.ns:
        repl_env.set(sym, core.ns[sym])

    # Add a language-defined 'not' function:
    rep("(def! not (fn* (a) (if a false true)))", repl_env)

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
    Mal()
