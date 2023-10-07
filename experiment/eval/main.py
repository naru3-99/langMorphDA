import os
from lib763.multp import parallel_process

from lib763.fs import (
    load_str_from_file,
    get_file_rows_iter,
    get_all_file_path_in,
    ensure_path_exists,
    get_file_name_without_ext,
    save_str_to_file,
    get_all_dir_names_in,
    copy_file,
    get_parent_directory,
    get_file_extension,
    get_file_name,
)
from lib763.Bash import Bash
from lib763.Logger import Logger

from eval_func import (
    levenshtein_distance,
    dice_coefficient,
    jaccard_coefficient,
    overlap_coefficient,
    euclidean_distance,
    cosine_similarity,
)
from fix_seq_length import (
    get_path_seq_dict,
    fix_by_bow,
    fix_by_doc2vec,
    fix_by_tfidf,
)
from CONST import (
    BEFORE_PATH,
    AFTER_PATH,
    RESULT_PATH,
    DATA_SAVE_PATH,
    BY_BOW_VEC_SAVE_DIR,
    BY_D2V_VEC_SAVE_DIR,
    BY_IDF_VEC_SAVE_DIR,
    SELECTED_PATH,
    CULC_CA_FILES_PATH,
    CULC_CA_OUTPUT_PATH,
    CA_DATA_PATH,
)

V_EVAL_FUNC_LS = [
    dice_coefficient,
    overlap_coefficient,
    jaccard_coefficient,
    levenshtein_distance,
]
V_NAME_LS = ["dice", "overlap", "jaccard", "levenshtein"]

# 小さいほうが類似度が高いやつら
EVAL_BY_MIN_NAME_LS = ["levenshtein", "euclid"]


def eval_variable_py2j(before_path):
    for func, name in zip(V_EVAL_FUNC_LS, V_NAME_LS):
        res_path = f"{RESULT_PATH}{name}/py2j/"
        ensure_path_exists(res_path)
        test_name = get_file_name_without_ext(before_path)[0:-3]
        if os.path.exists(f"{res_path}{test_name}.txt"):
            continue
        before_scsq_ls = load_str_from_file(before_path).replace("\n", "").split(",")

        name_score_str_ls = []
        for after_path in get_all_file_path_in(f"{AFTER_PATH}java/{test_name}/"):
            after_scsq_ls = load_str_from_file(after_path).replace("\n", "").split(",")
            score = func(before_scsq_ls, after_scsq_ls)
            cand_name = get_file_name_without_ext(after_path)
            name_score_str_ls.append(f"{cand_name},{score}")
        save_str_to_file("\n".join(name_score_str_ls), f"{res_path}{test_name}.txt")


def eval_variable_j2py(before_path):
    for func, name in zip(V_EVAL_FUNC_LS, V_NAME_LS):
        res_path = f"{RESULT_PATH}{name}/j2py/"
        ensure_path_exists(res_path)
        test_name = get_file_name_without_ext(before_path)[0:-5]
        if os.path.exists(f"{res_path}{test_name}.txt"):
            continue
        before_scsq_ls = load_str_from_file(before_path).replace("\n", "").split(",")

        name_score_str_ls = []
        for after_path in get_all_file_path_in(f"{AFTER_PATH}python/{test_name}/"):
            after_scsq_ls = load_str_from_file(after_path).replace("\n", "").split(",")
            score = func(before_scsq_ls, after_scsq_ls)
            cand_name = get_file_name_without_ext(after_path)
            name_score_str_ls.append(f"{cand_name},{score}")
        save_str_to_file("\n".join(name_score_str_ls), f"{res_path}{test_name}.txt")


# # 固定長なやつの評価
# ## ベクトルの作成
def before_java(dir, func):
    ensure_path_exists("".join([DATA_SAVE_PATH, dir]) + "before/java/")
    path_seq_dict = get_path_seq_dict(f"{BEFORE_PATH}java/")
    path_vec_dict = func(path_seq_dict)
    for path, vec in path_vec_dict.items():
        save_str_to_file(
            ",".join([str(i) for i in vec]),
            "".join([DATA_SAVE_PATH, dir, "before/"]) + "/".join(path.split("/")[-2:]),
        )


