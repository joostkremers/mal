import mal_types as mal


class Env():
    """Mal environment class.

    An environment mapping symbols to Mal objects. Note that the symbols are
    stored as strings, not as Mal objects.

    """

    def __init__(self, outer=None, data={}):
        self.outer = outer
        self.data = data

    def set(self, symbol, value):
        self.data[symbol] = value

    def find(self, symbol):
        if symbol in self.data:
            return self
        elif self.outer is not None:
            return self.outer.find(symbol)
        else:
            return None

    def get(self, symbol):
        env = self.find(symbol)
        if env:
            return env.data[symbol]
        else:
            return mal.Error("SymbolError",
                             "Symbol's value is void '{}'". format(symbol))
