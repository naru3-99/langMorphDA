import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class SUM_K_TH_GROUP_ODD_POSITIVE_NUMBERS {

  public static int f_gold(int k) {
    int cur = (k * (k - 1)) + 1;
    int sum = 0;
    while (k-- > 0) {
      sum += cur;
      cur += 2;
    }
    return sum;
  }

  public static void main(String args[]) {
    f_gold(91);
  }
}
