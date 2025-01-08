import sys
import io
import unittest
import re
import sys
import os

def web_text_strip(input_text):

    patterns = [
        r"^.*?GetHandleVerifier.*$",
        r"^.*?\(No symbol\).*$",
        r"^.*?BaseThreadInitThunk.*$",
        r"^.*?RtlUserThreadStart.*$",
    ]

    # Combine patterns into a single regex
    combined_pattern = re.compile("|".join(patterns), re.MULTILINE)
    # Remove matching lines
    cleaned_text = re.sub(combined_pattern, "", input_text)
    # Remove extra blank lines
    cleaned_text = re.sub(r"\n+", "\n", cleaned_text).strip()
    print(cleaned_text)
    return cleaned_text

def runUnitTest():
    # Load the test files (testcode.py)
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Automatically load test cases from the testcode.py file
    suite.addTests(loader.discover("."))

    # Create a StringIO stream to capture both stdout and stderr
    output_stream = io.StringIO()
    error_stream = io.StringIO()

    # Create a TextTestRunner instance to run the tests and capture the output
    runner = unittest.TextTestRunner(stream=output_stream, verbosity=2)
    result = runner.run(suite)

    # Get the captured output and errors
    test_output = output_stream.getvalue()
    error_output = error_stream.getvalue()

    # Filter out some unimportant and repetitive output
    print("#### strip ####")
    test_output = web_text_strip(test_output)
    print(test_output)

    total = int(result.testsRun)
    passed = int(result.testsRun - len(result.failures) - len(result.errors))
    failed = len(result.failures)
    errors = len(result.errors)

    # Combine both stdout and stderr outputs
    combined_output = test_output + "\n" + error_output

    info = {
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "total": total,
        "output": combined_output,
    }

    print(f"Total tests run: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Errors: {errors}")
    print(f"output: {combined_output}")

    # 清除当前的测试套件和加载器
    suite._tests.clear()  # 清除测试套件中的测试用例
    loader = None  # 清除测试加载器对象
    suite = None  # 清空 TestSuite 对象
    output_stream.close()  # 关闭 StringIO 流
    return info

if __name__ == '__main__':
    runUnitTest()