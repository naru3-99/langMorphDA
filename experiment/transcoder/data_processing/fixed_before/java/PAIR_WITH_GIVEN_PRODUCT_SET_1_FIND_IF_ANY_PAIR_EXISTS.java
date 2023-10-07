import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class PAIR_WITH_GIVEN_PRODUCT_SET_1_FIND_IF_ANY_PAIR_EXISTS {

  static boolean f_gold(int arr[], int n, int x) {
    for (int i = 0; i < n - 1; i++) for (int j = i + 1; j < n; j++) if (
      arr[i] * arr[j] == x
    ) return true;
    return false;
  }

  public static void main(String args[]) {
    f_gold(new int[] { 10, 20, 9, 40 }, 4, 400);
  }
}
