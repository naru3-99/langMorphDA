import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class WRITE_A_C_PROGRAM_TO_FIND_THE_PARITY_OF_AN_UNSIGNED_INTEGER {

  static boolean f_gold(int n) {
    boolean parity = false;
    while (n != 0) {
      parity = !parity;
      n = n & (n - 1);
    }
    return parity;
  }

  public static void main(String args[]) {
    f_gold(63);
  }
}
