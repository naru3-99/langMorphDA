import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class CHECK_GIVEN_STRING_ROTATION_PALINDROME {

  static boolean f_gold(String str) {
    int l = 0;
    int h = str.length() - 1;
    while (h > l) if (str.charAt(l++) != str.charAt(h--)) return false;
    return true;
  }

  public static void main(String args[]) {
    f_gold("aadaa");
  }
}
