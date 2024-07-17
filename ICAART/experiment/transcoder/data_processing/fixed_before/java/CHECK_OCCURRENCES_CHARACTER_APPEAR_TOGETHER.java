import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class CHECK_OCCURRENCES_CHARACTER_APPEAR_TOGETHER {

  static boolean f_gold(String s, char c) {
    boolean oneSeen = false;
    int i = 0, n = s.length();
    while (i < n) {
      if (s.charAt(i) == c) {
        if (oneSeen == true) return false;
        while (i < n && s.charAt(i) == c) i++;
        oneSeen = true;
      } else i++;
    }
    return true;
  }

  public static void main(String args[]) {
    f_gold("gILrzLimS", 'm');
  }
}
