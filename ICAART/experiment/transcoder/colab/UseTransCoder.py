# 2023/08/09
# auther:naru
# encoding=utf-8

# 本クラスは与えられたディレクトリの中にあるすべての
# プログラムをTransCoderに入力し、翻訳候補を作成します。

# usage:
# !python UseTransCoder.py \
# --src_lang python --tgt_lang java \
# --model_path model_2.pth --beam_size 100 \
# --save_dir save_dir --tgt_dir tgt_data/python_func


import os
import torch
import argparse

from lib763.fs import (
    save_str_to_file,
    load_str_from_file,
    mkdir,
    get_file_name,
    get_file_name_without_ext,
    get_file_extension,
    get_all_file_path_in,
    get_all_dir_names_in,
)
from lib763.Logger import Logger

from translate import Translator, SUPPORTED_LANGUAGES

SUPPORTED_EXT_DICT = {"cpp": ".cpp", "java": ".java", "python": ".py"}
logger = Logger("./log.txt")


def get_parser():
    """
    Generate a parameters parser.
    """
    # parse parameters
    parser = argparse.ArgumentParser(description="Translate sentences")

    # model
    parser.add_argument("--model_path", type=str, default="", help="Model path")
    parser.add_argument(
        "--src_lang",
        type=str,
        default="",
        help=f"Source language, should be either {', '.join(SUPPORTED_LANGUAGES[:-1])} or {SUPPORTED_LANGUAGES[-1]}",
    )
    parser.add_argument(
        "--tgt_lang",
        type=str,
        default="",
        help=f"Target language, should be either {', '.join(SUPPORTED_LANGUAGES[:-1])} or {SUPPORTED_LANGUAGES[-1]}",
    )
    parser.add_argument(
        "--BPE_path",
        type=str,
        default="data/BPE_with_comments_codes",
        help="Path to BPE codes.",
    )
    parser.add_argument(
        "--beam_size",
        type=int,
        default=1,
        help="Beam size. The beams will be printed in order of decreasing likelihood.",
    )
    parser.add_argument(
        "--save_dir",
        type=str,
        default="save_dir",
        help="directory for saving translate candidates.",
    )
    parser.add_argument(
        "--tgt_dir",
        type=str,
        default="tgt_dir",
        help="target directory path that contains target program files",
    )
    return parser


class UseTransCoder:
    def __init__(self, params) -> None:
        """
        Initializes the UseTransCoder class.

        Args:
            params: A dictionary containing the parameters for the translator.
        """
        # Initialize translator
        self.params = params
        self.translator = Translator(params)

    def create_candidate(self, input_code_path: str):
        """
        Creates a translation candidate for the given input code.

        Args:
            input_code_path: The path to the input code file.

        Returns:
            A list of translation candidates.
        """
        input_code = load_str_from_file(input_code_path)
        with torch.no_grad():
            output = self.translator.translate(
                input_code,
                lang1=self.params.src_lang,
                lang2=self.params.tgt_lang,
                beam_size=self.params.beam_size,
            )
        return output

    def one_iter(self, input_code_path: str):
        """
        Performs one iteration of translation for the given input code.

        Args:
            input_code_path: The path to the input code file.
        """
        # target file name and extension
        file_name_no_ext = get_file_name(input_code_path).split(".")[0]
        save_file_extension = SUPPORTED_EXT_DICT[self.params.tgt_lang]

        # prepare for saving directory
        mkdir(self.params.save_dir, file_name_no_ext)

        # create translate candidate
        candidate_ls = self.create_candidate(input_code_path)

        # save all candidate
        for i, cand in enumerate(candidate_ls):
            save_path = os.path.join(
                self.params.save_dir, file_name_no_ext, f"Cand_{i}{save_file_extension}"
            )
            save_str_to_file(cand, save_path)

    def start_to_translate_all(self):
        """
        Starts the translation process for all files in the target directory.
        """
        # make directory for saving
        mkdir(".", self.params.save_dir)
        # get file path list that contains all target path
        tgt_file_path_ls = get_all_file_path_in(self.params.tgt_dir)

        # dir names list that contains already created test
        already_generated_ls = get_all_dir_names_in(self.params.save_dir)

        generating_ls = [
            p
            for p in tgt_file_path_ls
            if not get_file_name_without_ext(p) in already_generated_ls
        ]

        # start to one iter
        for i, tgt_path in enumerate(generating_ls):
            # target file extension check
            if (
                not get_file_extension(tgt_path)
                == SUPPORTED_EXT_DICT[self.params.src_lang]
            ):
                continue
            self.one_iter(tgt_path)
            logger.add_log(f"{i} {tgt_path}")


if __name__ == "__main__":
    # get parameters
    parser = get_parser()
    params = parser.parse_args()

    # check parameters
    assert os.path.isfile(
        params.model_path
    ), f"The path to the model checkpoint is incorrect: {params.model_path}"
    assert os.path.isfile(
        params.BPE_path
    ), f"The path to the BPE tokens is incorrect: {params.BPE_path}"
    assert (
        params.src_lang in SUPPORTED_LANGUAGES
    ), f"The source language should be in {SUPPORTED_LANGUAGES}."
    assert (
        params.tgt_lang in SUPPORTED_LANGUAGES
    ), f"The target language should be in {SUPPORTED_LANGUAGES}."
    # ## check save_dir is exist
    # assert (os.path.isdir(params.save_dir), f"{params.save_dir} is not a directory")
    # ## check tgt_dir is exist
    # assert (os.path.isdir(params.tgt_dir), f"{params.tgt_dir} is not a directory")

    # start UseTransCoder
    utc = UseTransCoder(params)
    utc.start_to_translate_all()
