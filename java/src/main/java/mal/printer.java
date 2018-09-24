package mal;

import mal.types.MalType;

public class printer {
    public static String pr_str(MalType item, boolean print_readably) {
        return item.pr_str(print_readably);
    }
}
