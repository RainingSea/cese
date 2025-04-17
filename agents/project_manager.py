import os
from pathlib import Path

# langchain lib
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

# custom lib
from prompt.write_plan_prompt_new import (
    WRITE_PLAN_SYS,
    WRITE_PLAN,
    WRITE_PLAN_WITH_FDBACK,
    WRITE_PLAN_FORMAT,
    WRITE_PLAN_PROMPT,
)
from prompt.meta_prompt import META_PROMPT

from agents.role import Role
from agents.team import Team
from messages.message import Message

from utils.read import read_file_2_line


class Project_Manager(Role):
    name: str = "Tsunoda"
    profile: str = "Project Manager"
    llm: object
    llm_sample: object
    system_msg: str = WRITE_PLAN_SYS
    own_message: Message = None
    team: Team = None

    action: str = "Task Plan"

    def go(self):
        pass

    def go_in_sample(self):
        # ---------- log info --------
        print(self.profile + " " + self.name + " generate Project Plan......")
        Team.log.info(self.profile + " " + self.name + " generate Project PLAN......")

        # ---------- get the information needed from SCR ----------
        functional_requirement = self.getPRD().content
        architect = self.getSystemModule().content

        # ---------- use metaprompt to let LLM write prompt to generate PRD
        meta_prompt_tplt = ChatPromptTemplate.from_template(
            WRITE_PLAN_FORMAT + META_PROMPT
        )
        # define the role_input and role_output
        meta_prompt_prompt = meta_prompt_tplt.invoke(
            {
                "functional_requirement": functional_requirement,
                "software_architecture": architect,
                "role_output": "task plan",
            }
        )

        meta_prompt_msg = meta_prompt_prompt.to_messages()[0]
        prompt_instruction = self.llm.invoke(meta_prompt_msg)

        # ---------- constructing prompt to LLM ----------
        # using message template from LangChain, the result is SYS Message & HUMAN Message.
        system_prompt = SystemMessage(content=WRITE_PLAN_SYS)
        user_prompt_template = ChatPromptTemplate.from_template(WRITE_PLAN_PROMPT)
        user_prompt_msg = user_prompt_template.invoke(
            {
                "functional_requirement": functional_requirement,
                "software_architecture": architect,
                "instruction": prompt_instruction,
            }
        )
        user_prompt = user_prompt_msg.to_messages()[0]
        Team.log.info(
            "\n\nPrompt to generate task plan is: \n"
            + system_prompt.content
            + "\n"
            + user_prompt.content
        )
        # prompt LLM
        result = self.llm.invoke(system_prompt, user_prompt)

        # ---------- logging --------
        Team.log.info(self.profile + " " + self.name)
        Team.log.info("generated task plan:\n" + result)

        # ---------- adding result to SCR(before align) ----------
        plan_msg = Message(sender=self.profile, content=result)
        self.own_message = plan_msg

        self.update_scr(plan_msg)
        # ---------- writing result to local ----------
        self.message_to_file(plan_msg.content)

        return

    # def go_in_sample(self):
    #     print(
    #         self.profile
    #         + " "
    #         + self.name
    #         + " generate Project PLAN variable temperature"
    #     )
    #     Team.log.info(
    #         self.profile
    #         + " "
    #         + self.name
    #         + " generate Project PLAN variable temperature"
    #     )

    #     # ---------- get the information needed from SCR ----------
    #     functional_requirement = self.getPRD().content
    #     architect = self.getSystemModule().content

    #     # ---------- constructing prompt to LLM ----------
    #     # using message template from LangChain, the result is SYS Message & HUMAN Message.
    #     system_prompt = SystemMessage(content=WRITE_PLAN_SYS)
    #     user_prompt_template = ChatPromptTemplate.from_template(WRITE_PLAN)
    #     user_prompt_msg = user_prompt_template.invoke(
    #         {
    #             "functional_requirement": functional_requirement,
    #             "architecture": architect,
    #         }
    #     )
    #     user_prompt = user_prompt_msg.to_messages()[0]
    #     Team.log.info(system_prompt.content + "\n" + user_prompt.content)
    #     # prompt LLM
    #     result = self.llm_sample.invoke(system_prompt, user_prompt)

    #     # ---------- logging --------
    #     Team.log.info(self.profile + " " + self.name)
    #     Team.log.info(result)

    #     # ---------- adding result to SCR(before align) ----------
    #     plan_msg = Message(sender=self.profile, content=result)
    #     self.own_message = plan_msg

    #     self.update_scr(plan_msg)
    #     # ---------- writing result to local ----------
    #     self.message_to_file(plan_msg.content)

    #     return

    def go_with_fdback(self, feedback):
        print(self.profile + " " + self.name + " generate Project PLAN with feedback")
        Team.log.info(
            self.profile + " " + self.name + " generate Project PLAN with feedback"
        )

        # ---------- get the information needed from SCR ----------
        functional_requirement = self.getPRD().content
        architect = self.getSystemModule().content

        # ---------- constructing prompt to LLM ----------
        # using message template from LangChain, the result is SYS Message & HUMAN Message.
        system_prompt = SystemMessage(content=WRITE_PLAN_SYS)
        user_prompt_template = ChatPromptTemplate.from_template(WRITE_PLAN_WITH_FDBACK)
        user_prompt_msg = user_prompt_template.invoke(
            {
                "functional_requirement": functional_requirement,
                "architecture": architect,
                "ce_feedback": feedback,
            }
        )
        user_prompt = user_prompt_msg.to_messages()[0]
        Team.log.info(system_prompt.content + "\n" + user_prompt.content)
        # prompt LLM
        result = self.llm.invoke(system_prompt, user_prompt)

        # ---------- logging --------
        Team.log.info(self.profile + " " + self.name)
        Team.log.info(result)

        # ---------- adding result to SCR(before align) ----------
        plan_msg = Message(sender=self.profile, content=result)
        self.own_message = plan_msg

        self.update_scr(plan_msg)
        # ---------- writing result to local ----------
        self.message_to_file(plan_msg.content)

        return

    def go_in_sample_with_fdback(self, feedback):
        print(self.profile + " " + self.name + " generate Project PLAN with feedback")
        Team.log.info(
            self.profile + " " + self.name + " generate Project PLAN with feedback"
        )

        # ---------- get the information needed from SCR ----------
        functional_requirement = self.getPRD().content
        architect = self.getSystemModule().content

        # ---------- constructing prompt to LLM ----------
        # using message template from LangChain, the result is SYS Message & HUMAN Message.
        system_prompt = SystemMessage(content=WRITE_PLAN_SYS)
        user_prompt_template = ChatPromptTemplate.from_template(WRITE_PLAN_WITH_FDBACK)
        user_prompt_msg = user_prompt_template.invoke(
            {
                "functional_requirement": functional_requirement,
                "architecture": architect,
                "ce_feedback": feedback,
            }
        )
        user_prompt = user_prompt_msg.to_messages()[0]
        Team.log.info(system_prompt.content + "\n" + user_prompt.content)
        # prompt LLM
        result = self.llm_sample.invoke(system_prompt, user_prompt)

        # ---------- logging --------
        Team.log.info(self.profile + " " + self.name)
        Team.log.info(result)

        # ---------- adding result to SCR(before align) ----------
        plan_msg = Message(sender=self.profile, content=result)
        self.own_message = plan_msg

        self.update_scr(plan_msg)
        # ---------- writing result to local ----------
        self.message_to_file(plan_msg.content)

        return

    def update_scr(self, message):
        """
        update team's shared certificated repository, with generated architecture
        """
        if len(Team.all_messages) < 4:
            # indicate that no new architecture
            Team.all_messages.append(message)
        else:
            # the other teams document
            Team.log.info("already a task plan, replace it")
            Team.all_messages[3] = message

    def update_own_message(self, msg: Message):
        self.own_message = msg
        Team.all_messages[3] = msg

    def message_to_file(self, msg_content):
        # ---------- writing Code Plan(Task Plan) to local ----------
        file_name = "task plan.md"

        Team.log.info(self.profile + " writting TASK PLAN")
        super().save_file_overwrite(
            os.path.join(Team.project_dir, file_name), msg_content
        )

    def getOriginRequirement(self):
        return Team.all_messages[0]

    def getPRD(self):
        return Team.all_messages[1]

    def getSystemModule(self):
        return Team.all_messages[2]

    def go_inter(self):
        # 从项目dir里读取，并且加到自己的
        print(self.profile + " " + self.name + " extracting Plan......")
        Team.log.info(self.profile + " " + self.name + " extracting Plan......")
        result = read_file_2_line(Path(Team.incremental_base_dir) / "task plan.md")
        if not os.path.exists(os.path.join(Team.project_dir, "task plan.md")):
            self.message_to_file(result)
        module_msg = Message(sender=self.profile, content=result)
        self.own_message = module_msg
        if len(Team.all_messages) <= 3:
            Team.all_messages.append(module_msg)
        else:
            Team.all_messages[3] = module_msg
