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
                        content = f.read()
                        # Check if the file is empty or already ends with a newline
                        if content and not content.endswith("\n"):
                            f.write("\n")
                            print(f"Added newline to: {file_path}")
                        else:
                            print(f"No changes needed for: {file_path}")
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")


def read_port():
    # "D:\Project\CE\CE\port.txt"
    with open("D:\\algorithm\\agent\\cese\\port.txt", "r") as file:
        port_number = file.read()
    return int(port_number)


def write_port(port):
    try:
        with open("D:\\algorithm\\agent\\cese\\port.txt", "w") as file:
            file.write(str(port))
    except Exception as e:
        print(e)


def update_flask_port(file_path):
    # 读取用户输入的端口号
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
        for line in lines:
            if re.search(r"app\.run\(.*\)", line):
                updated_lines.append(f"    app.run(port={port}, debug=True)\n")
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


if __name__ == "__main__":
    update_flask_port()
