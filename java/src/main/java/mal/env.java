package mal;

import java.util.HashMap;

import mal.types.MalException;
import mal.types.MalSymbol;
import mal.types.MalType;

public class env {
    public static class Env {
        Env outer;
        HashMap<MalSymbol,MalType> data = new HashMap<>();

        Env(Env outer) {
            this.outer = outer;
        }

        Env(Env outer, List<MalType> binds, List<MalType> exprs) throws MalException {
            if (binds.size() != exprs.size()) throw new MalException("Binds list does not match expressions list.");

            for (int i = 0; i<binds.size(); i++) {
                if (!(binds.get(i) instanceof MalSymbol)) throw new MalException("Cannot bind non-symbol: " + binds.get(i).toString());
            }
            this.set(binds.get(i), exprs.get(i));

            this.outer = outer;
        }

        public void set(MalSymbol symbol, MalType value) {
            data.put(symbol, value);
        }

        public Env find(MalSymbol symbol) {
            if (data.containsKey(symbol)) return this;
            else if (outer == null) return null;
            else return outer.find(symbol);
        }

        public MalType get(MalSymbol symbol) throws MalException {
            Env env = this.find(symbol);

            if (env != null) return env.data.get(symbol);
            else throw new MalException("Symbol value is void: " + symbol.toString());
        }
    }
}
