import readline  # so input() uses editable input
import reader
import printer
import mal_types
import mal_env


def READ(line):
    return reader.read_str(line)


def EVAL(ast, env):
    # import pdb; pdb.set_trace()

    evalled = eval_ast(ast, env)

    if evalled.type == "list":
        # apply function
        evalled = evalled.value[0].value(*evalled.value[1:])

    return evalled


def PRINT(data):
    return printer.pr_str(data)


def eval_ast(ast, env):
    if ast.type == "symbol":
        if ast.name in env:
            return env[ast.name]
        else:
            return mal_types.MalError("SymbolError",
                                      "Symbol has no value: '{}'".
                                      format(ast.name))

    elif ast.type in ["list", "vector"]:
        res = []
        for elem in ast.value:
            val = EVAL(elem, env)
            if val.type == "error":
                return val
            res.append(val)
        if ast.type == "list":
            return mal_types.MalList(res)
        else:
            return mal_types.MalVector(res)

    elif ast.type == "hash":
        res = {}
        for key, val in ast.value.items():
            newval = EVAL(val, env)
            if newval.type == "error":
                return newval
            res[key] = newval
        return mal_types.MalHash(res)

    else:
        return ast


def rep(line):
    ast = READ(line)
    result = EVAL(ast, mal_env.repl_env)
    return PRINT(result)


def mal():
    print("MAL in Python3")
    print()

    while True:
        try:
            line = input("user> ")
        except EOFError:
            print("\n\nBye")
            break
        result = rep(line)
        print(result)

if __name__ == '__main__':
    mal()
