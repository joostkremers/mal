import readline  # so input() uses editable input
import reader
import printer
import mal_types as mal
import mal_env as env
import core


def READ(line):
    return reader.read_str(line)


def EVAL(ast, env):
    # import pdb; pdb.set_trace()

    if ast.type == "list":
        if ast.value[0].type == "symbol":
            symbol = ast.value[0].name
            # Note: def! and let* can only take a single form.
            if symbol == "def!":
                return mal_def(env, ast.value[1], ast.value[2])
            elif symbol == "let*":
                return mal_let(env, ast.value[1], ast.value[2])
            elif symbol == "do":
                return mal_do(env, ast.value[1:])
            elif symbol == "if":
                return mal_if(env, ast.value[1:])
            elif symbol == "fn*":
                return mal_fn(env, ast.value[1], ast.value[2])

        # Either the list does not start with a symbol, or the symbol is not a
        # special form
        evalled = eval_ast(ast, env)
        if evalled.type == "error":
            return evalled
        else:
            return evalled.value[0].value(*evalled.value[1:])
    else:  # not a list
        return eval_ast(ast, env)


# Special forms


def mal_def(environment, symbol, value):
    evalled = EVAL(value, environment)
    environment.set(symbol.name, evalled)
    return evalled


def mal_let(environment, bindings, body):
    # import pdb; pdb.set_trace()

    if bindings.type not in ["list", "vector"]:
        return mal.Error("LetError", "Invalid bind form")
    if (len(bindings.value) % 2 != 0):
        return mal.Error("LetError", "Insufficient bind forms")

    new_env = env.MalEnv(outer=environment)
    # Note: bindings may be a mal.List or a mal.Vector.
    for i in range(0, len(bindings.value), 2):
        if bindings.value[i].type != "symbol":
            return mal.Error("LetError", "Attempt to bind to non-symbol")

        evalled = EVAL(bindings.value[i+1], new_env)
        if evalled.type == "error":
            return evalled

        new_env.set(bindings.value[i].name, evalled)

    return EVAL(body, new_env)


def mal_do(environment, forms):
    evalled = eval_ast(mal.List(forms), environment)
    if evalled.type == "error":
        return evalled
    else:
        return evalled.value[-1]

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
    if condition != mal.Boolean(False) and condition != mal.Nil():
        return EVAL(args[1], environment)
    else:
        if len(args) == 3:
            return EVAL(args[2], environment)
        else:
            return mal.Nil()


def mal_fn(environment, syms, body):
    def mal_closure(*params):
        new_env = env.MalEnv(outer=environment, binds=syms.value, exprs=params)
        return EVAL(body, new_env)

    return mal.Function(mal_closure)


def PRINT(data):
    return printer.pr_str(data)


def eval_ast(ast, env):
    if ast.type == "symbol":
        return env.get(ast.name)

    elif ast.type in ["list", "vector"]:
        res = []
        for elem in ast.value:
            val = EVAL(elem, env)
            if val.type == "error":
                return val
            res.append(val)
        if ast.type == "list":
            return mal.List(res)
        else:
            return mal.Vector(res)

    elif ast.type == "hash":
        res = {}
        for key, val in ast.value.items():
            newval = EVAL(val, env)
            if newval.type == "error":
                return newval
            res[key] = newval
        return mal.Hash(res)

    else:
        return ast


def rep(line, env):
    ast = READ(line)
    result = EVAL(ast, env)
    return PRINT(result)


def runmal():
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
    runmal()
