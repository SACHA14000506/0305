import os
import sys
from pathlib import Path
path = Path(__file__)
root_path = path.parent.absolute().parent
sys.path.append(str(root_path))
sys.path.append(str(root_path / 'src'))
print(root_path)

from src.settings import para
import pandas as pd
import time
from src.parser import args
import src.test1 as test1

# 删除指定目录下的所有.smt2文件
def delete_cases(path):
    if os.path.exists(path):  # 检查路径是否存在
        for fpath, _, file_list in os.walk(path):  # 遍历目录
            for fname in file_list:
                if fname.endswith('.smt2'):  # 查找以.smt2结尾的文件
                    os.remove(os.path.join(fpath, fname))  # 删除该文件
        print('已删除文件: ', path)  # 打印删除提示


# 主函数，协调程序的各个部分
def main():
    parameter = para()  # 从settings获取参数对象

    # 使用命令行参数来设置参数
    parameter.type = args.type
    parameter.solvers = args.solvers

    print("设置的求解器:", parameter.type)  # 打印调试信息
    print('求解器列表长度:', len(parameter.solvers))  # 打印求解器列表的长度
    print('求解器列表内容:', parameter.solvers)  # 打印求解器列表内容
    parameter.root_path = root_path  # 设置根路径到参数对象
    parameter.timeout = args.timeout  # 从命令行参数获取超时时间
    parameter.time0 = time.time()  # 记录当前时间，作为起始时间

    # 删除'results/Regression_cases'目录中的回归测试案例
    delete_cases(str(parameter.root_path / 'results' / 'Regression_cases'))

    # 实例化fuzzer并运行
    finder = test1.Fuzzer(parameter)
    finder.run()

if __name__ == '__main__':
    print("当前工作目录: ", os.getcwd())  # 打印当前工作目录
    df = pd.DataFrame(columns=['time', 'case_number'])  # 包含时间和案例数量的统计
    df.to_csv('./results/Statistics/Total_number.csv')  # 保存为CSV文件
    df1 = pd.DataFrame(columns=['case', 'solver1', 'solver2', 'solver3', 'var_num',
                                'assert_num', 'nax_str_len', 'max_depth'])  # 详细统计数据
    df1.to_csv('./results/Statistics/Results_for_cases.csv')  # 保存为CSV文件
    df1.to_csv('./Results.csv', mode='a', header=True)

    main()  # 执行主函数
