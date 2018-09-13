package mal;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.StringJoiner;

public class types {
  public abstract static class MalType {

    public abstract Object get();

    public abstract String pr_str();

    public abstract String getType();
  }

  public static class MalInt extends MalType {
    private int value;

    public MalInt(int value) {
      this.value = value;
    }

    public Integer get() {
      return value;
    }

    public String pr_str() {
      return Integer.toString(value);
    }

    public String getType() {
      return "MalInt";
    }
  }

  public static abstract class MalSequence extends MalType {
    List<MalType> items;

    public List<MalType> get() {
      return items;
    }

    public void add(MalType e) {
      items.add(e);
    }

    public MalType get(int i) {
      return items.get(i);
    }

    public String getType() {
      return "MalSequence";
    }
  }

  public static class MalList extends MalSequence {
    public MalList() {
      items = new LinkedList<MalType>();
    }

    public String pr_str() {
      StringJoiner result = new StringJoiner(" ", "(", ")");

      for(MalType item : items) {
        result.add(item.pr_str());
      }

      return result.toString();
    }

      public String getType() {
      return "MalList";
    }
}

  public static class MalVector extends MalSequence {
    public MalVector() {
      items = new ArrayList<MalType>();
    }

    public void add(MalType e) {
      items.add(e);
    }

    public MalType get(int i) {
      return items.get(i);
    }

    public String pr_str() {
      StringJoiner result = new StringJoiner(" ", "[", "]");

      for(MalType item : items) {
        result.add(item.pr_str());
      }

      return result.toString();
    }

    public String getType() {
      return "MalVector";
    }
  }

  // public static class MalError extends MalType {
  //   private String message;

  //   public MalError(String message) {
  //     this.message = message;
  //   }

  //   public String get() {
  //     return message;
  //   }

  //   public String pr_str() {
  //     return message;
  //   }
  // }

  public static class MalString extends MalType {
    private String value;

    public MalString(String value) {
      this.value = value;
    }

    public String get() {
      return value;
    }

    // This needs proper escaping of characters.
    public String pr_str() {
      return "\"" + value + "\"";
    }

    public String getType() {
      return "MalString";
    }
  }

  public static class MalSymbol extends MalType {
    private String name;

    public MalSymbol(String name) {
      this.name = name;
    }

    public String get() {
      return name;
    }

    public String pr_str() {
      return name;
    }

      public String getType() {
      return "MalSymbol";
    }
  }

    public static class MalKeyword extends MalType {
    private String name;

    public MalKeyword(String name) {
      this.name = name;
    }

    public String get() {
      return name;
    }

    public String pr_str() {
      return name;
    }

    public String getType() {
      return "MalKeyword";
    }
  }

  public static class MalNil extends MalType {

    public MalNil() {
      // Nothing to do.
    }

    public Boolean get() {
      return false;
    }

    public String pr_str() {
      return "nil";
    }
}

  public static class MalFalse extends MalType {

    public MalFalse() {
      // Nothing to do.
    }

    public Boolean get() {
      return false;
    }

    public String pr_str() {
      return "false";
    }
}

  public static class MalTrue extends MalType {

    public MalTrue() {
      // Nothing to do.
    }

    public Boolean get() {
      return true;
    }

    public String pr_str() {
      return "true";
    }
  }

  public static class MalException extends Exception {
    private static final long serialVersionUID = 1L;
    public MalException() { super(); }
    public MalException(String message) { super(message); }
    public MalException(String message, Throwable cause) { super(message, cause); }
    public MalException(Throwable cause) { super(cause); }
  }
}
