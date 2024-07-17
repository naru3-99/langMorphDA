# for AutoSclda
# hostのアドレス
SERVER_HOST = "192.168.56.1"
# プロセス生成に関わる、PIDとPPIDのペアを取得するポート
PIDPPID_PORT = 15001
# システムコールに関係する情報を取得する
# BASEPORT + (プロセッサID % 4)をPORTとして使用する
SYSCALL_BASEPORT = 15002
PORT_NUMBER = 16
## Guest OSの全自動システムからくる情報を取得する
GUESTOS_PORT = 14999
# パケットの大きさに関するバッファサイズ
# see sclda/linux_6.1_mod/include/net/sclda.h
PIDPPID_BUFSIZE = 80
SYSCALL_BUFSIZE = 1200
GUESTOS_BUFSIZE = 200
# パケットを何個単位で保存するか
PIDPPID_SAVESIZE = 100
SYSCALL_SAVESIZE = 1000
GUESTOS_SAVESIZE = 50
# sshするために必要な情報
SSH_USERNAME = "naru3"
SSH_HOST = "127.0.0.1"
SSH_PASSWORD = "1234567890"
SSH_KEY = None
SSH_PORT = 16763
# ゲストOSに関する情報
GUEST_OS_PATH = "~/workdir/sclda_guest/"
GUEST_OS_ANALYSIS_PATH = "analysis/"
GUEST_ZIPFILE_PATH = GUEST_OS_PATH + GUEST_OS_ANALYSIS_PATH
# サーバがタイムアウトするまでの秒数
DEFAULT_SERVER_TIMEOUT = 60
# 全自動システムをタイムアウトする秒数
AUTODA_TIMEOUT = 100
# zip file for host os
ZIP_FILES_PATH = "./zipfiles/"
# logを保存するパス
LOG_PATH = "./log.txt"
# serverを開始するまでのラグ
TIME_TO_WAIT_INIT = 0.3

# process_data.py
# 入力のパス
HANDSHAKE = "sclda\x00"
INPUT_DIR = "./input/"
INPUT_PID_DIR = f"{INPUT_DIR}PID/"
SYSCALL_INFO_PATH = "./syscall_info.csv"

# 出力するパス
OUTPUT_DIR = "./output/"
PID_OUTPUT_PATH = f"{OUTPUT_DIR}pid.csv"