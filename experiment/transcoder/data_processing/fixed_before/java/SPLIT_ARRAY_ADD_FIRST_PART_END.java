import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class SPLIT_ARRAY_ADD_FIRST_PART_END {

  public static void f_gold(int arr[], int n, int k) {
    for (int i = 0; i < k; i++) {
      int x = arr[0];
      for (int j = 0; j < n - 1; ++j) arr[j] = arr[j + 1];
      arr[n - 1] = x;
    }
  }

  public static void main(String args[]) {
    f_gold(new int[] { 75 }, 0, 0);
  }
}
