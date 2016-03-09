import readline  # so input() uses editable input
import reader
import printer


def READ(line):
    return reader.read_str(line)


def EVAL(line):
    return line


def PRINT(line):
    return printer.pr_str(line)


def rep(line):
    return PRINT(EVAL(READ(line)))


def main():
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
    main()
