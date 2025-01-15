from agents.role import Role
from agents.team import Team
from pathlib import Path
import sys, os, subprocess
import difflib

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from openai import OpenAI

from prompt.write_code_prompt import DEBUG, CODING_SYS, DEBUG_UNIT_TEST
from messages.message import Message
from utils.read import read_codebase, read_file_2_line
from ceaug.auto_test_prompt import (
    prompt_for_web_testing,
    prompt_for_gui_testing,
    prompt_for_game_testing,
    PROMPT_FOR_SCORING,
    PROMPT_FOR_TEST_ANA,
)
from ceaug.unit_test_utils import *


class Code_Tester(Role):
    name: str = "Tesla"
    profile: str = "Code Tester"
    team: Team = None
    own_message: Message = None
    unit_test_feedback: str = ""
    codebase_dir: str = ""

    def go(self):
        self.codebase_dir = os.path.join(Team.project_dir, "code")

        # 没有从codebase里读取
        code = self.getCode().content
        unit_test_feedback = self.unit_test_feedback

        system_prompt = SystemMessage(content=CODING_SYS)
        user_prompt_template = ChatPromptTemplate.from_template(DEBUG_UNIT_TEST)
        user_prompt_msg = user_prompt_template.invoke(
            {
                "code": code,
                "unit_test_report": unit_test_feedback,
            }
        )
        user_prompt = user_prompt_msg.to_messages()[0]
        Team.log.info(system_prompt.content + "\n" + user_prompt.content)
        fix_code_result = self.team.roles["Programmer"].llm.invoke(
            system_prompt, user_prompt
        )
        # logging
        Team.log.info("Tester | Fixed code based on the test :\n" + fix_code_result)

        self.team.roles["Programmer"].compare_code(fix_code_result)
        self.team.roles["Programmer"].store_code_dict(fix_code_result)

        self.team.roles["Programmer"].update_own_message(
            Message(sender="Programmer", content=fix_code_result)
        )
        

    # def go(self):
    #     self.codebase_dir = os.path.join(Team.project_dir, "code")

    #     # ______________ Level Zero: Test for syntax errors; check if the tests can run ______________
    #     architecture = self.getArchiture().content
    #     # if not web project

    #     # if web project
    #     if "flask" in architecture.lower():
    #         Team.log.info(
    #             "Tester | ----------- Use flask, please test by human --------------------"
    #         )
    #         test_msg = Message(sender=self.profile, content="Test Stop")
    #         self.own_message = test_msg
    #         Team.all_messages.append(test_msg)
    #         return

    #     test_turn = 1
    #     install_turn = 1
    #     Max_test_turn = 1
    #     Max_install_turn = 3

    #     # _____ iterative _____
    #     while test_turn <= Max_test_turn and install_turn <= Max_install_turn:
    #         # get entry file path
    #         main_py_path = self.get_entry_file()
    #         print(main_py_path)
    #         # test if code could run and get the running state
    #         result, result_data = self.run_main_py(main_py_path)
    #         #
    #         # if code run successfully
    #         if result == "SUCCESS":
    #             test_msg = Message(sender=self.profile, content="Test Success")
    #             self.own_message = test_msg
    #             Team.all_messages.append(test_msg)
    #             break
    #         # if breaks because lacking package
    #         elif result == "IMPORT_ERROR":
    #             Team.log.info("Tester | lacking third package:" + result_data)
    #             # install package
    #             install_result = self.install_package(result_data)
    #             # if install successfully
    #             if install_result == "INS_S":
    #                 print(
    #                     "Tester | Restarting the execution after installing the missing package."
    #                 )
    #                 Team.log.info(
    #                     "Tester | Restarting the execution after installing the missing package."
    #                 )
    #                 install_turn += 1
    #             # if install fails
    #             else:
    #                 test_msg = Message(
    #                     sender=self.profile, content="Test Install Failed"
    #                 )
    #                 self.own_message = test_msg
    #                 Team.all_messages.append(test_msg)
    #                 break
    #         # if breaks because other code problem
    #         elif result == "OTHER_ERROR":
    #             # Coding Error, call the Coder to fix
    #             print(f"An error occurred: {result_data}")
    #             Team.log.info("Tester | An error occurred: " + result_data)

    #             code = self.getCode().content
    #             system_prompt = SystemMessage(content=CODING_SYS)
    #             user_prompt_template = ChatPromptTemplate.from_template(DEBUG)
    #             user_prompt_msg = user_prompt_template.invoke(
    #                 {
    #                     "code": code,
    #                     "error_report": result_data,
    #                 }
    #             )
    #             user_prompt = user_prompt_msg.to_messages()[0]
    #             Team.log.info(system_prompt.content + "\n" + user_prompt.content)
    #             fix_code_result = self.team.roles["Programmer"].llm.invoke(
    #                 system_prompt, user_prompt
    #             )
    #             # logging
    #             Team.log.info(
    #                 "Tester | Fixed code based on the test :\n" + fix_code_result
    #             )
    #             self.team.roles["Programmer"].update_own_message(
    #                 Message(sender="Programmer", content=fix_code_result)
    #             )
    #             self.team.roles["Programmer"].message_to_file_test(fix_code_result)
    #             self.codebase_dir = os.path.join(Team.project_dir, "test_code")
    #             # # Re-test the fixed code, but only record the results without processing them.
    #             # self.run_main_py(main_py_path)
    #             test_turn += 1
    #     # test_msg = Message(sender=self.profile, content="Test Still Failed")
    #     # self.own_message = test_msg
    #     # Team.all_messages.append(test_msg)
    #     # _____ iterative _____
    #     # ______________ Level One: Test for syntax errors; check if the tests can run ______________
    #     #
    #     #
    #     #
    #     # ______________ Level Two: Unit test; check if code functions well ______________
    #     # config what unit test need
    #     project_category = Team.projec_catogory
    #     project_name = Team.project_name

    #     # get project's code
    #     code_base = read_codebase(self.codebase_dir)
    #     # get project's testcode
    #     test_code = test_code_autogen(self.codebase_dir, project_category, project_name)

    #     # apply unit test, will cd codebase_dir(which contains testcode.py) and execute it
    #     base_dir = Path.cwd()

    #     unit_test_raw_result = runUnitTest(
    #         self.codebase_dir, project_category, project_name
    #     )

    #     os.chdir(base_dir)

    #     unit_test_analysis = self.test_result_analyze(
    #         code_base, test_code, unit_test_raw_result
    #     )
    #     # ______________ Level Two: Unit test; check if code functions well ______________
    #     #
    #     #
    #     #
    #     # ______________ Level Three: step by step to fix code ______________

    #     # the most straight
    #     # read all the code skeleton

    #     if "<INFO> Finished" in review_result_level_1:
    #         # indicate low level problem, code review could fix
    #         pass

    #     # _____ check function not implemented _____
    #     function_add_ask = {
    #         "role": "user",
    #         "content": """
    #         unit test report: {sub_unit_test_report},
    #         codes:{codes}",

    #         "Based on the previous review results, a feature mentioned in the requirement {req} has not been implemented. You need to implement this feature. Here is the current project code:"
    #         """,
    #     }
    #     # _____ check function not implemented _____

    #     # _____ check static syntax error for unit test _____
    #     chat_messages = []
    #     skeleton = getSkeleton()

    #     skeleton_ana_sys = {
    #         "role": "system",
    #         "content": "you are a good Code Reviewer.",
    #     }
    #     # first, extract buggy code
    #     skeleton_ana_ask = {
    #         "role": "user",
    #         "content": """I have a software project with the code already implemented, along with its skeleton and unit test results. Based on the unit test results (known to failed or contain errors), please identify the specific block of the original code that is related to this test. Only the relevant code block needs to be identified.
    #         =======
    #         the project code is: {code}.
    #         the code skeleton is: {code_skeleton}.
    #         unit_test_result is: {unit_test_result}.
    #         related unit test case description is: {test_case_descption}.
    #         Think step by step and reason yourself to the right decisions to make sure we get it right.
    #         """.format_map(),
    #     }
    #     chat_messages.append(skeleton_ana_sys, skeleton_ana_ask)
    #     buggy_code = chat_to_LLM(chat_messages)
    #     chat_messages.append({"role": "assistant", "content": buggy_code})

    #     # after extracting the buggy code, first examine the syntax level(low level) bug
    #     # Mainly check for errors like unused variables, issues in data structures, or function parameters.

    #     # skeleton_ana(code_base, skeleton, unit_test_analysis)
    #     code_review_ask = {
    #         "role": "user",
    #         "content": """Now, we need to review the code based on the test report.
    #         unit test report: {sub_unit_test_report},
    #         codes:{codes},
    #         check the following formulated regulations:
    #         "1) all referenced classes should be imported;
    #         "2) all methods should be implemented;
    #         "3) all methods need to have the necessary comments;
    #         "you should check the above regulations one by one and review the codes in detail, and give me instructions on how to fix. If the codes are perfect and you have no comment on them, return only one line like \"<INFO> Finished\"."
    #         """,
    #     }
    #     review_result_level_1 = chat_messages.append(code_review_ask)
    #     chat_messages.append({"role": "assistant", "content": review_result_level_1})
    #     # _____ check static syntax error for unit test _____

    #     # line level fix
    #     fix_code()

    #     # run after test
    #     run()

    #     # if exceed max test turn, counter example fix

    #     #

    #     save_code()
    #     # ______________ Level Three: step by step to fix code ______________

    #     # If not exit from the while loop, it must be following two situations, which necessarily means there is an error

    def get_entry_file(self):
        # windows use \\ as path separator
        # Linux use / as path separator
        if Path(Team.project_dir + "test_code\\main.py").exists():
            entry_file = Team.project_dir + "test_code\\main.py"
        elif Path(Team.project_dir + "test_code\\app.py").exists():
            entry_file = Team.project_dir + "test_code\\app.py"
        elif Path(Team.project_dir + "review_code\\main.py").exists():
            entry_file = Team.project_dir + "review_code\\main.py"
        elif Path(Team.project_dir + "review_code\\app.py").exists():
            entry_file = Team.project_dir + "review_code\\app.py"
        elif Path(Team.project_dir + "code\\main.py").exists():
            entry_file = Team.project_dir + "code\\main.py"
        elif Path(Team.project_dir + "code\\app.py").exists():
            entry_file = Team.project_dir + "code\\app.py"
        else:
            return
        return entry_file

    def test_result_analyze(self, code_base, test_code, unit_test_result):
        messages = []
        values = {
            "code_base": code_base,
            "unit_test_code": test_code,
            "test_results": unit_test_result["output"],
        }
        # m_0, ask llm to analyze the unit test result
        PROMPT_FOR_TEST_ANA = """You are a software test analyst. Please help me analyze the code of a project.
        Here is the entire codebase for a project: {code_base}.
        Here are the unit test codes for this project: {unit_test_code}.
        These are all the unit test results (only including the failed ones):{test_results}

        Please analyze the test results one by one. For each unit test result, analyze step by step to identify the reasons for the test failure."""
        messages.append(PROMPT_FOR_TEST_ANA.format_map(values))
        unit_test_result_analysis = chat_to_LLM(messages)
        Team.log.info(str(messages[0]))
        Team.log.info(unit_test_result_analysis)
        return unit_test_result_analysis

    def run_main_py(self, main_py_path):
        """Execute the main.py file from the specified directory."""
        try:
            # Execute the main.py script with a timeout
            process = subprocess.Popen(
                [sys.executable, main_py_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            try:
                # Wait for a specified time or until the process completes
                stdout, stderr = process.communicate(
                    timeout=2
                )  # Adjust timeout as needed
                normal_exit = True
            except subprocess.TimeoutExpired:
                # Process is still running after timeout, terminate it
                process.terminate()
                stdout, stderr = (
                    process.communicate()
                )  # Fetch any remaining output after termination
                normal_exit = False

            # Decode output and error
            stdout = stdout.decode()
            stderr = stderr.decode()

            if normal_exit and process.returncode == 0:
                print("Program executed successfully with no errors.")
                Team.log.info("Tester | Program executed successfully with no errors.")
                return "SUCCESS", None
            elif not normal_exit:
                print(
                    "Process terminated due to timeout, which is considered as normal execution."
                )
                Team.log.info(
                    "Tester | Process terminated due to timeout, which is considered as normal execution."
                )
                return "SUCCESS", None
            else:
                print(f"Error: {stderr}")
                Team.log.info("Tester | Error: " + stderr)
                if "No module named" in stderr:
                    missing_package = (
                        stderr.split("No module named")[-1].strip().replace("'", "")
                    )
                    return "IMPORT_ERROR", missing_package
                else:
                    return "OTHER_ERROR", stderr

        except Exception as e:
            return "OTHER_ERROR", str(e)

    def install_package(self, package_name):
        """Install the missing package."""
        print(f"Installing missing package: {package_name}")
        Team.log.info("Installing missing package: " + package_name)
        try:
            # using subprocess & timeout
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package_name],
                timeout=120,  # timeout
                check=True,  # throw CalledProcessError if failed
            )
        except subprocess.TimeoutExpired:
            print(f"\nInstallation of {package_name} timed out after 120 seconds.")
            Team.log.info(
                "Tester | Installation of "
                + package_name
                + " timed out after 120 seconds."
            )
            return "INS_E"
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package_name}. Error: {e}")
            Team.log.info("Tester| Failed to install " + package_name)
            return "INS_E"
        else:
            if result.returncode == 0:
                print(f"Tester | {package_name} installed successfully.")
                Team.log.info(package_name + " installed successfully.")
            return "INS_S"

    def getArchiture(self):
        return Team.all_messages[2]

    def getCode(self):
        return Team.all_messages[4]
