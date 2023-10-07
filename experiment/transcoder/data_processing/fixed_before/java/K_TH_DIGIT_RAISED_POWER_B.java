import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class K_TH_DIGIT_RAISED_POWER_B {

  public static int f_gold(int a, int b, int k) {
    int p = (int) Math.pow(a, b);
    int count = 0;
    while (p > 0 && count < k) {
      int rem = p % 10;
      count++;
      if (count == k) return rem;
      p = p / 10;
    }
    return 0;
  }

  public static void main(String args[]) {
    f_gold(11, 2, 1);
  }
}
