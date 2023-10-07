# 2023/09/19
# auther:naru
# encoding=utf-8

from typing import Optional

from lib763.multp import start_process

from UDPServerSaveFile import UdpServerSaveFile
from CONST import (
    OUTPUT_PARENT_DIR,
    SYSCALL_OUTPUT_DIR,
    PIDTREE_OUTPUT_DIR,
    PIDNAME_OUTPUT_DIR,
    SCT_SERVER_HOST,
    SYSCALL_PORT,
    PIDTREE_PORT,
    PIDNAME_PORT,
    PIDNAME_BUFSIZE,
    PIDTREE_BUFSIZE,
    SYSCALL_BUFSIZE,
    PIDNAME_MSG_BUFSIZE,
    PIDTREE_MSG_BUFSIZE,
    SYSCALL_MSG_BUFSIZE,
)


def syscall_edit_func(recieved_str: str) -> Optional[str]:
    """
    Edits the received string for the syscall output.

    Args:
        recieved_str (str): The received string.

    Returns:
        Optional[str]: The edited string, or None if the string does not contain exactly one "\x05" character.
    """
    if sum([(lambda c: 1 if (c == "\x05") else 0)(c) for c in recieved_str]) != 1:
        return None
    return ",".join([d for d in recieved_str.split("\x05")])


def pidtree_edit_func(recieved_str: str) -> str:
    """
    Edits the received string for the pidtree output.

    Args:
        recieved_str (str): The received string.

    Returns:
        str: The edited string, or an empty string if the string does not contain exactly two "\x05" characters.
    """
    if sum([(lambda c: 1 if (c == "\x05") else 0)(c) for c in recieved_str]) != 2:
        return ""
    return ",".join([d for d in recieved_str.split("\x05")])


def pidname_edit_func(recieved_str: str) -> str:
    """
    Edits the received string for the pidname output.

    Args:
        recieved_str (str): The received string.

    Returns:
        str: The edited string.
    """
    return recieved_str


OUTPUT_DIR_LS = [SYSCALL_OUTPUT_DIR, PIDTREE_OUTPUT_DIR, PIDNAME_OUTPUT_DIR]
PORT_LS = [SYSCALL_PORT, PIDTREE_PORT, PIDNAME_PORT]
BUFSIZE_LS = [SYSCALL_BUFSIZE, PIDTREE_BUFSIZE, PIDNAME_BUFSIZE]
FUNC_LS = [syscall_edit_func, pidtree_edit_func, pidname_edit_func]
MSGS_BUF_LS = [SYSCALL_MSG_BUFSIZE, PIDTREE_MSG_BUFSIZE, PIDNAME_MSG_BUFSIZE]


class SctServer:
    def __init__(self) -> None:
        """
        Initializes the SctServer class.

        Returns:
            None.
        """
        self.server_ls = [
            UdpServerSaveFile(SCT_SERVER_HOST, port, buf, func, msgbuf)
            for port, buf, func, msgbuf in zip(
                PORT_LS, BUFSIZE_LS, FUNC_LS, MSGS_BUF_LS
            )
        ]
        # start all server process
        self.process_ls = [start_process(server.main) for server in self.server_ls]

    def one_iter(self, save_file_name: str) -> None:
        """
        Initializes the save file for each server.

        Args:
            save_file_name (str): The name of the save file.
            event_ls (list): A list of Event objects.

        Returns:
            None.
        """
        save_path_ls = [
            f"{OUTPUT_PARENT_DIR}{outdir}{save_file_name}" for outdir in OUTPUT_DIR_LS
        ]
        for path, server in zip(save_path_ls, self.server_ls):
            # server:UdpServerSaveFile
            server.change_save_path(path)

    def fin_one_iter(self):
        for server in self.server_ls:
            server.set_iter_fin()
