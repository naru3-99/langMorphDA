import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class HOW_CAN_WE_SUM_THE_DIGITS_OF_A_GIVEN_NUMBER_IN_SINGLE_STATEMENT {

  static int f_gold(int n) {
    int sum = 0;
    while (n != 0) {
      sum = sum + n % 10;
      n = n / 10;
    }
    return sum;
  }

  public static void main(String args[]) {
    f_gold(57);
  }
}
