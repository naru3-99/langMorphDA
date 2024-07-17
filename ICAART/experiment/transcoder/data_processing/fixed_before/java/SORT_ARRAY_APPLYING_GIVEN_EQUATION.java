import java.lang.*;
import java.util.*;
import java.util.stream.*;

class SORT_ARRAY_APPLYING_GIVEN_EQUATION {

  static void f_gold(int arr[], int n, int A, int B, int C) {
    for (int i = 0; i < n; i++) arr[i] = A * arr[i] * arr[i] + B * arr[i] + C;
    int index = -1;
    int maximum = -999999;
    for (int i = 0; i < n; i++) {
      if (maximum < arr[i]) {
        index = i;
        maximum = arr[i];
      }
    }
    int i = 0, j = n - 1;
    int[] new_arr = new int[n];
    int k = 0;
    while (i < index && j > index) {
      if (arr[i] < arr[j]) new_arr[k++] = arr[i++]; else new_arr[k++] =
        arr[j--];
    }
    while (i < index) new_arr[k++] = arr[i++];
    while (j > index) new_arr[k++] = arr[j--];
    new_arr[n - 1] = maximum;
    for (int p = 0; p < n; p++) arr[p] = new_arr[p];
  }

  public static void main(String args[]) {
    f_gold(new int[] { 9, 30, 49, 65, 78, 85, 85, 92 }, 4, 4, 5, 4);
  }
}
