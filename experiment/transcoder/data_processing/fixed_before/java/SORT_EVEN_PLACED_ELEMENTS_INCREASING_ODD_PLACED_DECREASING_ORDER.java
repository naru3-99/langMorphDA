import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class SORT_EVEN_PLACED_ELEMENTS_INCREASING_ODD_PLACED_DECREASING_ORDER {

  public static void f_gold(int arr[], int n, int k) {
    for (int i = 0; i < k; i++) {
      int x = arr[0];
      for (int j = 0; j < n - 1; ++j) arr[j] = arr[j + 1];
      arr[n - 1] = x;
    }
  }

  public static void main(String args[]) {
    f_gold(
      new int[] {
        -58,
        -60,
        -38,
        48,
        -2,
        32,
        -48,
        -46,
        90,
        -54,
        -18,
        28,
        72,
        86,
        0,
        -2,
        -74,
        12,
        -58,
        90,
        -30,
        10,
        -88,
        2,
        -14,
        82,
        -82,
        -46,
        2,
        -74,
      },
      27,
      17
    );
  }
}
