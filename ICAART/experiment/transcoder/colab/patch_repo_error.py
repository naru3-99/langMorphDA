from lib763.fs import (
    save_str_to_file,
    load_str_from_file,
    get_all_file_path_in,
    get_file_name,
)
from extract_fgold_func import P_META_TEST_DIR, J_META_TEST_DIR

save_str_to_file(
    load_str_from_file("../colab/patch/code_tokenizer.txt"),
    "./preprocessing/src/code_tokenizer.py",
)
for path in get_all_file_path_in("../colab/patch"):
    if ".py" in path:
        save_str_to_file(
            load_str_from_file(path),
            P_META_TEST_DIR + get_file_name(path),
        )
    elif ".java" in path:
        save_str_to_file(
            load_str_from_file(path),
            J_META_TEST_DIR + get_file_name(path),
        )
