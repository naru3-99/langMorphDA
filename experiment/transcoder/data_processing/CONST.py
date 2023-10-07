# いずれも、J2PY = java->pythonつまりpythonのファイル
#         PY2J = python->javaつまりjavaのファイル

# codegenから引っ張ってきたテスト用のエントリがあるファイル
# このフォルダ直下に'内容.py or java'が存在
J2PY_META_TEST_DIR = (
    "../TransCoder/data/evaluation/geeks_for_geeks_successful_test_scripts/python/"
)
PY2J_META_TEST_DIR = (
    "../TransCoder/data/evaluation/geeks_for_geeks_successful_test_scripts/java/"
)

# 翻訳対象の関数f_goldだけを抜き出したファイル
JAVA_TGT_FUNC_DIR = "../TransCoder/tgt_data/java_func/"
PYTHON_TGT_FUNC_DIR = "../TransCoder/tgt_data/python_func/"

# transcoderで生成した関数のファイルのパス
# このフォルダ直下に'内容/cand_0.py'などが存在
J2PY_GENERATED_DIR = "../../../created_data/generated/java2python/"
PY2J_GENERATED_DIR = "../../../created_data/generated/python2java/"

# テスト(計算機精度など、meta式)の保存先
J2PY_EVAL_TEST_DIR = "./eval_tests/python/"
PY2J_EVAL_TEST_DIR = "./eval_tests/java/"

# 翻訳後の関数f_filledのdaテストの保存先
AFTER_DA_PYTHON_DIR = "../../../created_data/after_da/python/"
AFTER_DA_JAVA_DIR = "../../../created_data/after_da/java/"

# 翻訳前の関数f_goldのdaテストの保存先
BEFORE_DA_JAVA_DIR = "../../../created_data/before_da/java/"
BEFORE_DA_PYTHON_DIR = "../../../created_data/before_da/python/"

# 手動で直したコードのディレクトリ
FIXED_BEFORE_JAVA_DIR = "./fixed_before/java"
FIXED_BEFORE_PYTHON_DIR = "./fixed_before/python"
