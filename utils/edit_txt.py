import os
import re


def add_newline_to_txt_files(directory):
    """
    Recursively traverses a directory, finds all .txt files, and ensures they end with a newline character if not already present.

    :param directory: Path to the directory to process.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r+", encoding="utf-8") as f:
                        # 读取文件内容并移除多余的空行
                        lines = [
                            line.rstrip() for line in f.readlines() if line.strip()
                        ]

                        # 将处理后的内容写回文件
                        f.seek(0)
                        f.writelines(line + "\n" for line in lines)
                        f.truncate()  # 清除多余内容
                        print(f"Processed file: {file_path}")
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")


# "D:\Project\CE\CE\port.txt"
# "D:\\algorithm\\agent\\cese\\port.txt"
# port_dir = "./port.txt"
port_dir = "D:\Project\ATEdev\ATEDev_main\port.txt"


def read_port():

    with open(port_dir, "r") as file:
        port_number = file.read()
    return int(port_number)


def write_port(port):
    # "D:\\algorithm\\agent\\cese\\port.txt"
    try:
        with open(port_dir, "w") as file:
            file.write(str(port))
    except Exception as e:
        print(e)


def update_flask_port(file_path, port):
    # 读取用户输入的端口号
    if not port:
        port = read_port()
        port = port + 1

    # 读取 main.py 文件路径
    if not os.path.isfile(file_path):
        print("指定的文件路径不存在，请检查后重新运行程序。")
        return

    try:
        # 打开并读取文件内容
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # 找到最后一行 app.run 并替换为指定端口
        updated_lines = []
        replaced = False

        for line in lines:
            if not replaced and re.match(r"(\s*).*?app\.run\(.*\)", line):  # 匹配前缀
                indent = re.match(r"(\s*)", line).group(1)  # 提取缩进
                updated_lines.append(
                    f"{indent}app.run(port={port}, debug=False)\n"
                )  # 替换
                replaced = True  # 标志设置为 True，防止后续替换
            else:
                updated_lines.append(line)

        # 写回文件
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(updated_lines)

        # print(f"已成功将 {file_path} 文件的 Flask 端口修改为 {port}。")

    except Exception as e:
        print(f"发生错误: {e}")

    # write back the next available port
    write_port(port)
    return port


if __name__ == "__main__":
    # add_newline_to_txt_files("D:\Project\CE\CE\project\website\Headlinr\code")
    directory = "D:\Project\Datasets\SD-bench\codebase\website"
    try:
        # 获取目录的绝对路径
        directory = os.path.abspath(directory)

        # 遍历目录，查找子目录
        subdirs = [
            name
            for name in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, name))
        ]

        #     # 输出结果
        print("Subdirectories found:")

        for index, value in enumerate(subdirs):
            print(str(index) + " " + os.path.join(directory, value))
            update_flask_port(os.path.join(directory, value, "code", "main.py"), "")

    except Exception as e:
        print(f"Error while reading directory: {e}")
