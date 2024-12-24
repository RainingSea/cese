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


class Team(BaseModel):
    # team name
    team_name: str = "SES midnigt wanderer"
    # team roles
    roles: dict[str, Role] = Field(default_factory=dict, validate_default=True)
    # team roles --- string format (use in specific scenarios)
    str_roles: str = ""

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
    project_dir: ClassVar[str] = ""
    incremental_base_dir: ClassVar[str] = ""
    active_roles: ClassVar[list[str]] = []
    cost: ClassVar[int] = 0

    def run(self):
        inter_launch = True
        # inter_launch = False
        if inter_launch:
            # 读取已有项目中的文件，然后开发，go_inter()代表读取已有文件作为角色在工作流中的信息
            Team.incremental_base_dir = os.path.normpath(
                "D:\\02-Project\\02-Align\models\RTADev\Altdev\project\game\\2048_20241223154030"
            )

            self.roles["Product Manager"].go_inter()
            self.roles["Architect"].go_inter()
            self.roles["Project Manager"].go_inter()
            
            # ceaug()

            # self.roles["C_Programmer"].c_go()
            self.roles["C_Programmer"].go()
            # self.roles["Programmer"].go()

        else:
            self.roles["Product Manager"].go()
            Team.active_role(self.roles["Product Manager"].profile)

            self.roles["Architect"].go()
            self.roles["Reviewer"].target = self.roles["Architect"]
            self.roles["Reviewer"].go()
            Team.active_role(self.roles["Architect"].profile)

            self.roles["Project Manager"].go()
            self.roles["Reviewer"].target = self.roles["Project Manager"]
            self.roles["Reviewer"].go()
            Team.active_role(self.roles["Project Manager"].profile)

            self.roles["Programmer"].go()
            # self.roles["Reviewer"].target = self.roles["Project Manager"]
            # self.roles["Reviewer"].go()
            Team.active_role(self.roles["Programmer"].profile)

            # self.roles["Code Tester"].go()
            Team.active_role(self.roles["Code Tester"].profile)

        print("Dev execute END")

    @classmethod
    def set_projdir(cls, projdir: str):
        Team.project_dir = projdir
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
