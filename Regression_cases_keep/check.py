import os
import time
import subprocess

# 配置信息
base_path = "/home/cass/Webstorm_project/0226"  # Z3 所在的基路径
versions = ["z3-4.8.7", "z3-4.8.8", "z3-4.8.9"]  # Z3 的版本列表
op = 'smt.string_solver=' + 'z3str3'  # 运行时的选项
output_file = "0checkout.csv"  # 输出文件名

# 获取当前目录下的所有 .smt2 文件
smt_files = [f for f in os.listdir('.') if f.endswith('.smt2')]

# 初始化结果列表
results = {}

# 遍历每个 .smt2 文件
for file_name in smt_files:
    results[file_name] = []  # 初始化空列表存储该文件在各版本下的测试结果
    # 遍历每个 Z3 版本
    for version in versions:
        solver_path = os.path.join(base_path, version, "bin", "z3")  # Z3 的路径
        # 构造命令
        cmd = [
            "timeout", "20",  # 设置超时时间为 20 秒
            "bash", "-c",
            f"'{solver_path}' {op} \"{file_name}\""
        ]

        # 记录运行时间
        start_time = time.time()

        # 执行命令
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=False
            )
        except subprocess.TimeoutExpired:
            end_time = time.time()
            runtime = end_time - start_time
            exit_code = 124  # 超时退出码
            results[file_name].append([runtime, exit_code])
            continue

        end_time = time.time()
        runtime = end_time - start_time
        exit_code = result.returncode

        results[file_name].append([runtime, exit_code])

# 将结果写入文件
with open(output_file, "w") as f:
    # 写入表头
    f.write("File Name | " + " | ".join([f"{version} (s/e)" for version in versions]) + "\n")
    f.write("-" * 80 + "\n")  # 分隔线
    
    # 写入数据
    for file_name in results:
        line = f"{file_name} | "
        # 遍历每个版本的结果
        for i, version in enumerate(versions):
            runtime, exit_code = results[file_name][i]
            line += f"{version} ({runtime:.2f}/{exit_code}) | "  # 格式化输出
        line = line.rstrip(" | ")  # 去除末尾多余的 |
        f.write(line + "\n")

print(f"测试结果已保存到文件: {output_file}")
