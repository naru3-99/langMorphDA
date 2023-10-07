import java.lang.*;
import java.util.*;
import java.util.stream.*;

class SORT_ARRAY_TWO_HALVES_SORTED {

  static void f_gold(int[] A, int n) {
    Arrays.sort(A);
  }

  public static void main(String args[]) {
    f_gold(
      new int[] {
        2,
        3,
        11,
        13,
        18,
        24,
        26,
        30,
        31,
        34,
        42,
        43,
        43,
        44,
        44,
        47,
        49,
        52,
        53,
        55,
        56,
        57,
        58,
        58,
        60,
        64,
        66,
        67,
        69,
        70,
        70,
        71,
        74,
        76,
        77,
        82,
        85,
        89,
        90,
        96,
        98,
      },
      33
    );
  }
}
