import java.lang.*;
import java.util.*;
import java.util.stream.*;

class REARRANGE_ARRAY_MAXIMUM_MINIMUM_FORM_SET_2_O1_EXTRA_SPACE {

  public static void f_gold(int arr[], int n) {
    int max_idx = n - 1, min_idx = 0;
    int max_elem = arr[n - 1] + 1;
    for (int i = 0; i < n; i++) {
      if (i % 2 == 0) {
        arr[i] += (arr[max_idx] % max_elem) * max_elem;
        max_idx--;
      } else {
        arr[i] += (arr[min_idx] % max_elem) * max_elem;
        min_idx++;
      }
    }
    for (int i = 0; i < n; i++) arr[i] = arr[i] / max_elem;
  }

  public static void main(String args[]) {
    f_gold(
      new int[] {
        1,
        1,
        2,
        3,
        9,
        10,
        14,
        22,
        26,
        28,
        29,
        29,
        30,
        32,
        32,
        32,
        34,
        37,
        39,
        40,
        42,
        42,
        42,
        43,
        45,
        47,
        49,
        52,
        53,
        54,
        56,
        58,
        59,
        68,
        71,
        73,
        76,
        81,
        81,
        83,
        84,
        91,
        94,
      },
      29
    );
  }
}
