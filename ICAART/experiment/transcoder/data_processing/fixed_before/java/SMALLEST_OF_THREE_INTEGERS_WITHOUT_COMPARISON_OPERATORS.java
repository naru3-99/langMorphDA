import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class SMALLEST_OF_THREE_INTEGERS_WITHOUT_COMPARISON_OPERATORS {

  static int f_gold(int x, int y, int z) {
    int c = 0;
    while (x != 0 && y != 0 && z != 0) {
      x--;
      y--;
      z--;
      c++;
    }
    return c;
  }

  public static void main(String args[]) {
    f_gold(23, 98, 25);
  }
}
