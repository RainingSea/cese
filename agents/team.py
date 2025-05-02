import os
from pydantic import BaseModel, ConfigDict, Field
from typing import ClassVar, Optional
import asyncio
from agents.role import Role
from typing import Optional
from messages.message import Message
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

from agents.role import Role
from utils.log import Log
from ceaug.ceaug_main import (
    ceaug,
    test_code_generate,
    ceaug_vice,
    ceaug_vice_no_summary,
    create_ce_document,
    feedback_split,
    feedback_split_ds,
    feedback_split_string,
    make_ce_dirs,
    read_feedback,
)
from utils.edit_txt import add_newline_to_txt_files, update_flask_port


class Team(BaseModel):
    # team name
    team_name: str = "SES midnigt wanderer"
    # team roles
    roles: dict[str, Role] = Field(default_factory=dict, validate_default=True)

    str_roles: str = ""

    projec_catogory: str = ""
    project_name: str = ""

    # origin requirement from user
    origin_requirement: str = ""
    explore_num: int = 0
    test_cases_dir: str = 0

    all_messages_d: dict[str, Message] = Field(
        default_factory=dict, validate_default=True
    )
    log: ClassVar[Optional[Log]] = None

    # workdir
    workdir: ClassVar[str] = ""
    all_messages: ClassVar[list[Message]] = []
    project_dir_abs: ClassVar[str] = ""
    project_dir: ClassVar[str] = ""
    incremental_base_dir: ClassVar[str] = ""
    active_roles: ClassVar[list[str]] = []
    cost: ClassVar[int] = 0

    def run_test(self):

        self.roles["Product Manager"].go()
        self.roles["Architect"].go_in_sample()
        self.roles["Programmer"].go_in_sample()

    def run_self_evo(self):
        previous_work_dir = Path.cwd()
        pervious_project_dir = Team.project_dir

        # inter_launch = True
        inter_launch = False

        # _______________ generate PRD, Architect, Task Plan _______________
        if inter_launch:
            # Read files from an existing project, then proceed with development.
            # go_inter() represents reading existing files to serve as artifacts for roles in the workflow.
            Team.incremental_base_dir = os.path.normpath(
                "D:\Project\CE\CE\project\website\RecipeHub"
            )
            self.roles["Product Manager"].go_inter()
            self.roles["Architect"].go_inter()
            self.roles["Project Manager"].go_inter()
        else:
            self.roles["Product Manager"].go()
            Team.active_role(self.roles["Product Manager"].profile)

            self.roles["Architect"].go()
            # self.roles["Reviewer"].target = self.roles["Architect"]
            # self.roles["Reviewer"].go()
            Team.active_role(self.roles["Architect"].profile)

            self.roles["Project Manager"].go()
            # self.roles["Reviewer"].target = self.roles["Project Manager"]
            # self.roles["Reviewer"].go()
            Team.active_role(self.roles["Project Manager"].profile)

        # generate code
        self.roles["Programmer"].go()
        # codebase dir
        code_base_dir = os.path.join(Team.project_dir, "code")
        # port = update_flask_port(os.path.join(code_base_dir, "main.py"), "")

        # 这个2就是重复测试的次数
        for j in range(1):
            # set code dir
            ce_projects_paths = [Team.project_dir]
            # execute unit test
            ce_score, ce_feedback = ceaug(
                previous_work_dir,
                self.test_cases_dir,
                ce_projects_paths,
                Team.projec_catogory,
                Team.project_name,
                "self_evo",
                Team.log,
            )
            # use feedback to regenate
            # self.roles["C_Programmer"].go(ce_feedback)
            if ce_feedback == "CodeIsGood":
                return
            else:
                print(ce_feedback)

                pass_feedback, no_pass_feedback = feedback_split(ce_feedback)
                if no_pass_feedback:
                    Team.log.info("No Pass Feedback:\n" + str(no_pass_feedback))
                # 测试就不需要处理通过的单元测试反馈了，只需要处理出错的
                init = True
                if no_pass_feedback:
                    # 迭代式的取出切片后的反馈，然后交给code tester来修改
                    for n_passfd in no_pass_feedback:
                        self.roles["Code Tester"].unit_test_feedback = n_passfd
                        if init:
                            self.roles["Code Tester"].go()
                            init = False
                        else:
                            self.roles["Code Tester"].go()

                # port = update_flask_port(
                #     os.path.join(code_base_dir, "main.py"), str(port)
                # )
            # 每个测试流程结束后写入一次本地文件
            self.roles["Programmer"].message_to_file(
                self.roles["Programmer"].own_message.content
            )

        # 将最初的分配的端口写入
        # port = update_flask_port(os.path.join(code_base_dir, "main.py"), str(port))

        return

    # 跑实验web特调版run()方法
    def run_web(self):
        # root work dir
        previous_work_dir = Path.cwd()
        # root project dir
        pervious_project_dir = Team.project_dir

        # Generate PRD, no exploration
        self.roles["Product Manager"].go()

        # make ce dirs and copy the PRD to each dir
        ce_projects_paths = make_ce_dirs(Team.project_dir, self.explore_num)

        # _________________________ [ EXPLORE ] ____________________________

        for j in range(len(ce_projects_paths)):

            # temporarily change project dir to a ce folder
            Team.incremental_base_dir = os.path.normpath(ce_projects_paths[j])
            Team.project_dir = ce_projects_paths[j]

            self.roles["Product Manager"].go_inter()
            self.roles["Architect"].go_in_sample()
            self.roles["Project Manager"].go_in_sample()
            self.roles["Programmer"].go_in_sample()

            self.roles["Programmer"].code_base.clear()

            code_base_dir = os.path.join(Team.project_dir, "code")
            port = update_flask_port(os.path.join(code_base_dir, "main.py"), "")

        # generate feedbacks of explored projects above
        ce_score, ce_feedbacks = ceaug(
            previous_work_dir,
            self.test_cases_dir,
            ce_projects_paths,
            Team.projec_catogory,
            Team.project_name,
            "ite_fdback",
            Team.log,
        )

        # |_____________________________________________________________|
        # |                      Attention!                             |
        # | ceaug() execute unit test, which                            |
        # | requires switching work dir to the test code's project dir "|
        # |                   Must switch back!                         |
        # |_____________________________________________________________|
        # |

        os.chdir(previous_work_dir)
        Team.project_dir = pervious_project_dir
        Team.incremental_base_dir = pervious_project_dir

        # save feedback of this turn to a log file (formatted)
        # 这里最好是写入到一个txt中，但我不知道为什么写入txt，程序就会异常退出
        save = True
        if save:
            for key, value in ce_feedbacks.items():
                # 格式化键值对并在键和值的左右添加"#_#"标记
                formatted_key = "#_#{}#_#".format(key)
                formatted_value = value
                # 将格式化后的键值对写入文件，键和值之间用空格、冒号或其他符号分隔
                # f.write(f"{formatted_key} \n{formatted_value}\n\n\n")
                print(formatted_key)
                print(formatted_value)

                Team.log.info(
                    "ITERATIVE_FEEDBACK "
                    + str(formatted_key)
                    + "\n"
                    + str(formatted_value)
                )

        # _________________________ [ REGENERATE ] ____________________________

        self.roles["Product Manager"].go_inter()
        self.roles["Architect"].go_with_fdback(ce_feedbacks["arch"])
        self.roles["Project Manager"].go_with_fdback(ce_feedbacks["plan"])

        ce_feedback = ce_feedbacks["code"]
        if ce_feedback:
            if ce_feedback == "CodeIsGood":
                print("Dev execute END")
                return

            Team.log.info("begin CE Coding")
            # C_programmer temperature is 0.2

            pass_feedback, no_pass_feedback = feedback_split_ds(ce_feedback)
            if pass_feedback:
                Team.log.info("Pass Feedback:\n" + str(pass_feedback))
            if no_pass_feedback:
                Team.log.info("No Pass Feedback:\n" + str(no_pass_feedback))
            # process pass feedback
            init = True

            self.roles["C_Programmer"].go("init", "0")

            if pass_feedback:
                for passfd in pass_feedback:
                    self.roles["C_Programmer"].go(passfd, "1")
                    self.roles["C_Programmer"].message_to_file(
                        self.roles["C_Programmer"].own_message.content
                    )
            # process no pass feedback
            if no_pass_feedback:
                for n_passfd in no_pass_feedback:

                    self.roles["C_Programmer"].go(n_passfd, "2")
                    # write only once
                    self.roles["C_Programmer"].message_to_file(
                        self.roles["C_Programmer"].own_message.content
                    )

        else:
            Team.log.info("No CE, Normal Coding")
            self.roles["Programmer"].code_base.clear()
            self.roles["Programmer"].go()

        code_base_dir = os.path.join(Team.project_dir, "code")
        port = update_flask_port(os.path.join(code_base_dir, "main.py"), "")

        print("Dev execute END")
        return

    # K的实验，可以读取之前的反馈（必须是总结好的）
    def run_web_iterative(self):
        # root work dir
        previous_work_dir = Path.cwd()
        # root project dir
        pervious_project_dir = Team.project_dir

        # _______________ generate PRD, Architect, Task Plan _______________

        Team.incremental_base_dir = Team.project_dir
        self.roles["Product Manager"].go_inter()

        # make ce dirs and copy the prd to each dir
        ce_projects_paths = make_ce_dirs(Team.project_dir, self.explore_num)

        # _________________________ [ EXPLORE ] ____________________________
        # generate sampling architect

        # 读取之前生成的反馈
        # 提取架构，计划和代码等的反馈
        pre_feedbacks = read_feedback(os.path.join(Team.project_dir, "feedbacks.txt"))

        for j in range(len(ce_projects_paths)):

            Team.incremental_base_dir = os.path.normpath(ce_projects_paths[j])
            Team.project_dir = ce_projects_paths[j]

            self.roles["Product Manager"].go_inter()
            self.roles["Architect"].go_in_sample_with_fdback(
                pre_feedbacks["#_#architecture_feedback#_#"]
            )
            self.roles["Project Manager"].go_in_sample_with_fdback(
                pre_feedbacks["#_#task_plan_feedback#_#"]
            )

            pass_feedback, no_pass_feedback = feedback_split_string(
                pre_feedbacks["#_#code_feedback#_#"]
            )
            self.roles["Programmer"].go_in_sample_with_fdback(pass_feedback, "0")
            if pass_feedback:
                Team.log.info("Pass Feedback:\n" + str(pass_feedback))
                self.roles["Programmer"].go_in_sample_with_fdback(pass_feedback, "1")

            if no_pass_feedback:
                Team.log.info("No Pass Feedback:\n" + str(no_pass_feedback))
                self.roles["Programmer"].go_in_sample_with_fdback(no_pass_feedback, "2")

            self.roles["Programmer"].code_base.clear()
            code_base_dir = os.path.join(Team.project_dir, "code")
            port = update_flask_port(os.path.join(code_base_dir, "main.py"), "")

        # generate feedbacks of explored projects above
        ce_score, ce_feedbacks = ceaug(
            previous_work_dir,
            self.test_cases_dir,
            ce_projects_paths,
            Team.projec_catogory,
            Team.project_name,
            "ite_fdback",
            Team.log,
        )

        # |_____________________________________________________________|
        # |                      Attention!                             |
        # | ceaug() execute unit test, which                            |
        # | requires switching work dir to the test code's project dir "|
        # |                   Must switch back!                         |
        # |_____________________________________________________________|
        # |

        os.chdir(previous_work_dir)
        Team.project_dir = pervious_project_dir
        Team.incremental_base_dir = pervious_project_dir

        # save feedback of this turn to a log file (formatted)
        # 这里最好是写入到一个txt中，但我不知道为什么写入txt，程序就会异常退出
        save = True
        if save:
            for key, value in ce_feedbacks.items():
                # 格式化键值对并在键和值的左右添加"#_#"标记
                formatted_key = "#_#{}#_#".format(key)
                formatted_value = value
                # 将格式化后的键值对写入文件，键和值之间用空格、冒号或其他符号分隔
                # f.write(f"{formatted_key} \n{formatted_value}\n\n\n")
                print(formatted_key)
                print(formatted_value)

                Team.log.info(
                    "ITERATIVE_FEEDBACK "
                    + str(formatted_key)
                    + "\n"
                    + str(formatted_value)
                )

        # _________________________ [ REGENERATE ] ____________________________

        self.roles["Product Manager"].go_inter()
        self.roles["Architect"].go_with_fdback(ce_feedbacks["arch"])
        self.roles["Project Manager"].go_with_fdback(ce_feedbacks["plan"])

        ce_feedback = ce_feedbacks["code"]
        if ce_feedback:
            

            Team.log.info("begin CE Coding")
            # C_programmer temperature is 0.2

            pass_feedback, no_pass_feedback = feedback_split_ds(ce_feedback)
            
            if pass_feedback:
                Team.log.info("Pass Feedback:\n" + str(pass_feedback))
            if no_pass_feedback:
                Team.log.info("No Pass Feedback:\n" + str(no_pass_feedback))
            # process pass feedback
            init = True

            self.roles["C_Programmer"].go("init", "0")

            if pass_feedback:
                for passfd in pass_feedback:
                    self.roles["C_Programmer"].go(passfd, "1")
                    self.roles["C_Programmer"].message_to_file(
                        self.roles["C_Programmer"].own_message.content
                    )
            # process no pass feedback
            if no_pass_feedback:
                for n_passfd in no_pass_feedback:

                    self.roles["C_Programmer"].go(n_passfd, "2")
                    # write only once
                    self.roles["C_Programmer"].message_to_file(
                        self.roles["C_Programmer"].own_message.content
                    )

        code_base_dir = os.path.join(Team.project_dir, "code")
        port = update_flask_port(os.path.join(code_base_dir, "main.py"), "")

        print("Dev execute END")
        return

    # 只生成测试代码
    def run_before_test(self):
        # root work dir
        previous_work_dir = Path.cwd()
        # root project dir
        pervious_project_dir = Team.project_dir

        # Generate PRD, no exploration
        self.roles["Product Manager"].go()

        # make ce dirs and copy the PRD to each dir
        ce_projects_paths = make_ce_dirs(Team.project_dir, self.explore_num)

        # _________________________ [ EXPLORE ] ____________________________

        for j in range(len(ce_projects_paths)):
            print(f"\ngenerate the architect of {j}th counter project\n")
            # temporarily change project dir to a ce folder
            Team.incremental_base_dir = os.path.normpath(ce_projects_paths[j])
            Team.project_dir = ce_projects_paths[j]

            self.roles["Product Manager"].go_inter()
            self.roles["Architect"].go_in_sample()
            self.roles["Project Manager"].go_in_sample()
            self.roles["Programmer"].go_in_sample()

            self.roles["Programmer"].code_base.clear()

            # code_base_dir = os.path.join(Team.project_dir, "code")
            # port = update_flask_port(os.path.join(code_base_dir, "main.py"), "")

        # generate feedbacks of explored projects above
        ce_score, ce_feedbacks = test_code_generate(
            previous_work_dir,
            self.test_cases_dir,
            ce_projects_paths,
            Team.projec_catogory,
            Team.project_name,
            "ite_fdback",
            Team.log,
        )

        # |_____________________________________________________________|
        # |                      Attention!                             |
        # | ceaug() execute unit test, which                            |
        # | requires switching work dir to the test code's project dir "|
        # |                   Must switch back!                         |
        # |_____________________________________________________________|
        # |

        os.chdir(previous_work_dir)
        Team.project_dir = pervious_project_dir
        Team.incremental_base_dir = pervious_project_dir

        # save feedback of this turn to a log file (formatted)
        # 这里最好是写入到一个txt中，但我不知道为什么写入txt，程序就会异常退出
        save = True
        if save:
            for key, value in ce_feedbacks.items():
                # 格式化键值对并在键和值的左右添加"#_#"标记
                formatted_key = "#_#{}#_#".format(key)
                formatted_value = value
                # 将格式化后的键值对写入文件，键和值之间用空格、冒号或其他符号分隔
                # f.write(f"{formatted_key} \n{formatted_value}\n\n\n")
                print(formatted_key)
                print(formatted_value)

                Team.log.info(
                    "ITERATIVE_FEEDBACK "
                    + str(formatted_key)
                    + "\n"
                    + str(formatted_value)
                )

        # _________________________ [ REGENERATE ] ____________________________

        print("Dev execute END")
        return

    # 单生成
    def run_pure(self):
        # root work dir
        previous_work_dir = Path.cwd()
        # root project dir
        pervious_project_dir = Team.project_dir

        # Generate PRD, no exploration
        self.roles["Product Manager"].go()
        self.roles["Architect"].go()
        self.roles["Project Manager"].go()
        self.roles["Programmer"].go()

        self.roles["Programmer"].code_base.clear()
        code_base_dir = os.path.join(Team.project_dir, "code")
        # port = update_flask_port(os.path.join(code_base_dir, "main.py"), "")

    # generate unit test or use feedback exist
    def run_vice(self, seq):

        previous_work_dir = Path.cwd()
        pervious_project_dir = Team.project_dir

        inter_launch = True

        # _______________ generate PRD, Architect, Task Plan _______________
        if inter_launch:
            Team.incremental_base_dir = os.path.join(
                "D:\Project\CE\CE\project",
                Team.projec_catogory,
                Team.project_name,
            )
            self.roles["Product Manager"].go_inter()
        else:
            self.roles["Product Manager"].go()
            Team.active_role(self.roles["Product Manager"].profile)

        ce_score = 0
        ce_feedbacks = ""

        # ___________________ one to one test and get result _________________
        if seq != "666":
            ce_projects_paths = []

            _path = os.path.join(
                "D:\Project\CE\CE\project",
                Team.projec_catogory,
                Team.project_name,
                "ce",
                f"ce_{seq}",
            )
            ce_projects_paths.append(_path)

            # 只执行测试，flag是ite_fdbackQAQ，因此不会总结
            ce_score, ce_feedbacks = ceaug(
                previous_work_dir,
                self.test_cases_dir,
                ce_projects_paths,
                Team.projec_catogory,
                Team.project_name,
                "ite_fdbackQAQ",
                Team.log,
            )
            return

        # ___________________ one to one test and get result _________________

        # ___________________ read feedbacks ___________________
        # 属于vice的部分 -- 路径格式
        # 这部分可以拿来读取已经测试过的unit test result

        if seq == "666":
            ce_projects_paths = []
            # 更改反馈的次数

            ce_index = 0
            for i in range(3):
                ce_projects_paths.append(
                    os.path.join(
                        "D:\Project\CE\CE\project",
                        Team.projec_catogory,
                        Team.project_name,
                        "ce",
                        f"ce_{ce_index}",
                    )
                )
                ce_index = ce_index + 1

            ce_score, ce_feedbacks = ceaug_vice(
                previous_work_dir,
                ce_projects_paths,
                Team.projec_catogory,
                Team.project_name,
                "ite_fdback",
                Team.log,
            )

        # ___________________ read feedbacks ___________________

        # |_____________________________________________________________|
        # |                      Attention!                             |
        # | ceaug() execute unit test, which                            |
        # | requires switching work dir to the test code's project dir "|
        # |                   Must switch back!                         |
        # |_____________________________________________________________|
        # |

        os.chdir(previous_work_dir)
        Team.project_dir = pervious_project_dir
        Team.incremental_base_dir = pervious_project_dir

        # _______________ use feedback to generate document _______________
        self.roles["Product Manager"].go_inter()
        self.roles["Architect"].go_with_fdback(ce_feedbacks["arch"])
        # self.roles["Architect"].go()
        self.roles["Project Manager"].go_with_fdback(ce_feedbacks["plan"])
        # self.roles["Project Manager"].go()

        ce_feedback = ce_feedbacks["code"]
        if ce_feedback:
            if ce_feedback == "CodeIsGood":
                print("Dev execute END")
                return
            
            Team.log.info("begin CE Coding")
            # C_programmer temperature is 0.2

            pass_feedback, no_pass_feedback = feedback_split(ce_feedback)

            if pass_feedback:
                Team.log.info("Pass Feedback:\n" + str(pass_feedback))
            if no_pass_feedback:
                Team.log.info("No Pass Feedback:\n" + str(no_pass_feedback))
            # process pass feedback
            init = True
            if pass_feedback:
                for passfd in pass_feedback:
                    if init:
                        self.roles["C_Programmer"].go(passfd, "0")
                        init = False
                    else:
                        self.roles["C_Programmer"].go(passfd, "1")
                    self.roles["C_Programmer"].message_to_file(
                        self.roles["C_Programmer"].own_message.content
                    )
            # process no pass feedback
            if no_pass_feedback:
                for n_passfd in no_pass_feedback:
                    if init:
                        self.roles["C_Programmer"].go(n_passfd, "0")
                        init = False
                    else:
                        self.roles["C_Programmer"].go(n_passfd, "2")
                    # write only once
                    self.roles["C_Programmer"].message_to_file(
                        self.roles["C_Programmer"].own_message.content
                    )

            # self.roles["C_Programmer"].check_data_format()
            # self.roles["C_Programmer"].message_to_file(
            #     self.roles["C_Programmer"].own_message.content
            # )
        else:
            Team.log.info("No CE, Normal Coding")
            self.roles["Programmer"].code_base.clear()
            self.roles["Programmer"].go()

        if Team.projec_catogory == "website":
            code_base_dir = os.path.join(Team.project_dir, "code")
            port = update_flask_port(os.path.join(code_base_dir, "main.py"), "")

        print("Dev execute END")
        return

    def run_inter(self):
        previous_work_dir = Path.cwd()
        pervious_project_dir = Team.project_dir

        inter_launch = True

        # _______________ generate PRD, Architect, Task Plan _______________
        if inter_launch:
            # Read files from an existing project, then proceed with development.
            # go_inter() represents reading existing files to serve as artifacts for roles in the workflow.
            Team.incremental_base_dir = os.path.normpath(
                # "D:\Project\CE\CE\project\website\PersonalBlog_20250112143843"
                # f"D:\\algorithm\\agent\\cese\\dataset\\SD-bench\\codebase\\{}"
                # pervious_project_dir
            )
            self.roles["Product Manager"].go_inter()
            self.roles["Architect"].go_inter()
            self.roles["Project Manager"].go_inter()

        ce_feedback = """### Passed Test Cases
There were no test cases that passed successfully.

### Failed or Error Test Cases

1. |Case|:**create_new_blog_post**
   - **Error**: `NoSuchElementException` for "Create New Post" link.
   - **Analysis**: The test fails to find the link, likely due to unsuccessful login, which prevents access to the main page.

2. |Case|:**delete_blog_post**
   - **Error**: `NoSuchElementException` for delete button.
   - **Analysis**: Similar to the previous test, the absence of the delete button may stem from a failed login or because posts aren't displayed.

3. |Case|:**edit_existing_post**
   - **Error**: `NoSuchElementException` for "First Post" link.
   - **Analysis**: Test cannot locate the post link due to login failure or due to no posts being displayed.

4. |Case|:**user_login**
   - **Failure**: The user was not directed to the main page. Assertion error indicating "Main Blog Page" is not found, showing a 404 error instead.
   - **Analysis**: This points to issues in the login flow leading to improper redirection.

5. |Case|:**user_registration**
   - **Failure**: The content for registration success was not found on the page, indicating that the registration process failed.
   - **Analysis**: This may be due to duplicate username checks or issues in user creation functionality.

6. |Case|:**view_blog_posts**
   - **Failure**: The test found no posts available to display.
   - **Analysis**: Likely indicates that the create post functionality is not working correctly or hasn't been triggered prior.

### Guidance to Resolve Issues
1. **Ensure Robust Authentication**:
   - Implement thorough checks in the registration and login mechanisms. Make sure that errors (e.g., username already in use) are handled gracefully and provide clear messaging to the user, which can also facilitate debugging during development.

2. **Validation of Post Operations**:
   - Before conducting tests related to posts (create, edit, delete), ensure that the functionality for creating a post is working correctly. This prevents subsequent tests from failing due to dependent operations that haven't been successfully implemented.

3. **Manage Routes and Responses**:
   - Clearly define the routes and their expected behaviors post-login. Ensure that routing logic in the Flask app leads users to the correct pages based on their authentication state. Any failure in routing should yield appropriate responses rather than exposing a 404 error.

4. **Perform Data Persistence Checks**:
   - Regularly verify that data (users and posts) is being saved correctly and that retrieval operations work as intended (i.e., posts being available after being created). Consider implementing unit tests for these functionalities as well.

5. **Maintain Clear Communication in the Application**:
   - Ensure that for every operation (registration, login, post creation, etc.), the application provides feedback to the user, such as success or failure messages. This aids both user experience and debugging.

6. **Log Important Events**:
   - Introduce logging mechanisms to trace important actions and errors within the application. Observing logs can provide insight into where failures occur during operational testing or debugging sessions. 

By addressing these areas during the development process, you can create a more robust application that minimizes issues reflected in unit tests and enhances overall code stability.
        """
        if ce_feedback:
            if ce_feedback == "CodeIsGood":
                print("Dev execute END")
                return
            # ceaug finally return the most valuable(temporarily is 1 case) project issues feedback
            Team.log.info("### ceaug feedback\n" + str(ce_feedback))
            # use feedback from counter example to augment coding
            Team.log.info("begin CE Coding")
            # C_programmer temperature is 0.2

            pass_feedback, no_pass_feedback = feedback_split(ce_feedback)
            if pass_feedback:
                Team.log.info("Pass Feedback:\n" + str(pass_feedback))
            if no_pass_feedback:
                Team.log.info("No Pass Feedback:\n" + str(no_pass_feedback))
            # process pass feedback
            init = True
            if pass_feedback:
                for passfd in pass_feedback:
                    if init:
                        self.roles["C_Programmer"].go(passfd, "0")
                        init = False
                    else:
                        self.roles["C_Programmer"].go(passfd, "1")
            # process no pass feedback
            if no_pass_feedback:
                for n_passfd in no_pass_feedback:
                    if init:
                        self.roles["C_Programmer"].go(n_passfd, "0")
                        init = False
                    else:
                        self.roles["C_Programmer"].go(n_passfd, "2")
            # write only once
            self.roles["C_Programmer"].message_to_file(
                self.roles["C_Programmer"].own_message.content
            )
        else:
            Team.log.info("No CE, Normal Coding")
            self.roles["Programmer"].code_base.clear()
            self.roles["Programmer"].go()

        code_base_dir = os.path.join(Team.project_dir, "code")
        # port = update_flask_port(os.path.join(code_base_dir, "main.py"), "")

        print("Dev execute END")
        return

    @classmethod
    def set_projdir(cls, projdir: str):
        Team.project_dir = projdir
        abs_projdir = Path(projdir).absolute()
        print("相对路径为：" + str(projdir))
        print("绝对路径为：" + str(abs_projdir))
        Team.project_dir_abs = abs_projdir

        if not os.path.exists(Team.project_dir):
            os.makedirs(Team.project_dir)

    @classmethod
    def set_log(cls):
        # Create a log in the working directory
        log_dir = Team.project_dir + "log.log"
        log = Log(log_path=log_dir)
        Team.log = log.setup_logger()
        # log the dir information here because sequence
        Team.log.info("Setting Project Dir to " + Team.project_dir)

    def project_statistics(self):
        # statistics for projects
        stat = {}
        stat["team_name"] = self.team_name
        stat["team roles"] = Team.active_roles
        stat["project name"] = self.project_name
        stat["origin requirement"] = self.origin_requirement
        stat["token_usage"] = Team.cost
        return stat

    def log_project_stat(self):
        # log function dedicated for above stat
        stat = self.project_statistics()
        stat_format = (
            "Team Name: "
            + stat["team_name"]
            + "\n"
            + "Team Roles: "
            + str(stat["team roles"])
            + "\n"
            + "Project Name: "
            + stat["project name"]
            + "\n-----------------\n"
            + "ALL COST FOR PROJECT IS: "
            + str(stat["token_usage"])
        )
        return stat_format

    @classmethod
    def active_role(cls, role_str: str):
        Team.active_roles.append(role_str)

    @classmethod
    def get_active_roles(cls):
        # actually equals return Team.active_roles
        result = []
        for _name in Team.active_roles:
            result.append(_name)
        return result

    def set_origin_req(self, project_name, original_requirement):
        self.project_name = project_name
        self.origin_requirement = original_requirement
        self.all_messages.append(Message(sender="User", content=original_requirement))
        self.all_messages_d["original_requirement"] = Message(
            sender="User", content=original_requirement
        )

    # hire single role
    def hire_role(self, role: Role):
        self.roles[role.profile] = role

    # hire multiple role, paras are passed in list
    def hire_roles(self, *roles: list[Role]):
        for role in roles:
            self.roles[role.profile] = role

    # fire role (not used for now)
    def fire_role(self, role: Role):
        self.roles.pop(role.profile)

    def get_team_roles(self):
        """
        return a list containing the names of all roles in the Team.
        """
        get_team_roles_result = []
        for key, role in self.roles.items():
            get_team_roles_result.append(role.profile)
        return get_team_roles_result
