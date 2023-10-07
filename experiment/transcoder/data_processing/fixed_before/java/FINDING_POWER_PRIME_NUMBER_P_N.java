import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class FINDING_POWER_PRIME_NUMBER_P_N {

  static int f_gold(int n, int p) {
    int ans = 0;
    for (int i = 1; i <= n; i++) {
      int count = 0, temp = i;
      while (temp % p == 0) {
        count++;
        temp = temp / p;
      }
      ans += count;
    }
    return ans;
  }

  public static void main(String args[]) {
    f_gold(49, 30);
  }
}
