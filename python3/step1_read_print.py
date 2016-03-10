import readline  # so input() uses editable input
import reader
import printer


def READ(line):
    return reader.read_str(line)


def EVAL(form):
    return form


def PRINT(line):
    return printer.pr_str(line)


def rep(line):
    return PRINT(EVAL(READ(line)))


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
