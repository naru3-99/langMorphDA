import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class COUNT_SET_BITS_IN_AN_INTEGER_2 {

  static int f_gold(int n) {
    int count = 0;
    while (n > 0) {
      n &= (n - 1);
      count++;
    }
    return count;
  }

  public static void main(String args[]) {
    f_gold(32);
  }
}
