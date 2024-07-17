import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class NUMBER_IS_DIVISIBLE_BY_29_OR_NOT {

  static boolean f_gold(long n) {
    while (n / 100 > 0) {
      int last_digit = (int) n % 10;
      n /= 10;
      n += last_digit * 3;
    }
    return (n % 29 == 0);
  }

  public static void main(String args[]) {
    f_gold(29L);
  }
}
