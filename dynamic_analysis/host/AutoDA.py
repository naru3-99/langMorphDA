
# 2023/06/21
# auther:naru
# encoding=utf-8
"""
このコードを実行するための初期状態:
virtual boxのsct_debianが起動していること
ssh -p 16763 naru3@localhost
"""

import os
import time
from typing import Optional

from lib763.SSHOperator import SSHOperator
from lib763.fs import get_all_file_path_in, get_file_name, rmrf
from lib763.Logger import Logger
from lib763.multp import start_process

from SctServer import SctServer
from analyze import analyze_ignore_pid
from CONST import (
    SSH_USER,
    SSH_HOST,
    SSH_PASSWORD,
    SSH_KEY,
    SSH_PORT,
    ZIP_FILES_PATH,
    OUTPUT_PARENT_DIR,
    PIDTREE_OUTPUT_DIR,
    PIDNAME_OUTPUT_DIR,
    SYSCALL_OUTPUT_DIR,
    SUMMARY_OUTPUT_DIR,
    LOG_PATH,
    GUEST_OS_PATH,
    GUEST_OS_ANALYSIS_PATH,
    SAVE_FINISH_COMMAND,
    SERVER_READY_COMMAND,
)

GUEST_ZIPFILE_PATH = GUEST_OS_PATH + GUEST_OS_ANALYSIS_PATH


class AutoDA:
    def __init__(self) -> None:
        self._ssh: Optional[SSHOperator] = None
        self.count = None
        self.sct_server = SctServer()
        self.logger = Logger(LOG_PATH)

    def _one_iter(self, zip_path: str) -> None:
        self.logger.add_log(f"start {self.count} {zip_path}")
        # 1. host osのサーバ立ち上げ
        self.sct_server.one_iter(f"{self.count}.csv")
        for server in self.sct_server.server_ls:
            server.eventh.wait(SERVER_READY_COMMAND)
            server.clear_server_ready()

        # 2. guest osのsct_debianにssh接続を確立
        self.ssh_connect()
        time.sleep(5)

        # 3. sshからzipファイルを送信
        self.ssh_execute(f"cd {GUEST_OS_PATH} && rm -rf {GUEST_OS_ANALYSIS_PATH}")
        self.ssh_execute(f"cd {GUEST_OS_PATH} && mkdir {GUEST_OS_ANALYSIS_PATH}")
        self.ssh_sendfile(zip_path)

        # 4. zipファイルを解凍
        self.ssh_execute(f"cd {GUEST_ZIPFILE_PATH} && unzip {get_file_name(zip_path)}")

        # 5. executorを実行
        self.ssh_execute(f"cd {GUEST_OS_PATH} && python3 -u Executor.py")
        time.sleep(2)

        # 6. sct_debianの再起動
        self._ssh.execute_sudo("reboot")
        self.ssh_disconnect()

        # 少し待ってから，終了処理を行う
        time.sleep(5)
        self.sct_server.fin_one_iter()

        # analyze processの呼び出し
        for server in self.sct_server.server_ls:
            server.eventh.wait(SAVE_FINISH_COMMAND)
            server.clear_save_fin()
        start_process(analyze_proc, self.count)

        # 終了ログ
        self.logger.add_log(f"end {self.count} {zip_path}")

    def main(self) -> None:
        for zip_path in get_all_file_path_in(ZIP_FILES_PATH):
            try:
                # check the log
                self.count = self.check_log(zip_path)
                if self.count == -1:
                    continue
                # start to da(one iter)
                print(zip_path)
                self._one_iter(zip_path)
            except:
                self._ssh.execute_sudo("reboot")

    def check_log(self, zip_path: str) -> int:
        # if log file does not exist, return 0
        if not os.path.exists(LOG_PATH):
            return 0

        # if zip file is already analyzed, return -1
        log_row_ls = self.logger.get_log().split("\n")
        end_row_ls = [row for row in log_row_ls if "end" in row]
        end_zip_path_ls = [row.split(" ")[2] for row in end_row_ls]
        if zip_path in end_zip_path_ls:
            return -1

        # if zip file is not analyzed, return the next save number
        start_zip_path_ls = [row.split(" ")[2] for row in log_row_ls if "start" in row]
        if zip_path not in start_zip_path_ls:
            return max([int(row.split(" ")[1]) for row in end_row_ls]) + 1

        # if zip file is already started but not finished, remove log and analysis data
        if zip_path in start_zip_path_ls and not zip_path in end_zip_path_ls:
            remove_row = [row for row in log_row_ls if zip_path in row][0]
            self.logger.pop_logs_row(remove_row)
            remove_file = remove_row.split(" ")[1]
            rmrf(f"{OUTPUT_PARENT_DIR}{PIDTREE_OUTPUT_DIR}{remove_file}.csv")
            rmrf(f"{OUTPUT_PARENT_DIR}{PIDNAME_OUTPUT_DIR}{remove_file}.csv")
            rmrf(f"{OUTPUT_PARENT_DIR}{SYSCALL_OUTPUT_DIR}{remove_file}.csv")
            if os.path.exists(f"{OUTPUT_PARENT_DIR}{SUMMARY_OUTPUT_DIR}{remove_file}/"):
                rmrf(f"{OUTPUT_PARENT_DIR}{SUMMARY_OUTPUT_DIR}{remove_file}/")
            # return the next save number
            return int(remove_row.split(" ")[1])

    def ssh_connect(self) -> None:
        if self._ssh is None:
            self._ssh = SSHOperator(
                SSH_USER, SSH_HOST, SSH_PASSWORD, key_path=SSH_KEY, port=SSH_PORT
            )
        while not self._ssh.connect_ssh():
            time.sleep(5)

    def ssh_disconnect(self):
        self._ssh.exit()

    def ssh_execute(self, command: str) -> None:
        try:
            self._ssh.execute(command)
        except:
            pass

    def ssh_sendfile(self, zip_path):
        return self._ssh.send_file(zip_path, GUEST_ZIPFILE_PATH)


# 取得したデータをanalyzeするプロセス
def analyze_proc(num: int) -> None:
    analyze_ignore_pid(str(num))


if __name__ == "__main__":
    AutoDA().main()
