import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class CHECK_WHETHER_TWO_STRINGS_ARE_ANAGRAM_OF_EACH_OTHER {

  static boolean f_gold(char[] str1, char[] str2) {
    int n1 = str1.length;
    int n2 = str2.length;
    if (n1 != n2) return false;
    Arrays.sort(str1);
    Arrays.sort(str2);
    for (int i = 0; i < n1; i++) if (str1[i] != str2[i]) return false;
    return true;
  }

  public static void main(String args[]) {
    f_gold("LISTEN".toCharArray(), "SILENT".toCharArray());
  }
}
