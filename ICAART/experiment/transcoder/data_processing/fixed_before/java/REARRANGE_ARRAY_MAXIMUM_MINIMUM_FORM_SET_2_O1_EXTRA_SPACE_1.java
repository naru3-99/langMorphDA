import java.lang.*;
import java.util.*;
import java.util.stream.*;

class REARRANGE_ARRAY_MAXIMUM_MINIMUM_FORM_SET_2_O1_EXTRA_SPACE_1 {

  public static void f_gold(int arr[], int n) {
    int max_ele = arr[n - 1];
    int min_ele = arr[0];
    for (int i = 0; i < n; i++) {
      if (i % 2 == 0) {
        arr[i] = max_ele;
        max_ele -= 1;
      } else {
        arr[i] = min_ele;
        min_ele += 1;
      }
    }
  }

  public static void main(String args[]) {
    f_gold(
      new int[] {
        3,
        4,
        8,
        10,
        12,
        14,
        14,
        17,
        18,
        19,
        20,
        25,
        28,
        29,
        30,
        31,
        34,
        35,
        37,
        38,
        40,
        41,
        42,
        45,
        47,
        49,
        54,
        54,
        55,
        58,
        58,
        63,
        65,
        66,
        66,
        67,
        67,
        72,
        74,
        75,
        75,
        80,
        82,
        86,
        92,
        95,
        96,
        99,
      },
      40
    );
  }
}