def before_python(dir, func):
    ensure_path_exists("".join([DATA_SAVE_PATH, dir]) + "before/python/")
    path_seq_dict = get_path_seq_dict(f"{BEFORE_PATH}python/")
    path_vec_dict = func(path_seq_dict)
    for path, vec in path_vec_dict.items():
        save_str_to_file(
            ",".join([str(i) for i in vec]),
            "".join([DATA_SAVE_PATH, dir, "before/"]) + "/".join(path.split("/")[-2:]),
        )


def after_java(dir, func):
    path_seq_dict = get_path_seq_dict(f"{AFTER_PATH}java/")
    path_vec_dict = func(path_seq_dict)
    for path, vec in path_vec_dict.items():
        ensure_path_exists(
            "".join([DATA_SAVE_PATH, dir, "after/"])
            + "/".join(path.split("/")[-3:-1])
            + "/"
        )
        save_str_to_file(
            ",".join([str(i) for i in vec]),
            "".join([DATA_SAVE_PATH, dir, "after/"]) + "/".join(path.split("/")[-3:]),
        )


def after_python(dir, func):
    path_seq_dict = get_path_seq_dict(f"{AFTER_PATH}python/")
    path_vec_dict = func(path_seq_dict)
    for path, vec in path_vec_dict.items():
        ensure_path_exists(
            "".join([DATA_SAVE_PATH, dir, "after/"])
            + "/".join(path.split("/")[-3:-1])
            + "/"
        )
        save_str_to_file(
            ",".join([str(i) for i in vec]),
            "".join([DATA_SAVE_PATH, dir, "after/"]) + "/".join(path.split("/")[-3:]),
        )


# ## 評価
def eval_fixed(eval_func, data_path, name):
    # 与えられたfunc(評価指標)により評価
    # 与えられたdata_path(固定長のベクトルがあるパス)を評価
    # name(評価指標名)のディレクトリにアウトプット

    # python => java
    res_path = f"{RESULT_PATH}{name}/py2j/"
    ensure_path_exists(res_path)
    for before_path in get_all_file_path_in(f"{data_path}before/python/"):
        test_name = get_file_name_without_ext(before_path)[0:-3]
        before_vec_ls = load_str_from_file(before_path).replace("\n", "").split(",")
        before_vec_ls = [float(v) for v in before_vec_ls]

        name_score_str_ls = []
        for after_path in get_all_file_path_in(f"{data_path}after/java/{test_name}/"):
            after_vec_ls = load_str_from_file(after_path).replace("\n", "").split(",")
            after_vec_ls = [float(v) for v in after_vec_ls]
            score = eval_func(before_vec_ls, after_vec_ls)
            cand_name = get_file_name_without_ext(after_path)
            name_score_str_ls.append(f"{cand_name},{score}")
        save_str_to_file("\n".join(name_score_str_ls), f"{res_path}{test_name}.txt")

    # java => python
    res_path = f"{RESULT_PATH}{name}/j2py/"
    ensure_path_exists(res_path)
    for before_path in get_all_file_path_in(f"{data_path}before/java/"):
        test_name = get_file_name_without_ext(before_path)[0:-5]
        before_vec_ls = load_str_from_file(before_path).replace("\n", "").split(",")
        before_vec_ls = [float(v) for v in before_vec_ls]

        name_score_str_ls = []
        for after_path in get_all_file_path_in(f"{data_path}after/python/{test_name}/"):
            after_vec_ls = load_str_from_file(after_path).replace("\n", "").split(",")
            after_vec_ls = [float(v) for v in after_vec_ls]
            score = eval_func(before_vec_ls, after_vec_ls)
            cand_name = get_file_name_without_ext(after_path)
            name_score_str_ls.append(f"{cand_name},{score}")
        save_str_to_file("\n".join(name_score_str_ls), f"{res_path}{test_name}.txt")


