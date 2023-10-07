import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class FIND_MAXIMUM_SUM_POSSIBLE_EQUAL_SUM_THREE_STACKS {

  public static int f_gold(
    int stack1[],
    int stack2[],
    int stack3[],
    int n1,
    int n2,
    int n3
  ) {
    int sum1 = 0, sum2 = 0, sum3 = 0;
    for (int i = 0; i < n1; i++) sum1 += stack1[i];
    for (int i = 0; i < n2; i++) sum2 += stack2[i];
    for (int i = 0; i < n3; i++) sum3 += stack3[i];
    int top1 = 0, top2 = 0, top3 = 0;
    int ans = 0;
    while (true) {
      if (top1 == n1 || top2 == n2 || top3 == n3) return 0;
      if (sum1 == sum2 && sum2 == sum3) return sum1;
      if (sum1 >= sum2 && sum1 >= sum3) sum1 -= stack1[top1++]; else if (
        sum2 >= sum3 && sum2 >= sum3
      ) sum2 -= stack2[top2++]; else if (sum3 >= sum2 && sum3 >= sum1) sum3 -=
        stack3[top3++];
    }
  }

  public static void main(String args[]) {
    f_gold(
      new int[] {
        4,
        10,
        11,
        24,
        27,
        33,
        34,
        36,
        36,
        40,
        42,
        43,
        52,
        58,
        67,
        69,
        77,
        86,
        86,
        88,
      },
      new int[] {
        4,
        13,
        34,
        40,
        41,
        47,
        47,
        52,
        55,
        62,
        66,
        66,
        69,
        70,
        73,
        74,
        75,
        76,
        85,
        98,
      },
      new int[] {
        6,
        8,
        10,
        12,
        14,
        29,
        41,
        52,
        53,
        54,
        55,
        66,
        69,
        73,
        77,
        77,
        78,
        80,
        90,
        99,
      },
      10,
      12,
      18
    );
  }
}
