import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class MINIMUM_LENGTH_SUBARRAY_SUM_GREATER_GIVEN_VALUE {

  static int f_gold(int arr[], int n, int x) {
    int curr_sum = 0, min_len = n + 1;
    int start = 0, end = 0;
    while (end < n) {
      while (curr_sum <= x && end < n) curr_sum += arr[end++];
      while (curr_sum > x && start < n) {
        if (end - start < min_len) min_len = end - start;
        curr_sum -= arr[start++];
      }
    }
    return min_len;
  }

  public static void main(String args[]) {
    f_gold(
      new int[] {
        6,
        11,
        11,
        14,
        18,
        19,
        21,
        22,
        22,
        23,
        26,
        27,
        28,
        28,
        29,
        30,
        31,
        34,
        39,
        42,
        42,
        44,
        45,
        49,
        49,
        53,
        57,
        61,
        65,
        66,
        67,
        70,
        71,
        73,
        74,
        74,
        78,
        85,
        88,
        94,
        95,
        97,
      },
      37,
      23
    );
  }
}
