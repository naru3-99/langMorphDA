import java.lang.*;
import java.util.*;
import java.util.stream.*;

class SORT_ARRAY_CONTAIN_1_N_VALUES {

  static void f_gold(int[] arr, int n) {
    for (int i = 0; i < n; i++) {
      arr[i] = i + 1;
    }
  }

  public static void main(String args[]) {
    f_gold(
      new int[] {
        3,
        3,
        6,
        7,
        9,
        11,
        15,
        15,
        17,
        19,
        21,
        23,
        26,
        27,
        37,
        48,
        48,
        51,
        53,
        53,
        59,
        64,
        69,
        69,
        70,
        71,
        72,
        84,
        93,
        96,
      },
      19
    );
  }
}
