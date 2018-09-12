package mal;

import java.io.Console;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import mal.types.MalError;
import mal.types.MalList;
import mal.types.MalSequence;
import mal.types.MalType;
import mal.types.MalVector;

public class reader {
  static Console console = System.console();

  static private HashMap<String, String> delims;
  static {
    delims = new HashMap<String, String>();
    delims.put("(", ")");
    delims.put("[", "]");
  }

  public static class Reader {
    List<String> tokens = new LinkedList<>();
    int position = 0;

    public Reader(List<String> tokens) {
      this.tokens = tokens;
    }

    public String peek() {
      if (position < tokens.size())
        return tokens.get(position);
      else return null;
    }

    public String next() {
      if (position < tokens.size())
        return tokens.get(position++);
      else return null;
    }
  }

  public static List<String> tokenizer(String inputLine) {
    // The regexp is modified a bit so as to require tokens to be consecutive.
    // Not sure if this is really a good idea. Note that I don't actually do
    // anything with this in the while loop.
    String tokenRegexString = "\\G[\\s,]*(~@|[\\[\\]{}\\(\\)'`~^@]|\"(?:\\.|[^\\\"])*\"|;.*|[^\\s\\[\\]{}\\('\"`,;\\)]+)";
    Pattern tokenRegex = Pattern.compile(tokenRegexString);
    Matcher inputMatcher = tokenRegex.matcher(inputLine);

    List<String> tokenizedInput = new LinkedList<>();

    String token;

    while (inputMatcher.find()) {
      token = inputMatcher.group(1);
      tokenizedInput.add(token);
    }

    console.format("Tokenized input: %s%n", tokenizedInput);

    return tokenizedInput;
  }

  public static MalType read_str(String inputLine) {
    Reader tokenized_input;

    tokenized_input = new Reader(tokenizer(inputLine));
    return read_form(tokenized_input);
  }

  private static MalType read_form(Reader inputForm) {
    MalType result = null;
    String item;

    item = inputForm.peek();

    console.format("Item: %s%n", item);

    if (item != null) {
      switch (item) {
      case "(":
      case "[":
        result = read_list(inputForm);
        break;

      default:
        result = read_atom(inputForm);
        break;
      }
    }
    return result;
  }

  private static MalType read_list(Reader inputForm) {
    MalSequence result;
    String item;

    String openingDelim = inputForm.next();
    String closingDelim = delims.get(openingDelim);

    switch (openingDelim) {
    case "(": result = new MalList();
      break;
    case "[": result = new MalVector();
      break;
    default: return new MalError("Not a list delimiter: " + openingDelim);
    }

    while (true) {
      item = inputForm.peek();

      console.format("List item: %s%n", item);

      if (item == null) return new MalError("Malformed input: expected «" + closingDelim + "», found EOL");
      if (item.equals(closingDelim)) {
        inputForm.next(); // Move past the list's closing parenthesis.
        return result;
      }

      MalType parsedItem = read_form(inputForm);
      if (parsedItem instanceof MalError) return parsedItem;
      else result.add(parsedItem);
    }

    // do {
    //   item = inputForm.peek();

    //   if (item != null) {
    //     MalType malItem = read_form(inputForm);
    //     if (malItem instanceof types.MalError)
    //       return malItem;
    //     else result.add(malItem);
    //     item = inputForm.next();
    //   }
    // } while ((item instanceof String) && (item != ")"));

    // if (item == null)  // inputForm was exhausted but no closing parenthesis was found.
    //   return new types.MalError("Malformed input");
    // else {

    //   return result;
    }

  private static MalType read_atom(Reader inputForm) {
    String item = inputForm.next();

    console.format("Atom: %s%n", item);

    Pattern
      // rxUnquoteSplicing  = Pattern.compile("~@"),
      // rxSpecialChar  = Pattern.compile("[\\[\\]{}\\(\\)'`~^@]"),
      rxString = Pattern.compile("\"(?:\\.|[^\\\"])*\""),
      rxComment = Pattern.compile(";.*"),
      rxNumber = Pattern.compile("[0-9]+"),
      rxSymbol = Pattern.compile("[^\\s\\[\\]{}\\('\"`,;\\)]+");

    if (rxString.matcher(item).matches())
      return new types.MalString(item);
    else if (rxComment.matcher(item).matches())
      return new types.MalComment(item);
    else if (rxNumber.matcher(item).matches())
      return new types.MalInt(Integer.parseInt(item));
    else if (item.equals("nil"))
      return new types.MalNil();
    else if (item.equals("false"))
      return new types.MalFalse();
    else if (item.equals("true"))
      return new types.MalTrue();
    else if (rxSymbol.matcher(item).matches())
      return new types.MalSymbol(item);
    else return new types.MalError("Unknown token in input string: " + item);
  }
}
