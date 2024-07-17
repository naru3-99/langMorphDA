import java.lang.*;
import java.util.*;
import java.util.stream.*;

class SORT_EVEN_NUMBERS_ASCENDING_ORDER_SORT_ODD_NUMBERS_DESCENDING_ORDER_1 {

  static void f_gold(int arr[], int n) {
    for (int i = 0; i < n; i++) if ((arr[i] & 1) != 0) arr[i] *= -1;
    Arrays.sort(arr);
    for (int i = 0; i < n; i++) if ((arr[i] & 1) != 0) arr[i] *= -1;
  }

  public static void main(String args[]) {
    f_gold(new int[] { 4 }, 0);
  }
}
