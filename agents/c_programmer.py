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
from utils.read import read_dir

# custom lib
from prompt.write_code_prompt import (
    CODING_SYS,
    CODING,
    CODING_C,
    CODING_P,
    RECODNIG,
)

from prompt.align_prompt import RETHINK, COMPLEMENT, ALIGN_WITH_WHO
from agents.role import Role
from agents.team import Team
from agents.searcher import Searcher
from messages.message import Message
from utils.read import read_file_2_line
from utils.edit_txt import add_newline_to_txt_files
from utils.edit_txt import update_flask_port


class C_Programmer(Role):
    name: str = "Clorinde"
    profile: str = "C_Programmer"
    llm: object
    llm_review: object
    system_msg: str = CODING_SYS
    own_message: Message = None
    team: Team = None
    # all_code_files: dict[str, list] = Field(default_factory=dict, validate_default=True)
    action: str = "Code"
    code_base: dict[str, str] = Field(default_factory=dict, validate_default=True)
    trigger_task: str = "T7"

    def go(self, ce_feedback):
        print(self.trigger_task)
        print(self.profile + " " + self.name + " Coding...")
        Team.log.info(self.profile + " " + self.name + " Coding...")

        # ---------- get the information needed from SCR ----------
        architecture = self.getArchiture().content
        task_plan = self.getProjectPlan().content

        # --------------- decompose and assign tasks to programmer

        # task_dict = self.task_list_extract()

        # --------------- get counter info -----------------
        # counter_reason, counter_code = self.read_counter()
        # ---------- constructing prompt to LLM ----------
        system_prompt = SystemMessage(content=CODING_SYS)
        # use counter prompt
        user_prompt_template = ChatPromptTemplate.from_template(CODING_C)
        user_prompt_msg = user_prompt_template.invoke(
            {
                "architecture": architecture,
                "task_plan": task_plan,
                "ce_feedback": ce_feedback,
            }
        )
        user_prompt = user_prompt_msg.to_messages()[0]
        # prompt LLM
        Team.log.info(system_prompt.content + "\n" + user_prompt.content)
        code_result = self.llm.invoke(system_prompt, user_prompt)
        Team.log.info("\n" + code_result)

        self.message_to_file(code_result)

        code_msg = Message(sender=self.profile, content=code_result)

        # Team.all_messages.append(code_msg)

    # def go():

    #     # --------------- get counter info -----------------
    #     counter_reason, counter_code = self.read_counter()
    #     # ---------- constructing prompt to LLM ----------
    #     system_prompt = SystemMessage(content=CODING_SYS)
    #     user_prompt_template = ChatPromptTemplate.from_template(CODING_C)
    #     user_prompt_msg = user_prompt_template.invoke(
    #         {
    #             "architecture": architecture,
    #             "task_plan": task_plan,
    #             "counter_reason": counter_reason,
    #             "counter_code": counter_code,
    #         }
    #     )
    #     user_prompt = user_prompt_msg.to_messages()[0]

    #     # prompt LLM
    #     Team.log.info(system_prompt.content + "\n" + user_prompt.content)
    #     code_result = self.llm.invoke(system_prompt, user_prompt)
    #     # ---------- logging --------
    #     Team.log.info("\n" + code_result)

    #     # ---------- writing result to local ----------
    #     # this is code before align
    #     self.message_to_file(code_result)

    #     align_TF = False
    #     review_code_result = ""

    #     # align for code
    #     align_TF, review_code_result = self.execute_and_feedback(
    #         architecture, task_plan, code_result
    #     )

    #     Team.log.info("is Align? : " + str(align_TF))

    #     # ---------- adding result to SCR(before align) ----------
    #     if align_TF == False:
    #         # if no problem
    #         code_msg = Message(sender=self.profile, content=code_result)
    #         # self.message_to_file(code_msg.content)
    #         Team.all_messages.append(code_msg)
    #     else:
    #         # if misalign happens and modify codes
    #         code_msg = Message(sender=self.profile, content=review_code_result)
    #         # self.message_to_file(code_msg.content)
    #         self.message_to_file_review(review_code_result)
    #         Team.all_messages.append(code_msg)

    #     self.own_message = code_msg

    # align process for code

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

    def execute_and_feedback(self, architecture, task_plan, raw_codes):

        Team.log.info("Begin Check for Programmer")

        align_result = raw_codes

        all_roles = Team.get_active_roles()

        Team.log.info("role involved in Code Alignment Checking: " + str(all_roles))

        # ------------ check roles to align ----------------
        print("[1] Roles go to Check")
        Team.log.info("[1] Roles go to Check")

        align_talk_turn = 1
        MAX_ALIGN_TURN = Team.align_check_num

        while align_talk_turn <= MAX_ALIGN_TURN:

            align_roles = []
            code_check_msg = []

            print("Begin the " + str(align_talk_turn) + " turn Alignment")
            Team.log.info("Begin the " + str(align_talk_turn) + " turn Alignment")
            # roles participating in the alignment to align check
            for i in range(len(all_roles)):
                align_participant_msg = (
                    ChatPromptTemplate.from_template(
                        self.team.roles[all_roles[i]].review_prompt["Programmer"]
                    )
                    .invoke(
                        {
                            "participant_content": self.team.roles[
                                all_roles[i]
                            ].own_message.content,
                            "role_content": align_result,
                        }
                    )
                    .to_messages()[0]
                )
                # align prompt
                Team.log.info(
                    self.team.roles[all_roles[i]].profile
                    + " Code Alignment prompt: "
                    + align_participant_msg.content
                )
                # record align check result
                participant_check = self.team.roles[all_roles[i]].llm.invoke(
                    align_participant_msg
                )
                print(
                    "Code Alignment | "
                    + self.team.roles[all_roles[i]].profile
                    + " | check result is : \n"
                    + participant_check
                )
                Team.log.info(
                    "Code Alignment | "
                    + self.team.roles[all_roles[i]].profile
                    + " | check result is : \n"
                    + participant_check
                )

                participant_check_msg = Message(
                    sender=self.team.roles[all_roles[i]].profile,
                    content=participant_check,
                )
                # role reporting problem will be list in align roles, participant in MAD process
                if "[NOTMATCH]" in participant_check:
                    align_roles.append(self.team.roles[all_roles[i]].profile)
                    code_check_msg.append(participant_check_msg)
                elif "[MATCH]" in participant_check:
                    pass
                else:
                    align_roles.append(self.team.roles[all_roles[i]].profile)
                    code_check_msg.append(participant_check_msg)

            # After Check, We get { align_roles & check_result }
            print("After Checking, Group Roles are: " + str(align_roles))
            Team.log.info("After Checking, Group Roles are: " + str(align_roles))

            # [1] if all roles no problem, align finished
            if len(align_roles) == 0:
                if align_talk_turn == 1:
                    # if all roles check result is GOOD, then return
                    Team.log.info("All roles no problem in Checking, No Align")
                    return False, align_result
                else:
                    Team.log.info(
                        "After Align, All roles no problem in Checking, No Align"
                    )
                    return True, align_result

            # [2] at least one role misalign, enter MAD-S / MAD-M

            sup_turn = 1
            MAX_SUP_TURN = Team.mad_num

            raw_complement_suggestion = []
            for _r in code_check_msg:
                raw_complement_suggestion.append(_r)

            # ---------- MAD ----------
            while sup_turn <= MAX_SUP_TURN:
                print("\nBegin the " + str(sup_turn) + " turn Supplement(MAD) ")
                Team.log.info("\nBegin the " + str(sup_turn) + " turn Supplement(MAD) ")
                # MAD-S / MAD-M
                # whether to supplement role's own messages based on messages from other roles.
                Team.log.info("### SUPPLEMENTING STAGE ###")

                # MAD-S / special case where there is only one role
                if len(align_roles) <= 1:
                    Team.log.info("Only one roles in Align, no MAD")
                    break
                # MAD-M
                else:
                    _raw_complement_suggestion = []
                    for j in range(len(align_roles)):
                        # extract other's message
                        other_suggestion = []
                        self_suggestion = None
                        for msg in raw_complement_suggestion:
                            if msg.sender != self.team.roles[align_roles[j]].profile:
                                other_suggestion.append(msg)
                            else:
                                self_suggestion = msg

                        # supplement one's own check result based on others' check result
                        complement_align_participant_msg = (
                            ChatPromptTemplate.from_template(COMPLEMENT)
                            .invoke(
                                {
                                    "participant_role": self.team.roles[
                                        align_roles[j]
                                    ].profile,
                                    "role_action": self.action,
                                    "participant_action": self.team.roles[
                                        align_roles[j]
                                    ].action,
                                    "participant_content": self.team.roles[
                                        align_roles[j]
                                    ].own_message.content,
                                    "role_content": align_result,
                                    "participant_review": self_suggestion.content,
                                    "other_review": self.read_suggestion(
                                        other_suggestion
                                    ),
                                }
                            )
                            .to_messages()[0]
                        )
                        # supplement prompt
                        Team.log.info(
                            self.team.roles[align_roles[j]].profile
                            + " complement self's review result prompt\n"
                            + complement_align_participant_msg.content
                        )
                        # record supplement thinking result
                        complement_align_participant_suggestion = self.team.roles[
                            align_roles[j]
                        ].llm.invoke(complement_align_participant_msg)
                        print(
                            align_roles[j]
                            + " SUP: "
                            + complement_align_participant_suggestion
                        )
                        Team.log.info(
                            "complement result is \n"
                            + complement_align_participant_suggestion
                        )

                        # Since the result is not necessarily a complement suggestion, use a temp_review.
                        # This way, the SUMMARY doesn’t need to be written twice.
                        if "[NOT_NEED]" in complement_align_participant_suggestion:
                            _temp_review = self_suggestion
                        else:
                            _temp_review = Message(
                                sender=self.team.roles[align_roles[j]].profile,
                                content=complement_align_participant_suggestion,
                            )
                        _raw_complement_suggestion.append(_temp_review)
                    raw_complement_suggestion = []
                    for _r in _raw_complement_suggestion:
                        raw_complement_suggestion.append(_r)
                    sup_turn = sup_turn + 1

            flag_suggestion = []
            complement_suggestion = []
            # complement_suggestion_string = ""
            for i in range(len(raw_complement_suggestion)):
                if "[NOTMATCH]" in raw_complement_suggestion[i].content:
                    flag_suggestion.append("BAD")
                    complement_suggestion.append(raw_complement_suggestion[i])
                elif "[MATCH]" in raw_complement_suggestion[i].content:
                    flag_suggestion.append("GOOD")
                else:
                    flag_suggestion.append("BAD")
                    complement_suggestion.append(raw_complement_suggestion[i])

            # ---------- MASTER or CODE decide whether to approve it. ----------
            # Logically, if roles reache this step, it means all NOTMATCH, so they should not pass.
            # will correct here after releasing.
            Team.log.info("flag " + str(flag_suggestion))
            PASS = True
            for i in range(len(flag_suggestion)):
                if flag_suggestion[i] != "GOOD":
                    PASS = False
                    break

            # decide whether to modify or end the alignment based on the results from the Agents (which may include humans).
            if PASS == False:
                align_TF = True
                # extract the not align check result
                user_prompt_template_1 = ChatPromptTemplate.from_template(RETHINK)
                code_review_user_msg_1 = user_prompt_template_1.invoke(
                    {"result": self.read_suggestion(complement_suggestion)}
                )
                code_review_user_prompt_1 = code_review_user_msg_1.to_messages()[0]
                Team.log.info(
                    "prompt to Extract Code Review: "
                    + code_review_user_prompt_1.content
                )
                p_result = self.llm.invoke(code_review_user_prompt_1)
                Team.log.info("Code Review Extract Result: " + p_result)
                print(self.profile + " " + self.name + " Recoding...")
                Team.log.info(self.profile + " " + self.name + " Recoding...")
                # system_prompt = SystemMessage(content=RECODING_SYS)
                user_prompt_template = ChatPromptTemplate.from_template(RECODNIG)
                code_review_user_msg = user_prompt_template.invoke(
                    {
                        "review_result": p_result,
                        "code": align_result,
                    }
                )
                code_review_user_prompt = code_review_user_msg.to_messages()[0]
                # prompt LLM and regenerate aligned result
                Team.log.info(code_review_user_prompt.content)
                recode_result = self.llm.invoke(
                    code_review_user_prompt,
                )
                Team.log.info("Regenerated Code is: \n" + recode_result)
                align_result = recode_result
                align_talk_turn = align_talk_turn + 1
            else:
                pass
                # print("all Align, alignment finished")
                # Team.log.info("Everyone Reaches an agreement, Align is Done")
                # if align_talk_turn == 1:
                #     align_TF = False
                #     return align_TF, align_result
                # else:
                #     align_TF = True
                #     return align_TF, align_result

        # Code — no consistent result is reached after MAX align, force return.
        Team.log.info("Align is upon MAX, return")
        return True, align_result

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

        add_newline_to_txt_files(code_base_dir)
        # update_flask_port(os.path.join(code_base_dir, "main.py"))

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
        if not os.path.exists(Team.project_dir + "test_code"):
            os.makedirs(Team.project_dir + "test_code")
        # split based on ###_
        code_base_dir = Team.project_dir + "test_code/"
        code_text_split = code_text.split("*** ")

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
                print(self.profile + " writting Test CODE: " + str(name))
                Team.log.info(self.profile + " writting Test CODE: " + str(name))
                super().save_file_overwrite(code_base_dir + str(name), str(code))

        add_newline_to_txt_files(code_base_dir)
        update_flask_port(os.path.join(code_base_dir, "main.py"))

    def update_own_message(self, msg: Message):
        self.own_message = msg
        Team.all_messages[4] = msg

    def get_align_roles(self, self_content):
        Team.log.info("Team's Active roles: " + Team.active_roles)
        # if not the first role
        if Team.active_roles:
            system_prompt = SystemMessage(
                content="You are a good software engineering expert"
            )
            user_prompt_template = ChatPromptTemplate.from_template(ALIGN_WITH_WHO)
            user_prompt_msg = user_prompt_template.invoke(
                {
                    "role": self.profile,
                    "other_rule_content": self.read_msg(Team.all_messages[1:]),
                    "role_action": self.action,
                    "role_content": self_content,
                    "roles_list": Team.active_roles,
                }
            )
            user_prompt = user_prompt_msg.to_messages()[0]
            Team.log.info("search Align roles's prompt: " + user_prompt.content)
            align_roles_llm_result = self.llm.invoke(system_prompt, user_prompt)
            Team.log.info(
                "LLM think Alignment Group Members: " + align_roles_llm_result
            )
            dict_obj = json.loads(align_roles_llm_result)
            print("Format Group Members: " + str(dict_obj["roles"]))

            roles_list = dict_obj["roles"]
            return roles_list
        else:
            return "HUMAN"

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

    def task_list_extract(self):
        task_plan = self.getProjectPlan().content
        task_dict = ast.literal_eval(task_plan)
        task_list_content = task_dict["Task list"]
        # print(task_list_content)
        print("Task Dictionary:")
        _log_task = ""
        for key, value in task_list_content.items():
            print(f"Key: {key}, Value: {value}")
            _log_task = _log_task + f"Key: {key}, Value: {value}" + "\n"
        Team.log.info("Task Dictionary:\n" + _log_task)
        return task_list_content
