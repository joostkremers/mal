import readline  # so input() uses editable input
# import sys


def READ(line):
    return line


def EVAL(line):
    return line


def PRINT(line):
    return line


def rep(line):
    return PRINT(EVAL(READ(line)))


def main():
    print("MAL in Python3")
    print()

    while True:
        try:
            line = input("user> ")
        except EOFError:
            print("Bye")
            # sys.exit(0)
            break
        result = rep(line)
        print(result)

if __name__ == '__main__':
    main()
