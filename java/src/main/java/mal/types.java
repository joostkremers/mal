package mal;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.StringJoiner;

public class types {
  public abstract static class MalType {

    protected String type = "type";

    public abstract Object get();

    public abstract String pr_str(boolean readably);

    public String toString() {
      return this.toString();
    }

    public String getType() {
      return type;
    }
  }

  public static class MalInt extends MalType {
    private int value;

    public MalInt(int value) {
      this.value = value;
      this.type = "int";
    }

    @Override
    public Integer get() {
      return value;
    }

    @Override
    public String pr_str(boolean readably) {
      return Integer.toString(value);
    }
  }

  public static abstract class MalSequence extends MalType {
    List<MalType> items;

    @Override
    public List<MalType> get() {
      return items;
    }

    public int size() {
      return items.size();
    }

    public void add(MalType e) {
      items.add(e);
    }

    public MalType get(int i) {
      return items.get(i);
    }

    public abstract MalType subList(int beg, int end);
  }

  public static class MalList extends MalSequence {
    public MalList() {
      this.items = new LinkedList<MalType>();
      this.type = "list";
    }

    public MalList(List items) {
      this.items = items;
      this.type = "list";
    }

    @Override
    public String pr_str(boolean readably) {
      StringJoiner result = new StringJoiner(" ", "(", ")");

      for(MalType item : items) {
        result.add(item.pr_str(readably));
      }

      return result.toString();
    }

    @Override
    public MalList subList(int beg, int end) {
      return new MalList(items.subList(beg, end));
    }
  }

  public static class MalVector extends MalSequence {
    public MalVector() {
      this.items = new ArrayList<MalType>();
      this.type = "vector";
    }

    public MalVector(List items) {
      this.items = items;
      this.type = "vector";
    }

    public void add(MalType e) {
      items.add(e);
    }

    public MalType get(int i) {
      return items.get(i);
    }

    @Override
    public String pr_str(boolean readably) {
      StringJoiner result = new StringJoiner(" ", "[", "]");

      for(MalType item : items) {
        result.add(item.pr_str(readably));
      }

      return result.toString();
    }

    @Override
    public MalVector subList(int beg, int end) {
      return new MalVector(items.subList(beg, end));
    }
  }

  public static class MalHash extends MalType {
    private HashMap<MalType,MalType> map;

    public MalHash() {
      map = new HashMap<MalType,MalType>();
      this.type = "hash-map";
    }

    public void put(MalType k, MalType v) {
      map.put(k, v);
    }

    public MalType get(MalType k) {
      return map.get(k);
    }

    @Override
    public HashMap get() {
      return map;
    }

    @Override
    public String pr_str(boolean readably) {
      StringJoiner result = new StringJoiner(", ", "{", "}");

      for (HashMap.Entry<MalType,MalType> entry : map.entrySet()) {
        MalType key = entry.getKey();
        MalType value = entry.getValue();
        result.add(key.pr_str(readably) + " " + value.pr_str(readably));
      }

      return result.toString();
    }
  }

  public static class MalString extends MalType {
    private String value;

    public MalString(String value) {
      this.value = value;
      this.type = "string";
    }

    @Override
    public String get() {
      return value;
    }

    @Override
    public String pr_str(boolean readably) {
      if (readably == false) return value;
      else {
        String result;

        result = value.replace("\\", "\\\\");
        result = result.replace("\n", "\\n");
        result = result.replace("\"", "\\\"");

        return "\"" + result + "\"";
      }
    }
  }

  public static class MalSymbol extends MalType {
    private String name;

    public MalSymbol(String name) {
      this.name = name;
      this.type = "symbol";
    }

    @Override
    public String get() {
      return name;
    }

    @Override
    public String pr_str(boolean readably) {
      return name;
    }
  }

  public static class MalKeyword extends MalType {
    private String name;

    public MalKeyword(String name) {
      this.name = name;
      this.type = "keyword";
    }

    @Override
    public String get() {
      return name;
    }

    @Override
    public String pr_str(boolean readably) {
      return name;
    }
  }

  public static class MalNil extends MalType {

    public MalNil() {
      this.type = "symbol";
    }

    @Override
    public Boolean get() {
      return false;
    }

    @Override
    public String pr_str(boolean readably) {
      return "nil";
    }
  }

  public static class MalBoolean extends MalType {
    Boolean value;

    public MalBoolean(boolean value) {
      this.value = value;
      this.type = "boolean";
    }

    @Override
    public Boolean get() {
      return value;
    }

    @Override
    public String pr_str(boolean readably) {
      return value.toString();
    }
  }

  @FunctionalInterface
  static abstract interface MalCallable {
    public MalType apply(MalList args) throws MalException;
  }

  public static abstract class MalFunction extends MalType implements MalCallable {
    public MalFunction() {
      this.type = "function";
    }

    @Override
    public Object get() {
      return this;
    }

    @Override
    public String pr_str(boolean readably) {
      return this.toString();
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
