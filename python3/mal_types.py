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
        if type(self) is Vector:
            val1 = self.value
        else:
            val1 = self
        if type(other) is Vector:
            val2 = other.value
        else:
            val2 = other

        return val1 == val2

    def __len__(self):
        return len(self.value)

    def __contains__(self, x):
        return x in self.value

    def __getitem__(self, x):
        return self.value[x]


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
    """Mal error type.

    Errors are returned as normal values, but they halt evaluation and are
    immediately returned to the top level.
    """

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


class HandledError(Error):
    """Mal handled error type.

    Errors handled by 'try*/catch*' are passed as handled errors, so that they
    do not halt evaluation.
    """

    def __init__(self, error_object):
        self.error = error_object.error
        self.descr = error_object.descr


class Keyword(MalType):
    """Mal keyword type. """

    def __init__(self, name):
        """Create a keyword.

        Keywords are strings that start with a colon. If NAME does not start
        with a colon, one is added.
        """
        if name[0] != ":":
            name = ':' + name
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
        return "#<Builtin function at {}>".format(hex(id(self)))


class Function(MalType):
    """Mal function type."""

    def __init__(self, fn=None, params=None, ast=None, env=None,
                 is_macro=False):
        self.fn = fn
        self.params = params
        self.ast = ast
        self.env = env
        self.is_macro = is_macro

    def __str__(self):
        if self.is_macro:
            fn_type = "macro"
        else:
            fn_type = "funcion"
        return "#<User {} at {}>".format(fn_type, hex(id(self)))


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
