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
from ceaug.ceaug_main import ceaug, create_ce_document
from utils.edit_txt import add_newline_to_txt_files, update_flask_port


class Team(BaseModel):
    # team name
    team_name: str = "SES midnigt wanderer"
    # team roles
    roles: dict[str, Role] = Field(default_factory=dict, validate_default=True)
    # team roles --- string format (use in specific scenarios)
    str_roles: str = ""

    projec_catogory: str = ""
    project_name: str = ""
    # origin requirement from user
    origin_requirement: str = ""

    # the number of align checking
    align_check_num: ClassVar[int] = 2
    # the number of mad
    mad_num: ClassVar[int] = 1

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

        self.roles["Programmer"].go()
        code_base_dir = os.path.join(Team.project_dir, "code")
        port = update_flask_port(os.path.join(code_base_dir, "main.py"), "")

        for j in range(2):
            # set code dir
            ce_projects_paths = [Team.project_dir]
            # execute unit test
            ce_score, ce_feedback = ceaug(
                previous_work_dir,
                ce_projects_paths,
                Team.projec_catogory,
                Team.project_name,
                Team.all_messages[0].content,
                Team.log,
            )
            # use feedback to regenate
            # self.roles["C_Programmer"].go(ce_feedback)
            if ce_feedback == "CodeIsGood":
                return
            else:
                print(ce_feedback)
                self.roles["Code Tester"].unit_test_feedback = ce_feedback
                self.roles["Code Tester"].go()
                port = update_flask_port(
                    os.path.join(code_base_dir, "main.py"), str(port)
                )

        return

    def run(self):
        previous_work_dir = Path.cwd()
        pervious_project_dir = Team.project_dir

        # inter_launch = True
        inter_launch = False

        # _______________ generate PRD, Architect, Task Plan _______________
        if inter_launch:
            # Read files from an existing project, then proceed with development.
            # go_inter() represents reading existing files to serve as artifacts for roles in the workflow.
            Team.incremental_base_dir = os.path.normpath(
                "D:\Project\CE\CE\project\website\\NoteTakingApp"
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

        # |--------- simplest coding process ---------|
        # |
        # self.roles["Programmer"].go()
        # return
        # |
        # |--------- simplest coding process ---------|
        # set code dir
        ce_projects_paths = create_ce_document(
            Team.project_dir, Team.all_messages[3].content, Team.log
        )

        for j in range(len(ce_projects_paths)):
            print(f"\ngenerate the code of {j}th counter project\n")
            Team.incremental_base_dir = os.path.normpath(ce_projects_paths[j])
            self.roles["Product Manager"].go_inter()
            self.roles["Architect"].go_inter()
            self.roles["Project Manager"].go_inter()
            # temporarily change project dir to a ce folder
            Team.project_dir = ce_projects_paths[j]
            self.roles["Programmer"].go()
            code_base_dir = os.path.join(Team.project_dir, "code")
            port = update_flask_port(os.path.join(code_base_dir, "main.py"), "")

        # execute unit test
        ce_score, ce_feedback = ceaug(
            previous_work_dir,
            ce_projects_paths,
            Team.projec_catogory,
            Team.project_name,
            Team.all_messages[0].content,
            Team.log,
        )
        # use feedback to regenate
        # self.roles["C_Programmer"].go(ce_feedback)
        # pass all the ce_project, execute unit test, analyze, and select the most valuable one
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

        self.roles["Product Manager"].go_inter()
        self.roles["Architect"].go_inter()
        self.roles["Project Manager"].go_inter()
        if ce_feedback:
            if ce_feedback == "CodeIsGood":
                print("Dev execute END")
                return
            # ceaug finally return the most valuable(temporarily is 1 case) project issues feedback
            Team.log.info("### ceaug feedback\n" + str(ce_feedback))
            # use feedback from counter example to augment coding
            Team.log.info("begin CE Coding")
            # C_programmer temperature is 0.2
            self.roles["C_Programmer"].go(ce_feedback)
        else:
            Team.log.info("No CE, Normal Coding")
            self.roles["Programmer"].code_base.clear()
            self.roles["Programmer"].go()

        code_base_dir = os.path.join(Team.project_dir, "code")
        port = update_flask_port(os.path.join(code_base_dir, "main.py"), "")

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
