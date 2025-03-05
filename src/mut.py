import ollama
import time
import subprocess

# 调用 Ollama 使用大语言模型生成 SMT2 文件内容
def generate_smt2_content(prompt):
    response = ollama.generate(
        model="deepseek-r1:32b",  # 使用的模型名称
        prompt=prompt
    )
    # 提取生成的文本内容
    if hasattr(response, 'response'):
        return response.response
    else:
        raise ValueError("Unexpected response format")

def save_to_smt2_file(content, file_path):
    # 提取从 ```smt2 到 ``` 之间的内容，不包括这两行
    start_marker = "```smt2"
    end_marker = "```"

    start_index = content.find(start_marker)
    end_index = content.find(end_marker, start_index + len(start_marker))

    if start_index != -1 and end_index != -1:
        # 提取内容时排除标记行
        final_content = content[start_index + len(start_marker):end_index].strip()
    else:
        raise ValueError("The content does not contain the expected markers.")

    with open(file_path, 'w') as file:
        file.write(final_content)

def run_z3(file_path):
    # 运行 Z3 并捕获输出
    result = subprocess.run(['z3', file_path], capture_output=True, text=True)
    return result.stdout

def mutate_smt2_v2(original_smt2):
    prompt = (
        f"This is my initial SMT2 content: {original_smt2}. "
        "Modify the original SMT2 content "
        "Ensure the logic type remains QF_S and the file should have around 25 lines. "
        "Only include the SMT2 content without any explanatory language."
    )

    smt2_file_path = 'temp000.smt2'
    error_detected = True
    start = time.time()

    while error_detected:
        smt2_content = generate_smt2_content(prompt)
        # 保存生成的内容到 SMT2 文件
        save_to_smt2_file(smt2_content, smt2_file_path)
        # print(smt2_content)

        # 运行 Z3 并检查输出
        z3_output = run_z3(smt2_file_path)

        # print(f"Z3 Output: {z3_output}")

        # 检查输出中是否有错误
        if 'error' in z3_output.lower():
            print("Error detected in SMT2 file. Regenerating...")
            # 将错误信息添加到提示中以生成新的 SMT2 内容
            prompt = (
                f"The following SMT2 content produced an error: {z3_output}. "
                f"Original SMT2 content: {original_smt2}. "
                "The logic type should be QF_S. The file should have around 25 lines. "
                "Modify the content to fix the error. Only include the SMT2 content without any explanatory language."
            )
        else:
            error_detected = False
            # print(f"SMT2 file generated and saved to {smt2_file_path}")

    end = time.time()
    print(f"deepseek_chat 此次调用花费时间为：{(end-start):.4f}秒")
    print("z3_output: ", z3_output)
    return smt2_content

# 对SMT-LIB 2文件进行突变并生成新的内容
def generate_mutated_smt2_v2(original_smt2):
    mutated_smt2 = mutate_smt2_v2(original_smt2)
    print(mutated_smt2)
    return mutated_smt2

def main():
    # 读取示例的 SMT2 文件
    with open("example.smt2", "r") as file:
        original_smt2 = file.read()

    # 生成变异后的 SMT2 文件
    generate_mutated_smt2_v2(original_smt2)

if __name__ == "__main__":
    main()
