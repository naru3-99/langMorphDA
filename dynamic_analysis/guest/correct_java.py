# 2023/09/19
# auther:naru
# encoding=utf-8

from typing import Optional
from javalang import parse
from javalang.tree import ClassDeclaration, MethodDeclaration

from lib763.fs import get_file_name, load_str_from_file, save_str_to_file


def extract_class_name(java_code: str) -> Optional[str]:
    """Given a string of java code, extract and return the class name of the class containing the main method.

    Args:
        java_code (str): The java code from which to extract the class name.

    Returns:
        str: The name of the class if found, None otherwise.

    Raises:
        Exception: If there is an error while parsing the java code.
    """
    try:
        tree = parse.parse(java_code)
        for path, node in tree.filter(ClassDeclaration):
            for _, method in node.filter(MethodDeclaration):
                if method.name == "main" and "static" in method.modifiers:
                    return node.name
    except Exception as e:
        print("Javaコードのパース中にエラーが発生しました:", e)
    return None


def correct_java_class_name(java_file_path: str) -> bool:
    """
    Given a java file path, this function corrects the class name in the file to match the file name.
    It extracts the class name from the java code, replaces it with the file name, and saves the updated code to the file.

    Args:
        java_file_path (str): The path of the java file to be corrected.

    Returns:
        bool: True if the class name was corrected successfully, False otherwise.
    """
    try:
        current_java_code = load_str_from_file(java_file_path)
        class_name_in_code = extract_class_name(current_java_code)
        if class_name_in_code == None:
            return False
        class_name_from_filename = get_file_name(java_file_path).split(".")[0]
        new_code = current_java_code.replace(
            class_name_in_code, class_name_from_filename
        )
        new_code = "\n".join(
            [row for row in new_code.split("\n") if not "package " in row]
        )
        save_str_to_file(new_code, java_file_path)
    except:
        return False
    return True
