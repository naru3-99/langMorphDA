import java.lang.*;
import java.util.*;
import java.util.stream.*;

class POSITIVE_ELEMENTS_EVEN_NEGATIVE_ODD_POSITIONS {

  static void f_gold(int a[], int size) {
    int positive = 0, negative = 1, temp;
    while (true) {
      while (positive < size && a[positive] >= 0) positive += 2;
      while (negative < size && a[negative] <= 0) negative += 2;
      if (positive < size && negative < size) {
        temp = a[positive];
        a[positive] = a[negative];
        a[negative] = temp;
      } else break;
    }
  }

  public static void main(String args[]) {
    f_gold(
      new int[] {
        8,
        11,
        18,
        23,
        24,
        28,
        28,
        34,
        35,
        42,
        44,
        53,
        57,
        65,
        71,
        72,
        76,
        78,
        82,
        82,
        85,
        86,
        92,
        93,
      },
      15
    );
  }
}
