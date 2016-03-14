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
        return "#<Mal parent type>"

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


class Symbol(MalType):
    """Mal symbol type."""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

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


class Function(MalType):
    """Mal function type"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "#<Function>"
