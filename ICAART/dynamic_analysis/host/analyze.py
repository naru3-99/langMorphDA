# 2023/09/19
# auther:naru
# encoding=utf-8

import os

from lib763.fs import (
    save_str_to_file,
    load_str_from_file,
    mkdir,
    ensure_path_exists,
    get_file_extension,
    get_file_name_without_ext,
    get_all_file_path_in,
)
from lib763.Logger import Logger
from lib763.multp import parallel_process

from CONST import (
    OUTPUT_PARENT_DIR,
    SYSCALL_OUTPUT_DIR,
    PIDTREE_OUTPUT_DIR,
    PIDNAME_OUTPUT_DIR,
    SUMMARY_OUTPUT_DIR,
    SUMMARY2_OUTPUT_DIR,
    LOG_PATH,
)

PID_PPID_DATA_PATH = os.path.join(OUTPUT_PARENT_DIR, PIDTREE_OUTPUT_DIR)
SYSCALL_PID_DATA_PATH = os.path.join(OUTPUT_PARENT_DIR, SYSCALL_OUTPUT_DIR)
TARGET_PID_DATA_PATH = os.path.join(OUTPUT_PARENT_DIR, PIDNAME_OUTPUT_DIR)
SUMMARY_OUTPUT_PATH = os.path.join(OUTPUT_PARENT_DIR, SUMMARY_OUTPUT_DIR)
SUMMARY2_OUTPUT_PATH = os.path.join(OUTPUT_PARENT_DIR, SUMMARY2_OUTPUT_DIR)
logger = Logger(LOG_PATH)


# pidごとに呼び出されたシステムコールを取得する
# 最終的なアウトプットはpidの数と一致する(複数になる可能性がある)
def analyze(num: str) -> None:
    """Analyze the system call IDs of programs with an exit code of 0.

    Args:
        num (str): The execution number of the analysis target. Creates a summary of {PID_PPID_DATA_PATH}/{num}.csv.
    """
    ensure_path_exists(SUMMARY_OUTPUT_PATH + "/")
    mkdir(SUMMARY_OUTPUT_PATH, num)

    # Extract only pid and PPID from rows containing pid,ppid,comm
    pid_ppid_comm_ls = [
        row.split(",")
        for row in load_str_from_file(f"{PID_PPID_DATA_PATH}/{num}.csv").split("\n")
        if (len(row) != 0)
    ]
    pid_ppid_ls = [[pid, ppid] for pid, ppid, comm in pid_ppid_comm_ls]

    # List of syscall id and Pid
    scid_pid_ls = [
        row.split(",")
        for row in load_str_from_file(f"{SYSCALL_PID_DATA_PATH}/{num}.csv").split("\n")
        if (len(row) != 0)
    ]

    # List of pid and exit code
    # One row is like pid=1000,name=sample.java,retcode=0
    # Extract pid and file name where retcode=0.
    target_pid_fname_ls = [
        [row.split(",")[0].split("=")[1], row.split(",")[1].split("=")[1]]
        for row in load_str_from_file(f"{TARGET_PID_DATA_PATH}/{num}.csv").split("\n")
        if (len(row) != 0 and row.split(",")[2].split("=")[1] == "0")
    ]

    # dict[pid] = comm
    pid_comm_dict = {}
    for pid, ppid, comm in pid_ppid_comm_ls:
        pid_comm_dict[pid] = comm

    # Create a summary
    # The summary saves the system call sequence for each pid in the folder of the file name
    for targ_pid, fname in target_pid_fname_ls:
        # target_lang = "python3" if "py" in fname else "java"
        target_lang = "python3" if get_file_extension(fname) == ".py" else "java"
        mkdir(f"{SUMMARY_OUTPUT_PATH}/{num}", fname)
        for pid in [
            pid
            for pid in find_descendant_processes(pid_ppid_ls, targ_pid)
            if pid_comm_dict[pid] == target_lang
        ]:
            save_str_to_file(
                ",".join(find_syscalls_by_pid(scid_pid_ls, pid)),
                f"{SUMMARY_OUTPUT_PATH}/{num}/{fname}/{pid}.csv",
            )
    logger.add_log(f"Analyzed {num}")


