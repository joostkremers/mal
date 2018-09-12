package mal;

import java.util.Arrays;
import java.util.StringJoiner;

public class types {
  public abstract static class MalType {

    public abstract Object get();

    public abstract String pr_str();
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
  }

  // Cf. http://www.vogella.com/tutorials/JavaDatastructureList/article.html
  public static class MalList extends MalType {
    private int size = 0;
    private static final int DEFAULT_LENGTH = 10;
    private MalType items[];
    
    public MalList() {
      items = new MalType[DEFAULT_LENGTH];
    }

    public void add(MalType e) {
      if (size == items.length) {
        ensureCapacity();
      }
      items[size++] = e;
    }

    private void ensureCapacity() {
      int newSize = size * 2;
      items = Arrays.copyOf(items, newSize);
    }

    // This is needed so that MalList can extend MalType. As an alternative, we
    // might return the instance itself, or implement `get` in MalType.
    public MalType get() {
      return null;
    }
    
    public MalType get(int i) {
      if (i >= size || i < 0) {
        throw new IndexOutOfBoundsException("(MalList) Index out of Bounds: " + i + "(" + size + ")");
      }
      return items[i];
    }

    public String pr_str() {
      StringJoiner result = new StringJoiner(" ", "(", ")");

      for(int i = 0; i < size; i++) {
        result.add(items[i].pr_str());
      }

      return result.toString();
    }
  }
  
  public static class MalError extends MalType {
    String message;

    public MalError(String message) {
      this.message = message;
    }

    public String get() {
      return message;
    }

    public String pr_str() {
      return message;
    }
}

  public static class MalString extends MalType {
    String value;

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

  }
  
  public static class MalComment extends MalType {
    String comment;

    public MalComment(String comment) {
      this.comment = comment;
    }

    public String get() {
      return comment;
    }

    public String pr_str() {
      return comment;
    }
  }

  public static class MalSymbol extends MalType {
    String name;

    public MalSymbol(String name) {
      this.name = name;
    }

    public String get() {
      return name;
    }

    public String pr_str() {
      return name;
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
}
