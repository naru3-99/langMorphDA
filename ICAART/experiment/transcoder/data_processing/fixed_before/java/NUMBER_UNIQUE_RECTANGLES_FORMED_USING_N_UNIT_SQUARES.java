import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class NUMBER_UNIQUE_RECTANGLES_FORMED_USING_N_UNIT_SQUARES {

  static int f_gold(int n) {
    int ans = 0;
    for (int length = 1; length <= Math.sqrt(n); ++length) for (
      int height = length;
      height * length <= n;
      ++height
    ) ans++;
    return ans;
  }

  public static void main(String args[]) {
    f_gold(34);
  }
}
