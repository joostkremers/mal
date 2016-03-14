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

    def __eq__(self, other):
        if self.type == other.type and self.value == other.value:
            return True
        else:
            return False


class List(MalType):
    """Mal list type."""

    def __init__(self, value=None):
        if value is None:
            self.value = []
        else:
            self.value = value
        self.type = "list"

    def __str__(self):
        str_list = [str(s) for s in self.value]
        return '(' + ' '.join(str_list) + ')'


class Nil(MalType):
    """Mal nil type."""

    def __init__(self):
        self.value = None
        self.type = "nil"

    def __str__(self):
        return "nil"


class Vector(MalType):
    """Mal vector type."""

    def __init__(self, value=None):
        if value is None:
            self.value = []
        else:
            self.value = value
        self.type = "vector"

    def __str__(self):
        items = [str(s) for s in self.value]
        return '[' + ' '.join(items) + ']'


class Hash(MalType):
    """Mal hash table type."""

    def __init__(self, value=None):
        if value is None:
            self.value = {}
        else:
            self.value = value
        self.type = "hash"

    def __str__(self):
        items = []
        for k, v in self.value.items():
            items.extend([str(k), str(v)])
        return '{' + ' '.join(items) + '}'


class Symbol(MalType):
    """Mal symbol type."""

    def __init__(self, name):
        self.name = name
        self.type = "symbol"

    def __str__(self):
        return self.name


class Error(MalType):
    """Mal error type."""

    def __init__(self, type, descr):
        self.error = type
        self.descr = descr
        self.type = "error"

    def __str__(self):
        return self.error + ": " + self.descr


class Int(MalType):
    """Mal integer type."""

    def __init__(self, value):
        self.value = value
        self.type = "integer"

    def __str__(self):
        return str(self.value)


class String(MalType):
    """Mal string type."""

    def __init__(self, value):
        self.value = value
        self.type = "string"

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return '"' + self.value + '"'


class Keyword(MalType):
    """Mal keyword type."""

    def __init__(self, name):
        self.name = name
        self.type = "keyword"

    def __eq__(self, other):
        if self.type == other.type and self.name == other.name:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name


class Boolean(MalType):
    """Mal boolean type."""

    def __init__(self, value):
        self.value = value
        self.type = "boolean"

    def __str__(self):
        if self.value is True:
            return "true"
        else:
            return "false"


class Function(MalType):
    """Mal function type"""

    def __init__(self, value):
        self.value = value
        self.type = "function"

    def __str__(self):
        return "#<Function>"
