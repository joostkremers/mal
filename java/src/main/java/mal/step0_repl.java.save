package mal;

import java.io.Console;

public class step0_repl {
  public static void main(String args[]) {
    Console console = System.console();
    String input;
    String output;
    
    while (true) {
      input = console.readLine("user> ");
      if (input == null) {      // Test for EOF
        break; 
      }
      else {
        output = rep(input);
      }
      System.out.println(output);
    }
  }

  public static String READ(String arg) {
    return arg;
  }

  public static String EVAL(String arg) {
    return arg;
  }

  public static String PRINT(String arg) {
    return arg;
  }

  public static String rep(String arg) {
    String result;

    result = PRINT(EVAL(READ(arg)));
    return result;
  }
}