def find_descendant_processes(pid_ppid_ls, parent_pid):
    """Find all descendant PIDs of a given parent PID.

    Args:
        pid_ppid_ls: A list of lists, where each list contains a PID and its parent PID.
        parent_pid: The PID of the parent process.

    Returns:
        A list of PIDs that are descendants of the parent PID.
    """
    descendant_pids = [parent_pid]

    for pid_pair in pid_ppid_ls:
        if pid_pair[1] == parent_pid:
            descendant_pids.append(pid_pair[0])
            descendant_pids.extend(find_descendant_processes(pid_ppid_ls, pid_pair[0]))

    return descendant_pids


def find_syscalls_by_pid(scid_pid_ls, pid):
    """Find all syscall IDs invoked by a given PID.

    Args:
        scid_pid_ls: A list of lists, where each list contains a syscall ID and the PID thatmade the syscall.
        pid: The PID of the process.

    Returns:
        A list of syscall IDs that were made by the PID.
    """
    syscall_ids = []

    for syscall_pair in scid_pid_ls:
        if syscall_pair[1] == pid:
            syscall_ids.append(syscall_pair[0])

    return syscall_ids


# pidごとではなく、関係があるpidのシステムコールを時系列順に取得する
# 最終的なアウトプットは1ファイルになる
def analyze_ignore_pid(num: str) -> None:
    """Analyze the system call IDs of programs with an exit code of 0.
    Batch processing instead of separating by pid.

    Args:
        num (str): The execution number of the analysis target. Creates a summary of {PID_PPID_DATA_PATH}/{num}.csv.
    """
    ensure_path_exists(SUMMARY2_OUTPUT_PATH + "/")
    mkdir(SUMMARY2_OUTPUT_PATH, num)

    # Extract only pid and PPID from rows containing pid,ppid,comm
    pid_ppid_comm_ls = [
        row.split(",")
        for row in load_str_from_file(f"{PID_PPID_DATA_PATH}/{num}.csv").split("\n")
        if (len(row) != 0)
    ]
    pid_ppid_ls = [[pid, ppid] for pid, ppid, comm in pid_ppid_comm_ls]

    # List of syscall id and Pid
    scid_pid_ls = [
        row.split(",")
        for row in load_str_from_file(f"{SYSCALL_PID_DATA_PATH}/{num}.csv").split("\n")
        if (len(row) != 0)
    ]

    # List of pid and exit code
    # One row is like pid=1000,name=sample.java,retcode=0
    # Extract pid and file name where retcode=0.
    target_pid_fname_ls = [
        [row.split(",")[0].split("=")[1], row.split(",")[1].split("=")[1]]
        for row in load_str_from_file(f"{TARGET_PID_DATA_PATH}/{num}.csv").split("\n")
        if (len(row) != 0 and row.split(",")[2].split("=")[1] == "0")
    ]

    # dict[pid] = comm
    pid_comm_dict = {}
    for pid, ppid, comm in pid_ppid_comm_ls:
        pid_comm_dict[pid] = comm

    # Create a summary
    # The summary saves the system call sequence
    for targ_pid, fname in target_pid_fname_ls:
        target_lang = "python3" if get_file_extension(fname) == ".py" else "java"
        pid_ls = [
            pid
            for pid in find_descendant_processes(pid_ppid_ls, targ_pid)
            if pid_comm_dict[pid] == target_lang
        ]
        scid_ls = find_syscalls_ignore_pid(scid_pid_ls, pid_ls)
        save_fname = fname.replace(".", "_") + ".csv"
        save_str_to_file(
            ",".join(scid_ls), f"{SUMMARY2_OUTPUT_PATH}/{num}/{save_fname}"
        )
    logger.add_log(f"Analyzed_ignore {num}")


def find_syscalls_ignore_pid(scid_pid_ls, pid_ls):
    """Find all syscall IDs invoked by a given PID.

    Args:
        scid_pid_ls: A list of lists, where each list contains a syscall ID and the PID thatmade the syscall.
        pid_ls: The list of PIDs where i want to find.

    Returns:
        A list of syscall IDs that were made by the PID.
    """
    syscall_ids = []

    for scid, pid in scid_pid_ls:
        if pid in pid_ls:
            syscall_ids.append(scid)
    return syscall_ids


if __name__ == "__main__":
    parallel_process(
        analyze_ignore_pid,
        [
            get_file_name_without_ext(i)
            for i in get_all_file_path_in(SYSCALL_PID_DATA_PATH)
        ],
    )
