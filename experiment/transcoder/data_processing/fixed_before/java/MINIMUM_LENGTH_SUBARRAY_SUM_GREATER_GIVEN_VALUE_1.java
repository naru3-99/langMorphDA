import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class MINIMUM_LENGTH_SUBARRAY_SUM_GREATER_GIVEN_VALUE_1 {

  static int f_gold(int arr[], int n, int x) {
    int curr_sum = 0, min_len = n + 1;
    int start = 0, end = 0;
    while (end < n) {
      while (curr_sum <= x && end < n) {
        if (curr_sum <= 0 && x > 0) {
          start = end;
          curr_sum = 0;
        }
        curr_sum += arr[end++];
      }
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
        2,
        4,
        5,
        10,
        14,
        15,
        16,
        20,
        23,
        28,
        31,
        35,
        36,
        36,
        43,
        48,
        49,
        55,
        57,
        57,
        58,
        61,
        64,
        64,
        68,
        70,
        70,
        73,
        74,
        76,
        76,
        77,
        81,
        81,
        82,
        87,
        89,
        92,
        99,
      },
      33,
      28
    );
  }
}
