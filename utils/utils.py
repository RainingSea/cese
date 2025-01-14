import re

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