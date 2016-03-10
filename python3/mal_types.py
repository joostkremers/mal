class MalType:
    """Parent type of all Mal types."""

    # We can use MalType when we need to have an object that has no effect
    # whatsoever. VALUE in this case can indicate why this object exists. We do
    # this with comments, for example.
    def __init__(self, object):
        self.value = object
        self.type = None

    def __str__(self):
        return ""


class MalList(MalType):
    """Mal list type."""

    def __init__(self, value=[]):
        self.value = value
        self.type = "list"

    def __str__(self):
        str_list = [str(s) for s in self.value]
        return '(' + ' '.join(str_list) + ')'


class MalVector(MalType):
    """Mal vector type."""

    def __init__(self, value=[]):
        self.value = value
        self.type = "vector"

    def __str__(self):
        items = [str(s) for s in self.value]
        return '[' + ' '.join(items) + ']'


class MalHash(MalType):
    """Mal hash table type."""

    def __init__(self, value={}):
        self.value = value
        self.type = "hash"

    def __str__(self):
        items = []
        for k, v in self.value.items():
            items.extend([str(k), str(v)])
        return '{' + ' '.join(items) + '}'


class MalSymbol(MalType):
    """Mal symbol type."""

    def __init__(self, name):
        self.name = name
        self.type = "symbol"

    def __str__(self):
        return self.name


class MalError(MalType):
    """Mal error type."""

    def __init__(self, type, descr):
        self.error = type
        self.descr = descr
        self.type = "error"

    def __str__(self):
        return self.error + ": " + self.descr


class MalInt(MalType):
    """Mal integer type."""

    def __init__(self, value):
        self.value = value
        self.type = "integer"

    def __str__(self):
        return str(self.value)


class MalString(MalType):
    """Mal string type."""

    def __init__(self, value):
        self.value = value
        self.type = "string"

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return '"' + self.value + '"'


class MalKeyword(MalType):
    """Mal keyword type."""

    def __init__(self, name):
        self.name = name
        self.type = "keyword"

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name
