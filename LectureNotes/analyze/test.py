from lib763.fs import *

id_name_dict = {}
for row in load_str_from_file("./syscall_info.csv").split("\n"):
    splited_row = row.split(",")
    if len(splited_row) == 0:
        continue
    id_name_dict[splited_row[1]] = splited_row[0]

def count_syscall_num_1file(path):
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
    return cnt

def main():
    # 2のほうが前処理していないほう
    numpy_init = []
    func_exec = []
    for i,dirpath in enumerate(get_all_dir_names_in('./important_proc2/')):
        if i == 200:
            break
        index_ls = [0,0,0,0]
        offset = 0
        numpy_flag= False
        exec_flag = False
        for j,row in enumerate(load_str_from_file(f'./important_proc2/{dirpath}/{dirpath}.csv').split('\n')):
            tsr = row.split('\t')
            if (len(tsr) < 4):
                offset +=1
                continue
            if (tsr[1] == "1-write" and tsr[3] == "1"):
                if ("start to initialize numpy" in tsr[-1]):
                    numpy_flag = True
                    index_ls[0] += j-offset
                elif("finished to initialize numpy" in tsr[-1]):
                    numpy_flag = False
                    index_ls[1] += j-offset
                elif ("start to execute" in tsr[-1]):
                    exec_flag = True
                    index_ls[2] += j-offset
                elif("finished to execute" in tsr[-1]):
                    exec_flag = False
                    index_ls[3] += j-offset
            if (tsr[1] == "435-clone3"):
                if numpy_flag:
                    index_ls[1] +=count_syscall_num_1file(f'./important_proc2/{dirpath}/{tsr[2]}.csv')
                elif exec_flag:
                    index_ls[3] +=count_syscall_num_1file(f'./important_proc2/{dirpath}/{tsr[2]}.csv')
        numpy_init.append(index_ls[1]-index_ls[0]-1)
        func_exec.append(index_ls[3]-index_ls[2]-1)
    print(f'numpy min:{min(numpy_init)} avg:{sum(numpy_init)/200} max{max(numpy_init)}')
    print(f'func min:{min(func_exec)} avg:{sum(func_exec)/200} max{max(func_exec)}')

if __name__ == '__main__':
    main()
