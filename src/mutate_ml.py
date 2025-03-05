import os
import time
import re
import string
import subprocess
from mistralai import Mistral
from form import form1, form2, form3, form4, form5, form6, form7, form8, form9, form10, form11
import random
# 将所有 form 放入一个列表
forms = [form1, form2, form3, form4, form5, form6, form7, form8, form9, form10, form11]

# 随机选择三个 form
selected_forms = random.sample(forms, 1)


# Initialize the Mistral client with your API key
api_key = os.environ.get("MISTRAL_API_KEY")

model = "mistral-large-latest"
client = Mistral(api_key=api_key)

# 调用 Mistral 使用大语言模型生成 SMT2 文件内容
def generate_smt2_content(prompt, max_retries=20, retry_delay=5):
    """
    生成 SMT2 文件内容，并支持重试机制。
	 prompt (str): 提供给模型的提示。
        max_retries (int): 最大重试次数，默认为 10。
        retry_delay (int): 每次重试之间的延迟时间（秒），默认为 5 秒。
    """
    attempt = 0
    while attempt < max_retries:
        try:
            response = client.chat.complete(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            # 提取生成的文本内容
            if hasattr(response, 'choices') and len(response.choices) > 0:
                return response.choices[0].message.content
            else:
                raise ValueError("Unexpected response format")
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
            attempt += 1
            time.sleep(retry_delay)  # 等待一段时间后重试
    raise RuntimeError(f"Failed to generate content after {max_retries} attempts")

import re

def save_to_smt2_file(content, file_path):
    """
    从 content 中提取 SMT2 格式内容。
    优先匹配 ```smt 或 ```smt2（不区分大小写）起始标记。
    若未找到，选择第一行包含 (set-logic 的行作为起始行。
    提取内容直到首次出现 (exit) 行，保留起始行和结尾行。
    若未找到起始标记或 (exit)，返回提示信息。
    """
    # 匹配起始标记 (不区分大小写)
    start_match = re.search(r'```(smt|smt2)\b', content, flags=re.IGNORECASE)
    start_index = -1
    extracted_content = ""

    if start_match:
        # 清除起始标记所在行
        start_index = start_match.start()
        start_line_end = content.find('\n', start_index)
        if start_line_end == -1:
            return "no mark!"
        post_start_content = content[start_line_end + 1:]
    else:
        # 选择第一个包含 (set-logic 的行作为起始行
        logic_match = re.search(r'(?i)^.*\(set-logic.*$', content, re.MULTILINE)
        if not logic_match:
            return "no mark!"
        post_start_content = content[logic_match.start():]

    # 分割内容为行列表
    lines = post_start_content.split('\n')
    extracted_lines = []
    found_exit = False

    # 逐行查找 (exit)
    for line in lines:
        extracted_lines.append(line)
        if '(exit)' in line.strip():
            found_exit = True
            break

    if not found_exit:
        return "no mark!"

    # 合并有效内容并标准化格式
    extracted_content = '\n'.join(extracted_lines).strip()

    # 将提取的内容写入文件
    with open(file_path, 'w') as f:
        f.write(extracted_content)

    return extracted_content


def run_z3(file_path):
    try:
        # 运行 Z3 并捕获输出，设置超时时间为 20 秒
        result = subprocess.run(['z3', file_path], capture_output=True, text=True, timeout=20)
        return result.stdout
    except subprocess.TimeoutExpired:
        # 如果超时，返回超时提示信息
        print("Z3 solver timed out after 20 seconds.")
        return "timed_out"
        

def mutate_smt2_v2(original_smt2):
    prompt = (
        f"""This is my initial SMT2 content: `{original_smt2}`. 
When modifying the original SMT2 content, ensure that the logic type remains QF_S and that the file contains between 20 to 35 lines, including only the SMT2 content without any explanatory language. 
Note that the QF_S logic does not support array operations, so avoid introducing any array-related functions or declarations. 
You can consider using the following string functions to enrich the content: str.contains, str.prefixof, str.suffixof, str.indexof, str.replace, str.substr, str.len, str.++, str.at, str.to.int, int.to.str. 
Ensure the modified SMT2 content remains syntactically correct and logically consistent with the QF_S logic. 
The file ends with `(exit)`."""
    )
    # 将选中的 form 内容添加到 prompt 中
    for form in selected_forms:
        prompt += form + "\n\n"

    smt2_file_path = 'temp000.smt2'
    error_detected = True
    start = time.time()
    it = 0

    while error_detected:
        flag = 1
        while flag:

            smt2_content = generate_smt2_content(prompt)
            smt2_content = save_to_smt2_file(smt2_content, smt2_file_path)
            if smt2_content != "no mark!":
                flag = 0

        z3_output = run_z3(smt2_file_path)

        if z3_output == 'timed_out' or 'error' not in z3_output.lower():
            error_detected = False
            end = time.time()
            print(f"Mistral API call took: {(end - start):.4f} seconds")
            return smt2_content

        if 'error' in z3_output.lower():
            it += 1
            if it < 5:
                print("Error detected in SMT2 file. Regenerating...")
                prompt = (
                    f"The following SMT2 content produced an error: {z3_output}. "
                    f"Original SMT2 content: {smt2_content}. "
                    "The logic type should be QF_S. The file should contain between 20 to 40 lines. "
                    "Modify the content to fix the error. If too many errors occur, consider changing the variation direction. "
                    "Only include the SMT2 content without any explanatory language."
                )
                # print("prompt:",prompt)
            else:
                # 生成随机部分
                random_length = 10  # 随机部分的长度
                random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=random_length))

                # 生成文件名
                file_name = f"error_{random_part}.smt2"
                
                error_folder = "error"
                if not os.path.exists(error_folder):
                    os.makedirs(error_folder)
                full_content = smt2_content + "\n" + z3_output
                file_path = os.path.join(error_folder, file_name)
                with open(file_path, 'w') as file:
                    file.write(full_content)
                print(f"Error content saved to {file_path}")

                folder_path = "/home/cass/Webstorm_project/0226/init_item"
                smt2_files = [file for file in os.listdir(folder_path) if file.endswith(".smt2")]
                if not smt2_files:
                    print("没有找到.smt2文件！")
                    return None
                selected_file = random.choice(smt2_files)
                file_path = os.path.join(folder_path, selected_file)
                with open(file_path, "r", encoding="utf-8") as file:
                    smt2_content = file.read()
                    save_to_smt2_file(smt2_content, smt2_file_path)
                    end = time.time()
                    print(f"Mistral API call took: {(end - start):.4f} seconds")
                    return smt2_content
# 对SMT-LIB 2文件进行突变并生成新的内容smt2_content
def generate_mutated_smt2_v2(original_smt2):
    mutated_smt2 = mutate_smt2_v2(original_smt2)
    # print("最终:",mutated_smt2)
    print("success!")

    return mutated_smt2
