import javalang
import ast

from lib763.fs import (
    load_str_from_file,
    save_str_to_file,
    get_all_file_path_in,
    get_file_name,
    get_all_file_names_in,
    ensure_path_exists,
    rmrf,
)

P_TGT_FUNC_DIR = "./tgt_data/python_func/"
J_TGT_FUNC_DIR = "./tgt_data/java_func/"
P_META_TEST_DIR = "./data/evaluation/geeks_for_geeks_successful_test_scripts/python/"
J_META_TEST_DIR = "./data/evaluation/geeks_for_geeks_successful_test_scripts/java/"


def extract_java_func(java_path):
    """
    Javaファイルからf_gold関数の実装を抜き取る。

    Args:
        file_path (str): Javaファイルのパス。

    Returns:
        str: f_gold関数の実装コード。関数が見つからない場合は空の文字列。
    """
    file_content = load_str_from_file(java_path)

    # Javaのソースコードを解析
    tree = javalang.parse.parse(file_content)

    # すべてのクラスとインターフェイスを反復処理
    for type_declaration in tree.types:
        if isinstance(
            type_declaration,
            (javalang.tree.ClassDeclaration, javalang.tree.InterfaceDeclaration),
        ):
            # すべてのメソッドを反復処理
            for method in type_declaration.methods:
                if method.name == "f_gold":
                    # f_gold関数の開始位置を取得
                    start_pos = method.position
                    lines = file_content.split("\n")
                    brace_count = 0
                    for i in range(start_pos.line - 1, len(lines)):
                        brace_count += lines[i].count("{") - lines[i].count("}")
                        if brace_count == 0:
                            end_line = i
                            break
                    return "\n".join(lines[start_pos.line - 1 : end_line + 1])
    return ""


def extract_python_func(py_path):
    """
    Pythonファイルからf_gold関数の実装を抜き取る。

    Args:
        file_path (str): Pythonファイルのパス。

    Returns:
        str: f_gold関数の実装コード。関数が見つからない場合は空の文字列。
    """
    file_content = load_str_from_file(py_path)

    # Pythonのソースコードを解析
    tree = ast.parse(file_content)

    # すべての関数定義を反復処理
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "f_gold":
            # f_gold関数のソースコードを抽出
            start_line = node.lineno - 1
            end_line = node.end_lineno
            return "\n".join(file_content.split("\n")[start_line:end_line])
    return ""


def main():
    # 同じファイル名のファイルが存在しているかどうか確認し、
    # なければ削除する
    java_file_noext_ls = [
        name.split(".")[0] for name in get_all_file_names_in(J_META_TEST_DIR)
    ]
    python_file_noext_ls = [
        name.split(".")[0] for name in get_all_file_names_in(P_META_TEST_DIR)
    ]
    for jfile in java_file_noext_ls:
        if not jfile in python_file_noext_ls:
            rmrf(f"{J_META_TEST_DIR}{jfile}.java")
    for pyfile in python_file_noext_ls:
        if not pyfile in java_file_noext_ls:
            rmrf(f"{P_META_TEST_DIR}{pyfile}.py")

    # javaのファイルからf_gold関数を抜き出し、保存する
    ensure_path_exists(J_TGT_FUNC_DIR)
    for jpath in get_all_file_path_in(J_META_TEST_DIR):
        try:
            save_str_to_file(
                extract_java_func(jpath), f"{J_TGT_FUNC_DIR}{get_file_name(jpath)}"
            )
        except:
            print(jpath)

    # 同じくpythonも
    ensure_path_exists(P_TGT_FUNC_DIR)
    for pypath in get_all_file_path_in(P_META_TEST_DIR):
        try:
            save_str_to_file(
                extract_python_func(pypath),
                f"{P_TGT_FUNC_DIR}{get_file_name(pypath)}",
            )
        except:
            print(pypath)

if __name__ == '__main__':
    main()
