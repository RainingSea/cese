import os


def generate_commands(folder_path, category):
    file_count = 0  # 初始化文件计数器

    # 遍历给定目录下的所有文件
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        if os.path.isfile(full_path):
            # 打印出转换后的命令行形式
            print(f"python start_by_file.py --category {category} --name {filename}")
            file_count += 1  # 每找到一个文件就增加计数器

    # 输出总文件数量
    print(f"\nTotal files processed: {file_count}")


# 使用示例
folder_path = (
    "D:\Project\CE\CE\dataset\SD-bench\dataset\gui"  # 替换为你的文件夹路径
)
category = "gui"  # 你想要设置的category值
generate_commands(folder_path, category)
