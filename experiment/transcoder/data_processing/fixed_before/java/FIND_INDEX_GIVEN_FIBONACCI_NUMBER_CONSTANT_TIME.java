import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class FIND_INDEX_GIVEN_FIBONACCI_NUMBER_CONSTANT_TIME {

  static int f_gold(int n) {
    if (n <= 1) return n;
    int a = 0, b = 1, c = 1;
    int res = 1;
    while (c < n) {
      c = a + b;
      res++;
      a = b;
      b = c;
    }
    return res;
  }

  public static void main(String args[]) {
    f_gold(5);
  }
}
