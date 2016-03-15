# coding=utf-8
import re
import mal_types as mtype


class Reader:
    """A Reader object for storing a list of tokens and an index into that list.

    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def next(self):
        """Return the current token and increment the index.

        If the list of tokens has been exausted, return the empty string.

        """
        token = self.peek()
        self.position += 1
        return token

    def peek(self):
        """Return the current token.

        If the list of tokens has been exhausted, return the empty string.
        """
        if self.position >= len(self.tokens):
            return ''
        else:
            return self.tokens[self.position]


reader_macros = {"'": "quote",
                 "`": "quasiquote",
                 "~": "unquote",
                 "~@": "splice-unquote"}


def read_str(input_str):
    """Convert INPUT_STR into a Mal object."""
    tokens = tokenize(input_str)
    mal_object = read_form(Reader(tokens))
    return mal_object


def tokenize(input_str):
    """Tokenize INPUT_STR.

    Return a list of tokens."""
    token_regexp = (r'[\s,]*'
                    r'(~@|'
                    r'[\[\]{}()\'`~^@]|'
                    r'"(?:\\.|[^\\"])*"'
                    r'|;.*|'
                    r'[^\s\[\]{}(\'"`,;)]*)')

    tokens = re.findall(token_regexp, input_str)

    # The re.findall() call adds an empty match to the end of the list. I'm not
    # sure how to remove this other than by checking for it explictly. We also
    # filter out comments at this point.
    return [token for token in tokens if token != '' and token[0] != ';']


def read_form(form):
    token = form.next()
    if token in ['(', '[', '{']:
        return read_sequence(form, token)
    elif token in reader_macros:
        return apply_reader_macro(form, token)
    elif token == '':
        return mtype.MalType("comment")
    else:
        return read_atom(token)


def read_sequence(form, token):
    """Read a sequence from FORM.

    This function reads list, vectors and hash tables.
    """
    res = []

    end_token = {'(': ')', '[': ']', '{': '}'}[token]

    while True:
        token = form.peek()
        if token == end_token:  # We've found the end of the list.
            break
        if token == '':  # We've reached the end of FORM.
            return mtype.Error("ParenError", "Missing closing parenthesis")
        next_form = read_form(form)
        if isinstance(next_form, mtype.Error):
            return next_form

        res.append(next_form)

    # Now we need to move past the end token
    form.next()

    if end_token == ')':
        return res
    elif end_token == '}':
        return create_hash(res)
    else:
        return mtype.Vector(res)


def create_hash(items):
    """Create a hash table from ITEMS."""

    # Hash tables in Mal can have strings or keywords as keys. MalString and
    # MalKeyword are hashable, so there's no need to use a rare Unicode
    # character as prefix in order to distinguish them, as suggested in the
    # mal_guide.

    if (len(items) % 2) != 0:
        return mtype.Error("HashError", "Insufficient number of items")

    res = {}
    for i in range(0, len(items), 2):
        key = items[i]
        value = items[i+1]
        res[key] = value
    return res


def apply_reader_macro(form, token):
    next_form = read_form(form)
    if isinstance(next_form, mtype.Error):
        return next_form
    replacement = mtype.Symbol(reader_macros[token])
    return [replacement, next_form]


def read_atom(token):
    # integers
    if re.match(r'\A-?[0-9]+\Z', token):
        return int(token)

    # strings
    if re.match(r'\A"(.*)"\Z', token):
        string = token[1:-1]
        string = string.replace(r'\"', '"')
        string = string.replace(r'\n', '\n')
        string = string.replace(r'\\', '\\')
        return string

    # keywords
    if re.match(r'\A:.*\Z', token):
        return mtype.Keyword(token)

    # boolean
    if token == "true":
        return True
    if token == "false":
        return False

    # nil
    if token == "nil":
        return mtype.Nil()

    # symbols
    if re.match(r"[^\s\[\]{}('\"`,;)]*", token):
        return mtype.Symbol(token)

    # Found nothing parsable. (Shouldn't really happen, since symbols are a
    # catch-all already.)
    return mtype.Error("ParseError", "Could not parse token: '{}'".
                       format(token))


def main():
    form = '(def (fn a (b c)) (print (+ a b)))'
    print(read_str(form))


if __name__ == '__main__':
    main()
