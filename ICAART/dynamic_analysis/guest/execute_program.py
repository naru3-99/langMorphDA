import os
import subprocess

from lib763.fs import change_file_encoding, load_str_from_file

from correct_java import correct_java_class_name
from CONST import (
    DEFAULT_TIMEOUT,
    COMPILE_TIMEOUT,
    COMMANDLINE_ARGUMENT_FILE,
    STANDARD_IO_FILE,
)


def execute_python_file(
    current_dir: str,
    python_filename: str,
    input_filename: str,
) -> tuple[int, int, str, str]:
    change_file_encoding(os.path.join(current_dir, python_filename), "utf-8")
    proc = subprocess.Popen(
        f"python3 {python_filename} $(cat {COMMANDLINE_ARGUMENT_FILE})",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        cwd=current_dir,
    )
    pid = proc.pid
    try:
        out, err = proc.communicate(
            load_str_from_file(os.path.join(current_dir, STANDARD_IO_FILE)).encode(),
            timeout=DEFAULT_TIMEOUT,
        )
        exitcode = proc.returncode
    except subprocess.TimeoutExpired:
        return (None, None, None, None)
    return (exitcode, pid, out.decode(), err.decode())


def execute_java_file(
    current_dir: str,
    java_filename: str,
    input_filename: str,
) -> tuple[int, int, str, str]:
    java_file_path = os.path.join(current_dir, java_filename)
    change_file_encoding(java_file_path, "utf-8")
    if not correct_java_class_name(java_file_path):
        return (None, None, None, None)
    java_class_name = java_filename.split(".")[0]

    compile_proc = subprocess.Popen(
        f"javac -encoding UTF-8 {java_class_name}.java",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        cwd=current_dir,
    )
    compile_proc.wait(COMPILE_TIMEOUT)
    if compile_proc.returncode != 0:
        return (None, None, None, None)

    exec_proc = subprocess.Popen(
        f"java {java_class_name} $(cat {COMMANDLINE_ARGUMENT_FILE})",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        cwd=current_dir,
    )
    pid = exec_proc.pid
    try:
        out, err = exec_proc.communicate(
            load_str_from_file(os.path.join(current_dir, STANDARD_IO_FILE)).encode(),
            timeout=DEFAULT_TIMEOUT,
        )
        exitcode = exec_proc.returncode
    except subprocess.TimeoutExpired:
        return (None, None, None, None)
    return (exitcode, pid, out.decode(), err.decode())
