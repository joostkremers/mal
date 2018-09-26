package mal;

import java.util.HashMap;

import mal.types.MalException;
import mal.types.MalFunction;
import mal.types.MalInt;
import mal.types.MalList;
import mal.types.MalSymbol;
import mal.types.MalType;

public class core {
    // Built-in integer arithmetic functions.
    //
    // Although these functions are obvious candidates for reduce(), the fact that
    // we need to handle errors makes that too cumbersome.

    private static int checkMalInt(MalType arg) throws MalException {
        if (arg instanceof MalInt)
            return (int)arg.getJValue();
        else throw new MalException("Wrong argument type: expected int, got " + arg.getType() + ".");
    }

    static MalFunction malAdd = new MalFunction() {
            @Override
            public MalInt apply(MalList args) throws MalException {
                int result = 0;

                for(MalType i : args.getJValue()) {
                    result += checkMalInt(i);
                }
                return new MalInt(result);
            }
        };

    static MalFunction malSubtract = new MalFunction() {
            @Override
            public MalInt apply(MalList args) throws MalException {
                int size = args.getJValue().size();

                if (size == 0) return new MalInt(0);

                int result = checkMalInt(args.get(0));
                if (size == 1) return new MalInt(-result);

                for (MalType i : args.getJValue().subList(1,size)) {
                    result -= checkMalInt(i);
                }
                return new MalInt(result);
            }
        };

    static MalFunction malMultiply = new MalFunction() {
            @Override
            public MalInt apply(MalList args) throws MalException {
                int result = 1;

                for(MalType i : args.getJValue()) {
                    result *= checkMalInt(i);
                }
                return new MalInt(result);
            }
        };

    static MalFunction malDivide = new MalFunction() {
            @Override
            public MalInt apply(MalList args) throws MalException {
                int size = args.getJValue().size();

                if (size == 0) throw new MalException("Wrong number of arguments: required >1, received 0.");

                int result = checkMalInt(args.get(0));
                if (size == 1) return new MalInt(1/result); // These are integers, so this will always return 0.

                for (MalType i : args.getJValue().subList(1,size)) {
                    result /= checkMalInt(i);
                }
                return new MalInt(result);
            }
        };

    static HashMap<MalSymbol,MalFunction> ns = new HashMap<>();

    static {
        ns.put(new MalSymbol("+"), malAdd);
        ns.put(new MalSymbol("-"), malSubtract);
        ns.put(new MalSymbol("*"), malMultiply);
        ns.put(new MalSymbol("/"), malDivide);
    }
}
