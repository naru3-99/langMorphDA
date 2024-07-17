import java.lang.*;
import java.util.*;
import java.util.stream.*;

public class FIND_EXPRESSION_DUPLICATE_PARENTHESIS_NOT {

  static boolean f_gold(String s) {
    Stack<Character> Stack = new Stack<>();
    char[] str = s.toCharArray();
    for (char ch : str) {
      if (ch == ')') {
        char top = Stack.peek();
        Stack.pop();
        int elementsInside = 0;
        while (top != '(') {
          elementsInside++;
          top = Stack.peek();
          Stack.pop();
        }
        if (elementsInside < 1) {
          return true;
        }
      } else {
        Stack.push(ch);
      }
    }
    return false;
  }

  public static void main(String args[]) {
    f_gold("((a+b)+((c+d)))");
  }
}
