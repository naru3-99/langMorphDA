import java.lang.*;
import java.util.*;
import java.util.stream.*;

class FUNCTION_COPY_STRING_ITERATIVE_RECURSIVE_1 {

  static void f_gold(char s1[], char s2[], int index) {
    s2[index] = s1[index];
    if (index == s1.length - 1) {
      return;
    }
    f_gold(s1, s2, index + 1);
  }

  public static void main(String args[]) {
    f_gold(new char[] { 'v' }, new char[] { 'Z' }, 0);
  }
}
