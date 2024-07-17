from lib763.fs import *
from CONST import *


id_name_dict = {}
for row in load_str_from_file("./syscall_info.csv").split("\n"):
    splited_row = row.split(",")
    if len(splited_row) == 0:
        continue
    id_name_dict[splited_row[1]] = splited_row[0]

def process_pid():
    # 新しいPID情報のリストを作成
    new_info_ls = []
    for filepath in get_all_file_path_in('./inpaut/PID/'):
        for msg in load_object_from_file(filepath):
            row = "\t".join([s.decode("ISO-8859-1", errors="replace") for s in msg.split(b"\x05")])
            new_info_ls.append(row)
    if HANDSHAKE in new_info_ls:
        new_info_ls.remove(HANDSHAKE)

    # 新しいPID情報を統合し、保存する
    tab_splited_pidls = [
        info.split("\t") for info in new_info_ls if (len(info) != 0)
    ]
    if len(tab_splited_pidls) == 0:
        return
    sorted_pid_ls = [
        "\t".join(row) for row in sorted(tab_splited_pidls, key=lambda x: int(x[0]))
    ]
    save_str_to_file("\n".join(sorted_pid_ls), PID_OUTPUT_PATH)

def process_syscall_last():
    # 新しいパケットを読み込む
    rmrf('./output')
    ensure_path_exists("./output/")
    pid__clock_scid__dict = {}
    for path in get_all_file_path_in('./input/'):
        if "PID" in path:
            continue
        for msg in load_object_from_file(path):
            temp_ls = [
                s.decode("latin-1", errors="replace") for s in msg.split(b"\x05")
            ]
            # pid,clock,scid,retval,...なはずなので、
            # 2未満の長さならパケット破棄
            if len(temp_ls) <= 2:
                continue
            pid = temp_ls[0]
            clock = temp_ls[1]
            if temp_ls[2] in id_name_dict.keys():
                scname = f"{temp_ls[2]}-{id_name_dict[temp_ls[2]]}"
            else:
                continue
            other = "\t".join(temp_ls[3:]).replace("\n", "\\n")

            if not (pid in pid__clock_scid__dict.keys()):
                pid__clock_scid__dict[pid] = {}
            if not (clock in pid__clock_scid__dict[pid].keys()):
                pid__clock_scid__dict[pid][clock] = ""
            pid__clock_scid__dict[pid][clock] += scname + "\t" + other

    for pid in pid__clock_scid__dict.keys():
        save_file_path = f"./output/{pid}.csv"

        clock_msg_ls = [
            [int(clock), msg] for clock, msg in pid__clock_scid__dict[pid].items()
        ]
        sorted_clock_msg_ls = sorted(clock_msg_ls, key=lambda x: x[0])
        min_clock = sorted_clock_msg_ls[0][0]

        save_row_ls = []
        for clock, msg in sorted_clock_msg_ls:
            save_row_ls.append(f"{clock-min_clock}\t{msg}")
        if is_exists(save_file_path):
            append_str_to_file("\n".join(save_row_ls), save_file_path)
        else:
            save_str_to_file("\n".join(save_row_ls), save_file_path)

def preprocess():
    rmrf('./prep')
    ensure_path_exists('./prep/')
    for path in get_all_file_path_in('./output/'):
        save_row_ls = []
        for row in load_str_from_file(path).split('\n'):
            for id,name in id_name_dict.items():
                if f'{id}-{name}' in row:
                    try:
                        retval = int(row.split('\t')[2])
                        if(retval>=0):
                            save_row_ls.append(row)
                    except:
                        pass
        if(len(save_row_ls) > 0):
            save_str_to_file('\n'.join(save_row_ls),f'./prep/{get_file_name(path)}')

def get_important_process(target_keyword_ls):
    # execveの引数にtarget_keywordが存在するもの
    # そのプロセスの子プロセスを分けて取得
    # if (tsp[1] == "56-clone" or tsp[1] == "57-fork" or tsp[1] == "58-vfork")
    cp_syscall_ls = ["56-clone" ,"57-fork","58-vfork","435-clone3"]
    for path in get_all_file_path_in('./prep/'):
        target_path_ls = []
        target_name = ""
        contents_str  = load_str_from_file(path)
        if not ("59-execve" in contents_str):
            continue
        flag = True
        for tkw in target_keyword_ls:
            if not (tkw in contents_str):
                flag = False
                break
        if (flag):
            # ターゲットのプロセス
            target_name = get_file_name_without_ext(path)
            target_path_ls.append(path)
            for row in contents_str.split('\n'):
                tsp = row.split('\t')
                if (tsp[1] in cp_syscall_ls):
                    target_path_ls.append(f'./prep/{tsp[2]}.csv')
            ensure_path_exists(f"./important_proc/{target_name}/")
            for tpath in target_path_ls:
                save_str_to_file(load_str_from_file(tpath),f'./important_proc/{target_name}/{get_file_name(tpath)}')




def count_syscall_num_1file(out_dir,target_dir):
    ensure_path_exists(out_dir)
    for path in get_all_file_path_in(target_dir):
        cnt =0
        id_count_dict = {}
        for id in id_name_dict.keys():
            id_count_dict[id] = 0

        for row in load_str_from_file(path).split('\n'):
            for id,name in id_name_dict.items():
                if f'{id}-{name}' in row:
                    id_count_dict[id]+=1
                    cnt +=1
                    break
        print(cnt)
        save_row_ls =[f'all:{cnt}']+ [f'{id},{name},{id_count_dict[id]}' for id,name in id_name_dict.items()]
        save_str_to_file('\n'.join(save_row_ls),f'{out_dir}{get_file_name(path)}')

def count_syscall_num_all(out_dir,target_dir,save_fname):
    id_count_dict = {}
    cnt = 0
    for id in id_name_dict.keys():
        id_count_dict[id] = 0
    ensure_path_exists(out_dir)

    for path in get_all_file_path_in(target_dir):
        for row in load_str_from_file(path).split('\n'):
            for id,name in id_name_dict.items():
                if f'{id}-{name}' in row:
                    id_count_dict[id]+=1
                    cnt +=1
                    break
    save_row_ls =[f'NaN,ALL,{cnt}']+ [f'{id},{name},{id_count_dict[id]}' for id,name in id_name_dict.items()]
    save_str_to_file('\n'.join(save_row_ls),f'{out_dir}{save_fname}')


if __name__ == '__main__':
    process_syscall_last()
    process_pid()
    preprocess()
    get_important_process(['python3','import_numpy_only.py'])
    for path in get_all_dir_path_in('./important_proc/'):
        count_syscall_num_all('./prepi_count/',path,path.split('/')[-2])
