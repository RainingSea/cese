import re
import os


def remove_time_sleep_after_popen(test_code):
    """
    删除 subprocess.Popen 后紧接的以 time.sleep 开头的行。

    :param test_code: 输入的代码字符串
    :return: 更新后的代码字符串
    """
    # 正则模式：匹配 subprocess.Popen(...) 后面紧接的以 time.sleep(...) 开头的行
    # 这里我们使用 \s* 来允许 space 和注释
    pattern = r"(subprocess\.Popen\(.*?\)\s*\n)\s*time\.sleep\(.*?\)\s*(#.*)?\n"

    # 使用 re.sub 替换匹配的内容，去掉 time.sleep 的行
    updated_code = re.sub(pattern, r"\1", test_code)
    return updated_code

def list_directories(path):
    """
    列出指定路径下的所有文件夹名字（不递归）。

    :param path: 要遍历的根路径
    :return: 文件夹名字的列表
    """
    # 列出指定路径下的所有文件和文件夹
    entries = os.listdir(path)
    # 过滤仅保留文件夹
    directories = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]
    return directories

def read_file(filename):
    with open(filename, 'r', encoding = 'utf-8') as file:
        return file.read()

def write_file(filename, content):
    with open(filename, 'w', encoding = 'utf-8') as file:
        file.write(content)

if __name__ == "__main__":
    pro = "D:\\algorithm\\agent\\cese\\dataset\\SD-bench\\codebase\\website\\"
    directs = list_directories(pro)
    for direct in directs:
        code_path = os.path.join(pro, direct, 'code', 'testcode.py')
        content = read_file(code_path)
        new_code = remove_time_sleep_after_popen(content)
        write_file(code_path, new_code)

