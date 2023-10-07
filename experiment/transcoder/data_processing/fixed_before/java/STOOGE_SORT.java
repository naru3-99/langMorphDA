import java.lang.*;
import java.util.*;
import java.util.stream.*;

class STOOGE_SORT {

  static void f_gold(int arr[], int l, int h) {
    if (l >= h) return;
    if (arr[l] > arr[h]) {
      int t = arr[l];
      arr[l] = arr[h];
      arr[h] = t;
    }
    if (h - l + 1 > 2) {
      int t = (h - l + 1) / 3;
      f_gold(arr, l, h - t);
      f_gold(arr, l + t, h);
      f_gold(arr, l, h - t);
    }
  }

  public static void main(String args[]) {
    f_gold(new int[] { 6, 25, 42, 52, 53, 54, 58, 66, 67, 70 }, 6, 6);
  }
}
