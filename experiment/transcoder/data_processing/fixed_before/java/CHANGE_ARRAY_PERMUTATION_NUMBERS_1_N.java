import java.lang.*;
import java.util.*;
import java.util.stream.*;

class CHANGE_ARRAY_PERMUTATION_NUMBERS_1_N {

  static void f_gold(int[] a, int n) {
    HashMap<Integer, Integer> count = new HashMap<Integer, Integer>();
    for (int i = 0; i < n; i++) {
      if (count.containsKey(a[i])) {
        count.put(a[i], count.get(a[i]) + 1);
      } else {
        count.put(a[i], 1);
      }
    }
    int next_missing = 1;
    for (int i = 0; i < n; i++) {
      if (
        count.containsKey(a[i]) && count.get(a[i]) != 1 || a[i] > n || a[i] < 1
      ) {
        count.put(a[i], count.get(a[i]) - 1);
        while (count.containsKey(next_missing)) next_missing++;
        a[i] = next_missing;
        count.put(next_missing, 1);
      }
    }
  }

  public static void main(String args[]) {
    f_gold(new int[] { 19 }, 0);
  }
}
