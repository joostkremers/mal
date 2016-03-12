import readline  # so input() uses editable input
import reader
import printer
import mal_types as mal
import mal_env as env


# Built-ins


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


# REPL


def READ(line):
    return reader.read_str(line)


def EVAL(ast, env):
    # import pdb; pdb.set_trace()

    if ast.type == "list":
        if ast.value[0].type == "symbol":
            symbol = ast.value[0].name
        else:
            return mal.Error("EvalError",
                             "First element of list is not a symbol")

        # Note: def! and let* can only take a single form.
        if symbol == "def!":
            return mal_def(env, ast.value[1], ast.value[2])
        elif symbol == "let*":
            return mal_let(env, ast.value[1], ast.value[2])
        else:  # a normal function
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
    if bindings.type not in ["list", "vector"]:
        return mal.Error("LetError", "Invalid bind form")
    if (len(bindings.value) % 2 != 0):
        return mal.Error("LetError", "Insufficient bind forms")

    new_env = env.Env(outer=environment)
    # Note: bindings may be a mal.List or a mal.Vector.
    for i in range(0, len(bindings.value), 2):
        if bindings.value[i].type != "symbol":
            return mal.Error("LetError", "Attempt to bind to non-symbol")

        evalled = EVAL(bindings.value[i+1], new_env)
        if evalled.type == "error":
            return evalled

        new_env.set(bindings.value[i].name, evalled)

    return EVAL(body, new_env)


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

    e = {}
    e[('+')] = mal.Function(mal_add)
    e[('-')] = mal.Function(mal_substract)
    e[('*')] = mal.Function(mal_multiply)
    e[('/')] = mal.Function(mal_divide)

    repl_env = env.Env(outer=None, data=e)

    while True:
        try:
            line = input("user> ")
        except EOFError:
            print("\n\nBye")
            break
        result = rep(line, repl_env)
        print(result)

if __name__ == '__main__':
    runmal()
