from gensim.models import Doc2Vec
from concurrent.futures import ProcessPoolExecutor, as_completed
import math

from lib763.fs import (
    load_str_from_file,
    get_all_file_path_in,
)

from CONST import (
    DOC2VEC_MODEL_PATH,
    VOCAB_CSV_PATH,
)


def get_path_seq_dict(path):
    return {
        data_path: load_str_from_file(data_path).replace("\n", "").split(",")
        for data_path in get_all_file_path_in(path)
        if data_path
    }


# def fix_by_doc2vec(data_seq_dict: dict):
#     model = Doc2Vec.load(DOC2VEC_MODEL_PATH)
#     return {path: model.infer_vector(seq) for path, seq in data_seq_dict.items()}


def infer_doc_vector(model, seq):
    return model.infer_vector(seq)


def fix_by_doc2vec(data_seq_dict: dict):
    model = Doc2Vec.load(DOC2VEC_MODEL_PATH)
    with ProcessPoolExecutor() as executor:
        future_to_path = {
            executor.submit(infer_doc_vector, model, seq): path
            for path, seq in data_seq_dict.items()
        }
        return {
            future_to_path[future]: future.result()
            for future in as_completed(future_to_path.keys())
        }


def fix_by_bow(path_seq_dict: dict):
    vocab_ls = load_str_from_file(VOCAB_CSV_PATH).replace("\n", "").split(",")
    word_dict = {word: 0 for word in vocab_ls}

    path_vector_dict = {}
    for path, seq in path_seq_dict.items():
        wdict = word_dict.copy()
        for word in seq:
            wdict[word] += 1
        path_vector_dict[path] = list(wdict.values())
    return path_vector_dict


def fix_by_tfidf(path_seq_dict: dict):
    # idfを計算する
    vocab_ls = load_str_from_file(VOCAB_CSV_PATH).replace("\n", "").split(",")
    word_doccnt_dict = {word: 0 for word in vocab_ls}
    for seq in path_seq_dict.values():
        for word in vocab_ls:
            if word in set(seq):
                word_doccnt_dict[word] += 1
    idf_ls = []
    doc_num = len(path_seq_dict.keys())
    for word in vocab_ls:
        if word_doccnt_dict[word] == 0:
            idf_ls.append(0)
            continue
        idf_ls.append(math.log(doc_num / (word_doccnt_dict[word])))

    path_tfidf_dict = {}
    for path, bow in fix_by_bow(path_seq_dict).items():
        word_num = sum(bow)
        tf_ls = [b / word_num for b in bow]
        path_tfidf_dict[path] = [tf * idf for tf, idf in zip(tf_ls, idf_ls)]
    return path_tfidf_dict
