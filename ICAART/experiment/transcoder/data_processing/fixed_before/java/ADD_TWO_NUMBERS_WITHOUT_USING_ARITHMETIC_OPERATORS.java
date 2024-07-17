import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class ADD_TWO_NUMBERS_WITHOUT_USING_ARITHMETIC_OPERATORS {

  static int f_gold(int x, int y) {
    while (y != 0) {
      int carry = x & y;
      x = x ^ y;
      y = carry << 1;
    }
    return x;
  }

  public static void main(String args[]) {
    f_gold(56, 60);
  }
}
