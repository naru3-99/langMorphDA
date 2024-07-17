import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class PRODUCT_NODES_K_TH_LEVEL_TREE_REPRESENTED_STRING {

  static int f_gold(String tree, int k) {
    int level = -1;
    int product = 1;
    int n = tree.length();
    for (int i = 0; i < n; i++) {
      if (tree.charAt(i) == '(') level++; else if (
        tree.charAt(i) == ')'
      ) level--; else {
        if (level == k) product *= (tree.charAt(i) - '0');
      }
    }
    return product;
  }

  public static void main(String args[]) {
    f_gold("(0(5(6()())(4()(9()())))(7(1()())(3()())))", 2);
  }
}
