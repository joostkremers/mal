package mal;

import java.io.Console;

import mal.types.MalException;
import mal.types.MalType;

public class step1_read_print {
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
        try {
          output = rep(input);
        }
        catch(MalException ex) {
          output = "*** Error *** " + ex.getMessage();
        }
      }
      System.out.println(output);
    }
  }

  public static MalType READ(String arg) throws MalException {
    return reader.read_str(arg);
  }

  public static MalType EVAL(MalType arg) {
    return arg;
  }

  public static String PRINT(MalType arg) {
    return printer.pr_str(arg);
  }

  public static String rep(String arg) throws MalException {
    String result;

    result = PRINT(EVAL(READ(arg)));
    return result;
  }
}
