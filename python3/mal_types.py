class MalType:
    """Parent type of all Mal-specific types."""

    # This makes it easier to define certain properties that apply to all or
    # most types, such as equality.

    # We can use MalType when we need to have an object that has no effect
    # whatsoever. VALUE in this case can indicate why this object exists. We do
    # this with comments, for example.
    def __init__(self, object):
        self.value = object

    def __str__(self):
        return ""

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (self.value == other.value)


class Nil(MalType):
    """Mal nil type."""

    def __init__(self):
        self.value = None

    def __str__(self):
        return "nil"


class Vector(MalType):
    """Mal vector type."""

    def __init__(self, value=None):
        if value is None:
            self.value = []
        else:
            self.value = value

    def __str__(self):
        items = [str(s) for s in self.value]
        return '[' + ' '.join(items) + ']'

    def __eq__(self, other):
        if isinstance(self, Vector):
            val1 = self.value
        else:
            val1 = self
        if isinstance(other, Vector):
            val2 = other.value
        else:
            val2 = other

        return val1 == val2


class Symbol(MalType):
    """Mal symbol type."""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Mal Symbol object '{}'>".format(self.name)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (self.name == other.name)


class Error(MalType):
    """Mal error type."""

    def __init__(self, error_type, descr):
        self.error = error_type
        self.descr = descr

    def __str__(self):
        return self.error + ": " + self.descr

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return ((self.error_type == other.error_type) and
                self.descr == other.descr)


class Keyword(MalType):
    """Mal keyword type."""

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (self.name == other.name)

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name


class Builtin(MalType):
    """Mal builtin function type."""

    def __init__(self, fn=None):
        self.fn = fn

    def __str__(self):
        return "#<Builtin function>"


class Function(MalType):
    """Mal function type."""

    def __init__(self, fn=None, params=None, ast=None, env=None):
        self.fn = fn
        self.params = params
        self.ast = ast
        self.env = env

    def __str__(self):
        return "#<User function>"


class Atom(MalType):
    """Mal atom type."""

    def __init__(self, value=None):
        if value is None:
            self.value = Nil()
        else:
            self.value = value

    def set(self, value):
        self.value = value

    def __str__(self):
        return '(atom ' + self.value.__str__() + ')'
