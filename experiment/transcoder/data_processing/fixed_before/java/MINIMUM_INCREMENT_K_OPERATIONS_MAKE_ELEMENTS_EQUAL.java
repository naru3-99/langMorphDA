import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class MINIMUM_INCREMENT_K_OPERATIONS_MAKE_ELEMENTS_EQUAL {

  static int f_gold(int arr[], int n, int k) {
    Arrays.sort(arr);
    int max = arr[arr.length - 1];
    int res = 0;
    for (int i = 0; i < n; i++) {
      if ((max - arr[i]) % k != 0) return -1; else res += (max - arr[i]) / k;
    }
    return res;
  }

  public static void main(String args[]) {
    f_gold(new int[] { 4, 7, 19, 16 }, 4, 3);
  }
}
