# 2024/03/28
# auther:naru
# encoding=utf-8

import time

from Server.UdpServerSaveFile import UdpServerSaveFile
from CONST import (
    SERVER_HOST,
    PIDPPID_PORT,
    SYSCALL_BASEPORT,
    PORT_NUMBER,
    GUESTOS_PORT,
    PIDPPID_BUFSIZE,
    SYSCALL_BUFSIZE,
    GUESTOS_BUFSIZE,
    DEFAULT_SERVER_TIMEOUT,
    PIDPPID_SAVESIZE,
    SYSCALL_SAVESIZE,
    GUESTOS_SAVESIZE,
    SSH_USERNAME,
    SSH_HOST,
    SSH_KEY,
    SSH_PASSWORD,
    SSH_PORT,
    ZIP_FILES_PATH,
    LOG_PATH,
    AUTODA_TIMEOUT,
    GUEST_OS_ANALYSIS_PATH,
    GUEST_OS_PATH,
    GUEST_ZIPFILE_PATH,
)
from lib.multp import start_process
from lib.fs import get_all_file_path_in, get_file_name_without_ext, get_file_name
from lib.Logger import Logger
from lib.SSHOperator import SSHOperator


def main():
    # init servers
    syscall_server_ls = [
        UdpServerSaveFile(
            SERVER_HOST,
            SYSCALL_BASEPORT + i,
            SYSCALL_BUFSIZE,
            DEFAULT_SERVER_TIMEOUT,
            SYSCALL_SAVESIZE,
        )
        for i in range(PORT_NUMBER)
    ]
    guestos_server = UdpServerSaveFile(
        SERVER_HOST,
        GUESTOS_PORT,
        GUESTOS_BUFSIZE,
        DEFAULT_SERVER_TIMEOUT,
        GUESTOS_SAVESIZE,
    )
    pidppid_server = UdpServerSaveFile(
        SERVER_HOST,
        PIDPPID_PORT,
        PIDPPID_BUFSIZE,
        DEFAULT_SERVER_TIMEOUT,
        PIDPPID_SAVESIZE,
    )
    process_ls = [start_process(server.main) for server in syscall_server_ls]
    process_ls.append(start_process(guestos_server.main))
    process_ls.append(start_process(pidppid_server.main))

    # init logger
    lgr = Logger(LOG_PATH)

    # start iterations
    for count, zip_path in enumerate(get_all_file_path_in(ZIP_FILES_PATH)):
        zipname = get_file_name_without_ext(zip_path)
        lgr.add_log(f"start {count} {zipname}")

        # 1. serverに保存先変更を伝える
        for i, server in enumerate(syscall_server_ls):
            server.change_save_dir(f"./{zipname}/syscall{i}/")
        guestos_server.change_save_dir(f"./{zipname}/guestos/")
        pidppid_server.change_save_dir(f"./{zipname}/pidppid/")

        # 2. guest osのsct_debianにssh接続を確立
        flag = False
        stime = time.time()
        while not flag:
            if time.time() - stime > AUTODA_TIMEOUT:
                lgr.add_log("ssh init connection timeout")
                raise TimeoutError("time out for ssh connection")
            try:
                ssh = SSHOperator(
                    SSH_USERNAME, SSH_HOST, SSH_PASSWORD, SSH_KEY, SSH_PORT
                )
                flag = ssh.connect_ssh()
                time.sleep(5)
            except:
                lgr.add_log("ssh connection failed.")

        # 3. sshからzipファイルを送信
        try:
            ssh.execute(f"cd {GUEST_OS_PATH} && rm -rf {GUEST_OS_ANALYSIS_PATH}")
            ssh.execute(f"cd {GUEST_OS_PATH} && mkdir {GUEST_OS_ANALYSIS_PATH}")
            ssh.send_file(zip_path)
        except Exception as e:
            lgr.add_log("sending zip file failed")
            raise SendingZipFileError("sending zip file failed") from e

        # 4. zipファイルを解凍
        try:
            ssh.execute(f"cd {GUEST_ZIPFILE_PATH} && unzip {get_file_name(zip_path)}")
        except Exception as e:
            lgr.add_log("unzipping failed")
            raise UnzippingError("unzipping failed") from e

        # 5. executorを実行
        try:
            ssh.execute(f"cd {GUEST_OS_PATH} && python3 -u Executor.py")
            time.sleep(2)
        except Exception as e:
            lgr.add_log("Executor execution Error")
            raise ExecutorError from e

        # 6. sct_debianの再起動
        try:
            ssh.execute_sudo("reboot")
            ssh.exit()
        except Exception as e:
            lgr.add_log("Guest reboot Error")
            raise GuestRebootError from e

        time.sleep(5)
        # analyze processの呼び出し
        lgr.add_log(f"end {count} {zip_path}")


class SendingZipFileError(Exception):
    pass


class UnzippingError(Exception):
    pass


class ExecutorError(Exception):
    pass


class GuestRebootError(Exception):
    pass


if __name__ == "__main__":
    main()
