class MalType:
    """Parent type of all MaL types."""

    def __init__(self, object):
        self.value = object

    def __str__(self):
        return str(object)


class MalList(MalType):
    """MaL list type."""

    def __init__(self, value=[]):
        self.value = value

    def __str__(self):
        str_list = [str(s) for s in self.value]
        return '(' + ' '.join(str_list) + ')'


class MalSymbol(MalType):
    """MaL symbol type."""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class MalError(MalType):
    """MaL error type."""

    def __init__(self, type, descr):
        self.type = type
        self.descr = descr

    def __str__(self):
        return self.type + ": " + self.descr


class MalInt(MalType):
    """MaL integer type."""

    def __str__(self):
        return str(self.value)


class MalString(MalType):
    """MaL string type."""

    def __str__(self):
        return '"' + self.value + '"'
