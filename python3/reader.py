import re
import mal_types


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


def read_str(input_str):
    input_list = tokenize(input_str)
    return read_form(Reader(input_list))


def tokenize(input_str):
    token_regexp = (r'[\s,]*'
                    r'(~@|'
                    r'[\[\]{}()\'`~^@]|'
                    r'"(?:\\.|[^\\"])*"'
                    r'|;.*|'
                    r'[^\s\[\]{}(\'"`,;)]*)')

    tokens = re.findall(token_regexp, input_str)
    # not sure how to remove the final empty element from the list.
    return [token for token in tokens if token != '']


def read_form(form):
    token = form.peek()
    if token[0] == '(':
        return read_list(form)
    else:
        return read_atom(form)


def read_list(form):
    """Read a list from FORM."""
    res = []
    # current token is still '(', so we advance first
    form.next()

    while True:
        # We only peek the next token here. Advancing is done in read_atom
        token = form.peek()
        if token == ')':  # we've found the end of the list
            break
        if token == '':  # we've reached the end of FORM
            return mal_types.MalError("ParenError",
                                      "Missing closing parenthesis")
        res.append(read_form(form))

    return mal_types.MalList(res)


def read_atom(form):
    token = form.next()
    # numbers (integers for now)
    if re.match(r'\A[0-9]+\Z', token):
        return mal_types.MalInt(int(token))

    # strings
    if re.match(r'\A"(.*)"\Z', token):
        return mal_types.MalString(token[1:-1])

    # symbols
    if re.match(r"[^\s\[\]{}('\"`,;)]*", token):
        return mal_types.MalSymbol(token)

    # found nothing parsable
    return mal_types.MalError("ParseError",
                              "Could not parse token: »{}«".format(token))