def execute_and_get_comacc(path):
    # 与えられたpath(計算機精度を計算するためのテストのパス)
    # を実行して、標準出力に出力された結果をログとして返す
    bash = Bash(get_parent_directory(path), "")
    if get_file_extension(path) == ".py":
        # execute python file
        _, retcode, stdout, stderr = bash.execute(
            command=f"python -u {get_file_name(path)}", timeout=100
        )
    else:
        # java tests
        java_class_name = get_file_name_without_ext(path)
        # compile java file
        _, retcode, stdout, stderr = bash.execute(
            f"javac -encoding UTF-8 {java_class_name}.java", timeout=100
        )
        if retcode != 0:
            return retcode, stdout, "compile error\n" + stderr
        # execute java file
        _, retcode, stdout, stderr = bash.execute(command=f"java {java_class_name}")
    return retcode, stdout, stderr


if __name__ == "__main__":
    # 固定長じゃないヤツ
    parallel_process(eval_variable_py2j, get_all_file_path_in(f"{BEFORE_PATH}python/"))
    parallel_process(eval_variable_j2py, get_all_file_path_in(f"{BEFORE_PATH}java/"))

    # 固定長なやつ
    ## ベクトルの作成
    func_ls = [before_java, before_python, after_java, after_python]
    fix_func_dict = {
        BY_BOW_VEC_SAVE_DIR: fix_by_bow,
        BY_D2V_VEC_SAVE_DIR: fix_by_doc2vec,
        BY_IDF_VEC_SAVE_DIR: fix_by_tfidf,
    }
    for dir, ffunc in fix_func_dict.items():
        for func in func_ls:
            func(dir, ffunc)

    ## 評価
    eval_func_ls = [euclidean_distance, cosine_similarity]
    eval_name_ls = ["euclid", "cossim"]
    _dir_name_ls = [
        BY_BOW_VEC_SAVE_DIR,
        BY_D2V_VEC_SAVE_DIR,
        BY_IDF_VEC_SAVE_DIR,
    ]
    data_path_ls = [DATA_SAVE_PATH + dirname for dirname in _dir_name_ls]
    vec_name_ls = [dirname[:-1] for dirname in _dir_name_ls]
    for efunc, ename in zip(eval_func_ls, eval_name_ls):
        for dpath, vname in zip(data_path_ls, vec_name_ls):
            eval_fixed(efunc, dpath, f"{ename}_{vname}")

    # 結果の集計
    for dirname1 in get_all_dir_names_in(f"{RESULT_PATH}"):
        # 指標が大きいければ類似度が高い->max;else min;
        how_eval = max
        for min_name in EVAL_BY_MIN_NAME_LS:
            if min_name in dirname1:
                how_eval = min
                break
        # ./result/cossim_bow/など
        path1 = f"{RESULT_PATH}{dirname1}/"
        for dirname2 in get_all_dir_names_in(path1):
            # ./result/cossim_bow/j2py/など
            path2 = f"{path1}{dirname2}/"
            # ['testname,best filename, best score'...]
            tname_fname_score_ls = []
            for path in get_all_file_path_in(path2):
                testname = get_file_name_without_ext(path)
                file_row_ls = get_file_rows_iter(path)
                if len(file_row_ls) == 1 and len(file_row_ls[0]) == 0:
                    best_fname, best_score = None, None
                else:
                    fname_score_ls = [
                        [row.split(",")[0], float(row.split(",")[1])]
                        for row in file_row_ls
                    ]
                    best_fname, best_score = how_eval(
                        fname_score_ls, key=lambda x: x[1]
                    )
                tname_fname_score_ls.append(f"{testname},{best_fname},{best_score}")
            save_path = f"{SELECTED_PATH}{dirname1}/{dirname2}/"
            ensure_path_exists(save_path)
            save_str_to_file(
                "\n".join(tname_fname_score_ls), f"{save_path}selected.txt"
            )

    # ## 最善の翻訳候補の計算機精度を計算するファイルを取得
    for dirname1 in get_all_dir_names_in(f"{SELECTED_PATH}"):
        # ./selected/cossim_bow/など
        path1 = f"{SELECTED_PATH}{dirname1}/"

        # java => python
        ca_files_path = f"{CULC_CA_FILES_PATH}python/"
        save_path = f"{CULC_CA_OUTPUT_PATH}{dirname1}/j2py/"
        ensure_path_exists(save_path)
        for row in get_file_rows_iter(f"{path1}j2py/selected.txt"):
            testname, filename, _ = row.split(",")
            if filename == "None":
                continue
            cand_num = filename.split("_")[1]
            copy_file(
                f"{ca_files_path}{testname}/cand_{cand_num}.py",
                f"{save_path}{testname}.py",
            )

        # python => java
        ca_files_path = f"{CULC_CA_FILES_PATH}java/"
        save_path = f"{CULC_CA_OUTPUT_PATH}{dirname1}/py2j/"
        ensure_path_exists(save_path)
        for row in get_file_rows_iter(f"{path1}py2j/selected.txt"):
            testname, filename, _ = row.split(",")
            if filename == "None":
                continue
            cand_num = filename.split("_")[1]
            copy_file(
                f"{ca_files_path}{testname}/cand_{cand_num}.java",
                f"{save_path}{testname}.java",
            )

    # patch: numpy
    for path in get_all_file_path_in(CULC_CA_OUTPUT_PATH):
        if get_file_extension(path) == ".py":
            save_str_to_file(
                "\n".join(["import numpy as np"] + get_file_rows_iter(path)), path
            )

    # メタのテストを実行する
    for dirname1 in get_all_dir_names_in(CULC_CA_OUTPUT_PATH):
        # dirname1 = 'cossim_bow'など
        path1 = f"{CULC_CA_OUTPUT_PATH}{dirname1}/"
        for dirname2 in get_all_dir_names_in(path1):
            # dirname2 = 'j2py' or 'py2j'
            path2 = f"{path1}{dirname2}/"
            for path in get_all_file_path_in(path2):
                # path = 'testname.py or java'のパス
                retcode, stdout, stderr = execute_and_get_comacc(path)
                save_path = f"{CA_DATA_PATH}{dirname1}/{dirname2}/"
                ensure_path_exists(save_path)
                save_str_to_file(
                    f"retcode={retcode}\n\nstdout=\n{stdout}\n\nstderr=\n{stderr}",
                    f"{save_path}{get_file_name_without_ext(path)}.txt",
                )

    # ca_resultからデータを引っ張ってくる
    ensure_path_exists('./ca_temp/')
    for dirname1 in get_all_dir_names_in(CA_DATA_PATH):
        path1 = f"{CA_DATA_PATH}{dirname1}/"
        for dirname2 in get_all_dir_names_in(path1):
            path2 = f"{path1}{dirname2}/"
            testname_result_ls = []
            for path in get_all_file_path_in(path2):
                row_ls = get_file_rows_iter(path)
                retcode = None
                for row in row_ls:
                    if "retcode" in row:
                        retcode = row.split("=")[1]
                        break
                if retcode is None:
                    continue
                result = None
                if retcode == "0":
                    for row in row_ls:
                        if row.startswith("#"):
                            result = row.replace("#Results:", "").replace(" ", "")
                if result is None:
                    continue
                testname_result_ls.append(
                    f"{get_file_name_without_ext(path)}, {result}"
                )
            save_str_to_file(
                "\n".join(testname_result_ls),
                f"./ca_temp/{dirname1}_{dirname2}.txt",
            )

    path_comaccave_dict = {}
    for path in get_all_file_path_in("./ca_temp"):
        sum_of_correct = 0
        for row in get_file_rows_iter(path):
            testname, correct, _ = row.replace(" ", "").split(",")
            sum_of_correct += int(correct)
        path_comaccave_dict[get_file_name_without_ext(path)] = sum_of_correct / 6150

    lgr = Logger("./log")
    for k, v in path_comaccave_dict.items():
        lgr.add_log(f"{k} : {v}")
