import os
import re
import json
import ast
from pydantic import Field
from pathlib import Path
import difflib

# langchain lib
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage

# project's utility lib
from utils.commen import str_to_role
from utils.edit_txt import add_newline_to_txt_files

# custom lib
from prompt.write_code_prompt import (
    CODING_SYS,
    CODING_C,
    CODING,
    CODING_FD,
)
from prompt.meta_prompt import META_PROMPT

from prompt.align_prompt import ALIGN_WITH_WHO
from agents.role import Role
from agents.team import Team
from agents.searcher import Searcher
from messages.message import Message
from utils.read import read_file_2_line
from utils.edit_txt import update_flask_port


class Programmer(Role):
    name: str = "Clorinde"
    profile: str = "Programmer"
    llm: object
    llm_sample: object
    system_msg: str = CODING_SYS
    own_message: Message = None
    team: Team = None
    action: str = "Code"
    code_base: dict[str, str] = Field(default_factory=dict, validate_default=True)

    def go(self):
        print(self.profile + " " + self.name + " Coding...")
        Team.log.info(self.profile + " " + self.name + " Coding...")

        # ---------- get the information needed from SCR ----------
        functional_requirement = self.getPRD().content
        architecture = self.getArchiture().content
        task_plan = self.getProjectPlan().content

        system_prompt = SystemMessage(content=CODING_SYS)
        user_prompt_template = ChatPromptTemplate.from_template(CODING)
        user_prompt_msg = user_prompt_template.invoke(
            {
                "architecture": architecture,
                "task_plan": task_plan,
            }
        )
        user_prompt = user_prompt_msg.to_messages()[0]
        # prompt LLM

        Team.log.info(system_prompt.content + "\n" + user_prompt.content)
        code_result = self.llm.invoke(system_prompt, user_prompt)
        Team.log.info("Generated Code: \n" + code_result)
        # ________ store in self code dict ________
        # Team.log.info("Compare Code")
        # self.compare_code(code_result)
        code_result_split = code_result.split("*** ")
        for i in range(1, len(code_result_split)):
            file_name, file_content = self.match(code_result_split[i])
            self.code_base[file_name] = file_content

        self.message_to_file(code_result)
        code_msg = Message(sender=self.profile, content=code_result)
        # Team.all_messages.append(code_msg)
        self.own_message = code_msg
        return

    def go_in_sample(self):
        print(self.profile + " " + self.name + " Coding...")
        Team.log.info(self.profile + " " + self.name + " Coding...")

        # ---------- get the information needed from SCR ----------
        functional_requirement = self.getPRD().content
        architecture = self.getArchiture().content
        task_plan = self.getProjectPlan().content

        system_prompt = SystemMessage(content=CODING_SYS)
        user_prompt_template = ChatPromptTemplate.from_template(CODING)
        user_prompt_msg = user_prompt_template.invoke(
            {
                "architecture": architecture,
                "task_plan": task_plan,
            }
        )
        user_prompt = user_prompt_msg.to_messages()[0]
        # prompt LLM

        Team.log.info(system_prompt.content + "\n" + user_prompt.content)
        code_result = self.llm_sample.invoke(system_prompt, user_prompt)
        Team.log.info("Generated Code: \n" + code_result)
        # ________ store in self code dict ________
        # Team.log.info("Compare Code")
        # self.compare_code(code_result)
        code_result_split = code_result.split("*** ")
        for i in range(1, len(code_result_split)):
            file_name, file_content = self.match(code_result_split[i])
            self.code_base[file_name] = file_content

        self.message_to_file(code_result)
        code_msg = Message(sender=self.profile, content=code_result)
        # Team.all_messages.append(code_msg)
        self.own_message = code_msg
        return

    def go_in_sample_with_fdback(self, ce_feedback, flag):
        print(self.profile + " " + self.name + " Coding with feedback...")
        Team.log.info(self.profile + " " + self.name + " Coding with feedback...")

        # ---------- get the information needed from SCR ----------
        functional_requirement = self.getPRD().content
        architecture = self.getArchiture().content

        system_prompt = SystemMessage(content=CODING_SYS)

        if flag == "0":
            user_prompt_template = ChatPromptTemplate.from_template(CODING_C)
            user_prompt_msg = user_prompt_template.invoke(
                {
                    "architecture": architecture,
                    "functional_requirements": functional_requirement,
                    "ce_feedback": ce_feedback,
                }
            )
        elif flag == "1":
            exist_code = self.own_message.content
            user_prompt_template = ChatPromptTemplate.from_template(CODING_FD)
            user_prompt_msg = user_prompt_template.invoke(
                {
                    "exist_code": exist_code,
                    "ce_feedback": ce_feedback,
                }
            )

        user_prompt = user_prompt_msg.to_messages()[0]
        # prompt LLM
        Team.log.info(system_prompt.content + "\n" + user_prompt.content)
        code_result = self.llm_sample.invoke(system_prompt, user_prompt)
        Team.log.info("\n" + code_result)
        # ________ store in self code dict ________
        Team.log.info("Compare Code")
        self.compare_code(code_result)
        code_result_split = code_result.split("*** ")
        for i in range(1, len(code_result_split)):
            file_name, file_content = self.match(code_result_split[i])
            self.code_base[file_name] = file_content

        self.message_to_file(code_result)
        code_msg = Message(sender=self.profile, content=code_result)
        Team.all_messages.append(code_msg)
        self.own_message = code_msg

        return

    def store_code_dict(self, code_result):
        code_result_split = code_result.split("*** ")
        for i in range(1, len(code_result_split)):
            file_name, file_content = self.match(code_result_split[i])
            self.code_base[file_name] = file_content

    def read_code_base(self):
        # code could also include other types file, like txt.
        code_sum = ""
        for key, value in self.code_base.items():
            code_sum = code_sum + "file name: " + key + "\n\n" + value + "\n\n"
        return code_sum

    def compare_code(self, code_result):
        # add code files generated by LLM to programmer's codebase
        code_result_split = code_result.split("*** ")
        differ = difflib.Differ()
        for i in range(1, len(code_result_split)):
            file_name, file_content = self.match(code_result_split[i])
            update_codes_content = "**[Update Codes]**\n\n"
            update_codes_content += "{} updated.\n".format(file_name)
            # create only if name part is not empty, to handle occasional errors with the regular expression
            if file_name:
                old_file_content = (
                    self.code_base[file_name]
                    if file_name in self.code_base.keys()
                    else "# None"
                )
            lines_old = old_file_content.splitlines()
            lines_new = file_content.splitlines()

            unified_diff = difflib.unified_diff(
                lines_old, lines_new, lineterm="", fromfile="Old", tofile="New"
            )
            unified_diff = "\n".join(unified_diff)
            update_codes_content = (
                update_codes_content
                + "\n\n"
                + """```
'''

'''\n"""
                + unified_diff
                + "\n```"
            )
            Team.log.info(update_codes_content)

    def match(self, code_text):
        """
        accept a string that has been split by ***_ (where _ represents a space).
        main.py
        ```python
        code...
        ```
        following this format, extract the name and strings separately.
        """
        pattern = r"(.*?)```"
        match = re.search(pattern, code_text, re.DOTALL)

        if match:
            before_code_block = match.group(1).strip()
        else:
            return "", ""

        # extract code
        code_pattern = r"```(?:\w+)?(.*?)(?:```|$)"
        code_match = re.search(code_pattern, code_text, re.DOTALL)

        if code_match:
            code_block = code_match.group(1).strip()
            return before_code_block, code_block
        else:
            return "", ""

    def write_adapator(self, file_dict):
        """
        will be removed in futurn
        """
        result = ""
        for key, value in file_dict.items():
            result = result + "*** " + key + "\n```placeholder\n" + value + "\n```\n\n"
        return result

    def message_to_file(self, code_text):
        if not os.path.exists(os.path.join(Team.project_dir, "code")):
            # makedir_s, recursely create folders
            os.makedirs(os.path.join(Team.project_dir, "code"))
        code_base_dir = os.path.join(Team.project_dir, "code")
        # split based on ***_
        code_text_split = code_text.split("*** ")

        for i in range(1, len(code_text_split)):
            name, code = self.match(code_text_split[i])
            # create only if name part is not empty, to handle occasional errors with the regular expression
            if name:
                # if name contains a directory, create it
                file_relative_directory = os.path.dirname(name)
                code_dir = os.path.join(code_base_dir, file_relative_directory)
                if not os.path.exists(code_dir):
                    # makedir_s, recursely create folders
                    os.makedirs(code_dir)
                # writing result to local
                print(self.profile + " writting CODE: " + str(name))
                Team.log.info(self.profile + " writting CODE: " + str(name))
                super().save_file_overwrite(
                    os.path.join(code_base_dir, str(name)), str(code)
                )
        Team.log.info(" " + str(code_base_dir))
        Team.log.info(" ")
        add_newline_to_txt_files(code_base_dir)

    def message_to_file_review(self, code_text):
        os.makedirs(Team.project_dir + "review_code")
        code_base_dir = Team.project_dir + "review_code/"
        # split based on ###_
        code_text_split = code_text.split("### ")

        for i in range(1, len(code_text_split)):
            name, code = self.match(code_text_split[i])
            # create only if name part is not empty, to handle occasional errors with the regular expression
            if name:
                # if name contains a directory, create it
                file_relative_directory = os.path.dirname(name)
                code_dir = code_base_dir + file_relative_directory
                if not os.path.exists(code_dir):
                    # makedir_s, recursely create folders
                    os.makedirs(code_dir)
                # writing result to local
                print(self.profile + " Rewritting CODE: " + str(name))
                Team.log.info(self.profile + " Rewritting CODE: " + str(name))
                super().save_file_overwrite(code_base_dir + str(name), str(code))

    def message_to_file_test(self, code_text):
        if not os.path.exists(os.path.join(Team.project_dir, "test_code")):
            # makedir_s, recursely create folders
            os.makedirs(os.path.join(Team.project_dir, "test_code"))
        code_base_dir = os.path.join(Team.project_dir, "test_code")
        # split based on ***_
        code_text_split = code_text.split("*** ")

        for i in range(1, len(code_text_split)):
            name, code = self.match(code_text_split[i])
            # create only if name part is not empty, to handle occasional errors with the regular expression
            if name:
                # if name contains a directory, create it
                file_relative_directory = os.path.dirname(name)
                code_dir = os.path.join(code_base_dir, file_relative_directory)
                if not os.path.exists(code_dir):
                    # makedir_s, recursely create folders
                    os.makedirs(code_dir)
                # writing result to local
                print(self.profile + " writting Testing CODE: " + str(name))
                Team.log.info(self.profile + " writting Testing CODE: " + str(name))
                super().save_file_overwrite(
                    os.path.join(code_base_dir, str(name)), str(code)
                )
        add_newline_to_txt_files(code_base_dir)

    def update_own_message(self, msg: Message):
        self.own_message = msg
        Team.all_messages[4] = msg

    # programmer won't add self's message, no need to filter messages;
    def read_msg(self, messages):
        result = ""
        for msg in messages:
            result = (
                result
                + "# "
                + msg.sender
                + " - "
                + self.team.roles[msg.sender].action
                + "\n"
                + msg.content
                + "\n"
            )
        return result

    def read_suggestion(self, suggestion):
        # accept a Message List
        # return a more friendly result(String type)
        # User's review: xxx, User's review xxx
        result = ""
        for msg in suggestion:
            result = (
                result + "[ " + msg.sender + "'s code review: " + msg.content + " ]\n"
            )
        return result

    def getOriginalDescription(self):
        return Team.all_messages[0]

    def getPRD(self):
        return Team.all_messages[1]

    def getArchiture(self):
        return Team.all_messages[2]

    def getProjectPlan(self):
        return Team.all_messages[3]

    def go_inter(self):
        pass

    def read_counter(self):
        # input counter example path
        counter_path = Path(
            "D:\\02-Project\\02-Align\models\RTADev\Altdev\project\website\RecipeHub_20241220151721 counter"
        )
        counter_codes_path = [
            "review_code/templates/browse_recipes.html",
            "review_code/recipe_manager.py",
        ]
        counter_codes = ""
        for ccp in counter_codes_path:
            counter_codes += ccp.split("/")[-1]
            counter_codes += read_file_2_line(counter_path / Path(ccp))
            counter_codes += "\n"

        counter_reason_path = counter_path / "counter_reason.txt"
        counter_reason = read_file_2_line(counter_reason_path)

        return counter_reason, counter_codes
