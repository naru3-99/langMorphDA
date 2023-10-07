import java.lang.*;
import java.util.*;
import java.util.stream.*;

class SWAP_TWO_NUMBERS_WITHOUT_USING_TEMPORARY_VARIABLE {

  static void f_gold(int[] xp, int[] yp) {
    xp[0] = xp[0] ^ yp[0];
    yp[0] = xp[0] ^ yp[0];
    xp[0] = xp[0] ^ yp[0];
  }

  public static void main(String args[]) {
    f_gold(
      new int[] {
        2,
        7,
        12,
        13,
        15,
        17,
        24,
        27,
        28,
        31,
        36,
        44,
        55,
        55,
        56,
        58,
        60,
        62,
        64,
        73,
        75,
        77,
        89,
        90,
        93,
        93,
        95,
        97,
        98,
      },
      new int[] {
        5,
        8,
        12,
        13,
        14,
        20,
        23,
        25,
        27,
        28,
        31,
        33,
        33,
        37,
        38,
        39,
        42,
        42,
        43,
        47,
        52,
        54,
        62,
        67,
        71,
        72,
        73,
        76,
        77,
        79,
        81,
        81,
        85,
        86,
        89,
        91,
        91,
        96,
        96,
        99,
      }
    );
  }
}
