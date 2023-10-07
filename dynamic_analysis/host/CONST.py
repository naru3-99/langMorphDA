# 2023/09/19
# auther:naru
# encoding=utf-8

# Auto dynamic analysis configuration

## server configuration
SCT_SERVER_HOST = "192.168.56.1"
SYSCALL_PORT = 15001
PIDTREE_PORT = 15002
PIDNAME_PORT = 15003
# udpサーバのバッファサイズ
SYSCALL_BUFSIZE = 32
PIDTREE_BUFSIZE = 64
PIDNAME_BUFSIZE = 1024
# メッセージをバッファする量
# この量がたまると保存プロセスが保存を行う
SYSCALL_MSG_BUFSIZE = 5000
PIDTREE_MSG_BUFSIZE = 50
PIDNAME_MSG_BUFSIZE = 10

## SSH configuraion
SSH_USER = "naru3"
SSH_HOST = "127.0.0.1"
SSH_PASSWORD = "1234567890"
SSH_KEY = None
SSH_PORT = 16763

## path for zip files to be analyzed
ZIP_FILES_PATH = "../../da_data/da_zipfiles"

## path for output files
OUTPUT_PARENT_DIR = "../../da_data/"
SYSCALL_OUTPUT_DIR = "syscall/"
PIDTREE_OUTPUT_DIR = "pidtree/"
PIDNAME_OUTPUT_DIR = "pid_name/"
SUMMARY_OUTPUT_DIR = "summary/"
SUMMARY2_OUTPUT_DIR = "summary2/"

## path for log files
LOG_PATH = "../../da_data/da.log"

# guest os directry
GUEST_OS_PATH = "/home/naru3/workdir/langMorphDA/dynamic_analysis/guest/"
GUEST_OS_ANALYSIS_PATH = "analysis/"

# ipc commands must be int
SAVE_FINISH_COMMAND = 1
ITER_FINISH_COMMAND = 2
SERVER_READY_COMMAND = 3
