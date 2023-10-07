import java.lang.*;
import java.util.*;
import java.util.stream.*;

class REARRANGE_POSITIVE_AND_NEGATIVE_NUMBERS_PUBLISH {

  static void f_gold(int arr[], int n) {
    int i = -1, temp = 0;
    for (int j = 0; j < n; j++) {
      if (arr[j] < 0) {
        i++;
        temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
      }
    }
    int pos = i + 1, neg = 0;
    while (pos < n && neg < pos && arr[neg] < 0) {
      temp = arr[neg];
      arr[neg] = arr[pos];
      arr[pos] = temp;
      pos++;
      neg += 2;
    }
  }

  public static void main(String args[]) {
    f_gold(
      new int[] {
        5,
        5,
        6,
        7,
        8,
        10,
        13,
        15,
        15,
        27,
        27,
        29,
        29,
        29,
        29,
        31,
        33,
        33,
        36,
        38,
        38,
        39,
        42,
        47,
        47,
        51,
        51,
        51,
        52,
        53,
        55,
        56,
        57,
        64,
        66,
        66,
        67,
        68,
        70,
        72,
        74,
        78,
        86,
        88,
        94,
        97,
        97,
      },
      26
    );
  }
}
