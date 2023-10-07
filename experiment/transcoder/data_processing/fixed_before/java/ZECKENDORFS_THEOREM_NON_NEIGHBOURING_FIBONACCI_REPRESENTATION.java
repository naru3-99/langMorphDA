import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class ZECKENDORFS_THEOREM_NON_NEIGHBOURING_FIBONACCI_REPRESENTATION {

  public static int f_gold(int n) {
    if (n == 0 || n == 1) return n;
    int f1 = 0, f2 = 1, f3 = 1;
    while (f3 <= n) {
      f1 = f2;
      f2 = f3;
      f3 = f1 + f2;
    }
    return f2;
  }

  public static void main(String args[]) {
    f_gold(54);
  }
}
