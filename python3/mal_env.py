import mal_types as mtype


class MalEnv():
    """Mal environment class.

    An environment mapping symbols to Mal objects. Note that the symbols should
    be strings, not Mal objects, although the initializer accepts both strings
    naming symbols and mal_types.Symbol.

    """

    def __init__(self, outer=None, data=None, binds=[], exprs=[]):
        self.outer = outer

        if data is None:
            self.data = {}
        else:
            self.data = data

        for i in range(len(binds)):
            if isinstance(binds[i], mtype.Symbol):
                sym = binds[i].name
            else:
                sym = binds[i]

            if sym == '&':
                sym = binds[i+1]
                val = list(exprs)[i:]
                self.set(sym, val)
                break

            else:
                if i < len(exprs):
                    val = exprs[i]
                else:
                    val = mtype.Nil()

            self.set(sym, val)

    def set(self, symbol, value):
        if isinstance(symbol, mtype.Symbol):
            symbol = symbol.name
        if isinstance(symbol, str):
            self.data[symbol] = value
            return value
        else:
            return mtype.Error("TypeError", "Cannot bind to non-symbol")

    def find(self, symbol):
        if isinstance(symbol, mtype.Symbol):
            symbol = symbol.name
        if symbol in self.data:
            return self
        elif self.outer is None:
            return None
        else:
            return self.outer.find(symbol)

    def get(self, symbol):
        if isinstance(symbol, mtype.Symbol):
            symbol = symbol.name
        env = self.find(symbol)
        if env:
            return env.data[symbol]
        else:
            return mtype.Error("SymbolError",
                               "Symbol's value is void '{}'". format(symbol))
