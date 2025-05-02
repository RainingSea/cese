import os
from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage

from prompt.write_architect_prompt import (
    WRITE_ARCHITECT_SYS,
    WRITE_ARCHITECT,
    WRITE_ARCHITECT_WITH_FDBACK,
    WRITE_ARCHITECT_FORMAT,
    WRITE_ARCHITECT_PROMPT,
    WRITE_ARCHITECT_WITH_FDBACK_META,
)
from prompt.meta_prompt import META_PROMPT

from agents.role import Role
from agents.team import Team
from messages.message import Message


from utils.read import read_file_2_line


class Architect(Role):
    name: str = "Arnold"
    profile: str = "Architect"
    llm: object
    llm_sample: object
    system_msg: str = WRITE_ARCHITECT_SYS
    own_message: Message = None
    team: Team = None
    action: str = "Architecture"

    def go_in_sample(self):
        # ---------- log info --------
        print(self.profile + " " + self.name + " generate Architecture......")
        Team.log.info(" ")
        Team.log.info(self.profile + " " + self.name + " Writing Architecture...")

        # ---------- get the information needed from SCR ----------
        original_requirement = self.getOriginRequirement().content
        functional_requirement = self.getPRD().content

        # ---------- use metaprompt to let LLM write instruction
        meta_prompt_tplt = ChatPromptTemplate.from_template(
            WRITE_ARCHITECT_FORMAT + META_PROMPT
        )

        meta_prompt_prompt = meta_prompt_tplt.invoke(
            {
                "original_requirement": original_requirement,
                "functional_requirement": functional_requirement,
                "role_output": "Software Architecture Analysis",
            }
        )
        meta_prompt_msg = meta_prompt_prompt.to_messages()[0]
        # Team.log.info("\n<Architect Instruction>" + meta_prompt_msg.content)
        prompt_instruction = self.llm_sample.invoke(meta_prompt_msg)

        # ---------- constructing prompt to LLM ----------
        user_prompt_template = ChatPromptTemplate.from_template(WRITE_ARCHITECT_PROMPT)
        user_prompt_msg = user_prompt_template.invoke(
            {
                "original_requirement": original_requirement,
                "functional_requirement": functional_requirement,
                "instruction": prompt_instruction,
            }
        )
        user_prompt = user_prompt_msg.to_messages()[0]

        system_prompt = SystemMessage(content=self.system_msg)

        # ---------- prompt LLM ----------
        Team.log.info(
            "Prompt to generate architecture is: \n"
            + system_prompt.content
            + "\n"
            + user_prompt.content
        )
        result = self.llm_sample.invoke(system_prompt, user_prompt)

        # ------------ logging ----------
        Team.log.info(self.profile + " " + self.name)
        Team.log.info("generated architecture:\n" + result)

        # ---------- adding result to SCR(before align) ----------
        module_msg = Message(sender=self.profile, content=result)
        self.own_message = module_msg
        self.update_scr(module_msg)

        # ---------- writing result to local ----------
        self.message_to_file(module_msg.content)

        return

    def go(self):
        # ---------- log info --------
        print(self.profile + " " + self.name + " generate Architecture......")
        Team.log.info(" ")
        Team.log.info(self.profile + " " + self.name + " Writing Architecture...")

        # ---------- get the information needed from SCR ----------
        original_requirement = self.getOriginRequirement().content
        functional_requirement = self.getPRD().content

        # ---------- use metaprompt to let LLM write instruction
        meta_prompt_tplt = ChatPromptTemplate.from_template(
            WRITE_ARCHITECT_FORMAT + META_PROMPT
        )

        meta_prompt_prompt = meta_prompt_tplt.invoke(
            {
                "original_requirement": original_requirement,
                "functional_requirement": functional_requirement,
                "role_output": "Software Architecture Analysis",
            }
        )
        meta_prompt_msg = meta_prompt_prompt.to_messages()[0]
        # Team.log.info("\n<Architect Instruction>" + meta_prompt_msg.content)
        prompt_instruction = self.llm.invoke(meta_prompt_msg)

        # ---------- constructing prompt to LLM ----------
        user_prompt_template = ChatPromptTemplate.from_template(WRITE_ARCHITECT_PROMPT)
        user_prompt_msg = user_prompt_template.invoke(
            {
                "original_requirement": original_requirement,
                "functional_requirement": functional_requirement,
                "instruction": prompt_instruction,
            }
        )
        user_prompt = user_prompt_msg.to_messages()[0]

        system_prompt = SystemMessage(content=self.system_msg)

        # ---------- prompt LLM ----------
        Team.log.info(
            "Prompt to generate architecture is: \n"
            + system_prompt.content
            + "\n"
            + user_prompt.content
        )
        result = self.llm.invoke(system_prompt, user_prompt)

        # ------------ logging ----------
        Team.log.info(self.profile + " " + self.name)
        Team.log.info("generated architecture:\n" + result)

        # ---------- adding result to SCR(before align) ----------
        module_msg = Message(sender=self.profile, content=result)
        self.own_message = module_msg
        self.update_scr(module_msg)

        # ---------- writing result to local ----------
        self.message_to_file(module_msg.content)

        return

    def go_with_fdback(self, feedback):

        # ---------- log info --------
        print(self.profile + " " + self.name + " generate Architecture......")
        Team.log.info(" ")
        Team.log.info(self.profile + " " + self.name + " Writing Architecture...")

        # ---------- get the information needed from SCR ----------
        original_requirement = self.getOriginRequirement().content
        functional_requirement = self.getPRD().content

        # ---------- use metaprompt to let LLM write instruction
        meta_prompt_tplt = ChatPromptTemplate.from_template(
            WRITE_ARCHITECT_FORMAT + META_PROMPT
        )

        meta_prompt_prompt = meta_prompt_tplt.invoke(
            {
                "original_requirement": original_requirement,
                "functional_requirement": functional_requirement,
                "role_output": "Software Architecture Analysis",
            }
        )
        meta_prompt_msg = meta_prompt_prompt.to_messages()[0]
        # Team.log.info("\n<Architect Instruction>" + meta_prompt_msg.content)
        prompt_instruction = self.llm.invoke(meta_prompt_msg)

        # ---------- constructing prompt to LLM ----------
        user_prompt_template = ChatPromptTemplate.from_template(
            WRITE_ARCHITECT_WITH_FDBACK_META
        )
        user_prompt_msg = user_prompt_template.invoke(
            {
                "original_requirement": original_requirement,
                "functional_requirement": functional_requirement,
                "instruction": prompt_instruction,
                "ce_feedback": feedback,
            }
        )
        user_prompt = user_prompt_msg.to_messages()[0]

        system_prompt = SystemMessage(content=self.system_msg)

        # ---------- prompt LLM ----------
        Team.log.info(
            "Prompt to generate architecture is: \n"
            + system_prompt.content
            + "\n"
            + user_prompt.content
        )
        result = self.llm.invoke(system_prompt, user_prompt)

        print(self.profile + " " + self.name + " generate Architect with feedback done")
        Team.log.info(
            self.profile + " " + self.name + " generate Architect with feedback done"
        )

        Team.log.info(result)

        # ---------- adding result to SCR(before align) ----------
        module_msg = Message(sender=self.profile, content=result)
        self.own_message = module_msg
        self.update_scr(module_msg)

        # ---------- writing result to local ----------
        self.message_to_file(module_msg.content)
        return

    # 迭代的探索生成
    def go_in_sample_with_fdback(self, feedback):
        print(self.profile + " " + self.name + " generate Architect with feedback")
        Team.log.info(
            self.profile + " " + self.name + " generate Architect with feedback"
        )

        # ---------- get the information needed from SCR ----------
        functional_requirement = self.getPRD().content
        original_requirement = self.getOriginRequirement().content
        # ---------- constructing prompt to LLM ----------
        # using message template from LangChain, the result is SYS Message & HUMAN Message.
        user_prompt_template = ChatPromptTemplate.from_template(
            WRITE_ARCHITECT_WITH_FDBACK
        )
        user_prompt_msg = user_prompt_template.invoke(
            {
                "original_requirement": original_requirement,
                "functional_requirement": functional_requirement,
                "ce_feedback": feedback,
            }
        )
        user_prompt = user_prompt_msg.to_messages()[0]

        system_prompt = SystemMessage(content=self.system_msg)

        # ---------- prompt LLM ----------
        Team.log.info(system_prompt.content + "\n" + user_prompt.content)
        result = self.llm_sample.invoke(system_prompt, user_prompt)

        # ------------ logging ----------
        Team.log.info(self.profile + " " + self.name)
        Team.log.info(result)

        # ---------- adding result to SCR(before align) ----------
        module_msg = Message(sender=self.profile, content=result)
        self.own_message = module_msg
        self.update_scr(module_msg)

        # ---------- writing result to local ----------
        self.message_to_file(module_msg.content)
        return

    def update_scr(self, message):
        """
        update team's shared certificated repository, with generated architecture
        """
        if len(Team.all_messages) < 3:
            # indicate that no new architecture
            Team.all_messages.append(message)
        else:
            # the other teams document
            Team.log.info("already a architect, replace it")
            Team.all_messages[2] = message

    def update_own_message(self, msg: Message):
        self.own_message = msg
        Team.all_messages[2] = msg

    def message_to_file(self, msg_content):
        # ---------- writing Architecture to local ----------
        file_name = "architect.md"

        Team.log.info(self.profile + " saving ARCHITECT")
        super().save_file_overwrite(
            os.path.join(Team.project_dir, file_name), msg_content
        )

    def getOriginRequirement(self):
        return Team.all_messages[0]

    def getPRD(self):
        return Team.all_messages[1]

    def go_inter(self):
        # 从项目dir里读取，并且加到自己的
        print(self.profile + " " + self.name + " extracting Architect......")
        Team.log.info(self.profile + " " + self.name + " extracting Architect......")
        result = read_file_2_line(Path(Team.incremental_base_dir) / "architect.md")
        if not os.path.exists(os.path.join(Team.project_dir, "architect.md")):
            self.message_to_file(result)
        module_msg = Message(sender=self.profile, content=result)
        self.own_message = module_msg
        # not perfect for now
        if len(Team.all_messages) <= 2:
            Team.all_messages.append(module_msg)
        else:
            Team.all_messages[2] = module_msg

    def getMessage():
        pass
