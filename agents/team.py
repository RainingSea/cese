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
from ceaug.ceaug_main import ceaug, create_ce_document, feedback_split, make_ce_dirs
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
        # codebase dir
        code_base_dir = os.path.join(Team.project_dir, "code")
        port = update_flask_port(os.path.join(code_base_dir, "main.py"), "")

        # 这个2就是重复测试的次数
        for j in range(2):
            # set code dir
            ce_projects_paths = [Team.project_dir]
            # execute unit test
            ce_score, ce_feedback = ceaug(
                previous_work_dir,
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
        self.team.roles["Programmer"].message_to_file(
            self.roles["Programmer"].own_message.content
        )

        return

    # sampling run
    def run(self):
        previous_work_dir = Path.cwd()
        pervious_project_dir = Team.project_dir

        inter_launch = True
        # inter_launch = False

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

            # self.roles["Architect"].go()
            # Team.active_role(self.roles["Architect"].profile)

            # self.roles["Project Manager"].go()
            # Team.active_role(self.roles["Project Manager"].profile)
        # make ce dirs and copy the prd to each dir
        # ce_projects_paths = make_ce_dirs(Team.project_dir, 2)

        # # generate sampling architect
        # for j in range(len(ce_projects_paths)):
        #     print(f"\ngenerate the architect of {j}th counter project\n")
        #     Team.incremental_base_dir = os.path.normpath(ce_projects_paths[j])
        #     Team.project_dir = ce_projects_paths[j]

        #     self.roles["Product Manager"].go_inter()
        #     # sample architect generate
        #     self.roles["Architect"].go_in_sample()
        #     # sample task plan generate
        #     self.roles["Project Manager"].go_in_sample()
        #     # temporarily change project dir to a ce folder

        #     self.roles["Programmer"].go_in_sample()
        #     self.roles["Programmer"].code_base.clear()
        #     code_base_dir = os.path.join(Team.project_dir, "code")
        #     port = update_flask_port(os.path.join(code_base_dir, "main.py"), "")

        # # |--------- simplest coding process ---------|
        # # |
        # # self.roles["C_Programmer"].go(feedback)
        # # return
        # # |
        # # |--------- simplest coding process ---------|

        # # execute unit test
        # ce_score, ce_feedbacks = ceaug(
        #     previous_work_dir,
        #     ce_projects_paths,
        #     Team.projec_catogory,
        #     Team.project_name,
        #     "ite_fdback",
        #     Team.log,
        # )

        # # |_____________________________________________________________|
        # # |                      Attention!                             |
        # # | ceaug() execute unit test, which                            |
        # # | requires switching work dir to the test code's project dir "|
        # # |                   Must switch back!                         |
        # # |_____________________________________________________________|
        # # |

        # os.chdir(previous_work_dir)
        # Team.project_dir = pervious_project_dir
        # Team.incremental_base_dir = pervious_project_dir

        # _______________ use feedback to generate document _______________
        # self.roles["Product Manager"].go_inter()
        # self.roles["Architect"].go_with_fdback(ce_feedbacks["arch"])
        # self.roles["Project Manager"].go_with_fdback(ce_feedbacks["plan"])

        ce_feedback = """### Passed Test Cases
1. |Case|:**registration**
   ```plaintext
   DEFINE register_route with GET and POST methods:
       IF POST method is used:
           GET username and password from the registration form
           CALL NoteTakingApp's register method with username and password
           IF registration is successful:
               REDIRECT to the login page
       RENDER registration template
   ```

2. |Case|:**user_login**
   ```plaintext
   Function do_login(username, password):
       If user_manager.login(username, password) is True:
           session['username'] = username
           Redirect to dashboard
       Else:
           Redirect to login page
   ```

3. |Case|:**user_registration**
   ```plaintext
   Function register():
       If request.method is POST:
           username = request.form['username']
           password = request.form['password']
           If user_manager.register(username, password) is True:
               Redirect to login
       Render registration template
   ```

4. |Case|:**view_notes_on_dashboard**
   ```plaintext
   Function dashboard():
       If 'username' not in session:
           Redirect to login
       notes = note_manager.get_notes(session['username'])
       Render dashboard template with notes
   ```

5. |Case|:**add_new_note**
   ```plaintext
   Function add_note():
       If 'username' not in session:
           Redirect to login
       If request.method is POST:
           title = request.form['title']
           content = request.form['content']
           note_manager.add_note(session['username'], title, content)
           Redirect to dashboard
       Render add note template
   ```

6. |Case|:**view_note_details**
   ```plaintext
   Function view_note(title):
       If 'username' not in session:
           Redirect to login
       If request.method is POST:
           new_content = request.form['content']
           note_manager.edit_note(session['username'], title, new_content)
           Redirect to dashboard
       note_details = note_manager.get_note_details(session['username'], title)
       Render view note template with note_details
   ```

7. |Case|:**edit_note**
   ```plaintext
   Function view_note(title):
       ... (previous code)
       If request.method is POST:
           # Edit content logic
           note_manager.edit_note(session['username'], title, new_content)
           Save changes and redirect to dashboard
   ```

8. |Case|:**logout**
   ```plaintext
   Function logout():
       session.pop('username', None)
       Redirect to login
   ```

### Failed or Error Test Cases
1. |Case|:**add_new_note**
   - **Error Analysis**: The test failed because it could not locate the "Add Note" link, likely due to an authentication failure resulting from a failed login process.
   - **Improvement Guidance**: Ensure that user sessions are effectively managed. Each user login must result in setting the session correctly, and all routes should verify user authentication before rendering views or options that depend on user data.

2. |Case|:**delete_note**
   - **Error Analysis**: The test intentionally fails as the delete functionality is not implemented in the project.
   - **Improvement Guidance**: Ensure that any essential functionality (like deleting notes) is not only defined in the business logic but also has a user-facing feature within the application. Plan routes and UI elements for every feature you expose in your backend logic.

3. |Case|:**edit_note**
   - **Error Analysis**: This error occurred because the test could not find the "First Note" link, suggesting that the notes are not being loaded correctly for the logged-in user.
   - **Improvement Guidance**: Double-check the implementation of user-related features, such as adding and retrieving notes. Ensure that notes are consistently associated with the correct user account and accessible through the dashboard.

4. |Case|:**login**
   - **Error Analysis**: The test fails because it results in a 404 error when attempting to validate the dashboard title, indicating issues with user authentication.
   - **Improvement Guidance**: Always provide intuitive navigation options on each page. For example, all major functionalities should be easily accessible from the dashboard.

5. |Case|:**view_notes_on_dashboard**
   - **Error Analysis**: The test failed because no notes were found associated with the logged-in user.
   - **Improvement Guidance**: Maintain consistency in your UI elements. When adding new features or functionalities, ensure UI links are added where they logically belong to allow for seamless user experience.

6. |Case|:**view_note_details**
   - **Error Analysis**: Similar to `edit_note`, the inability to find "First Note" indicates issues with loading notes for the user.
   - **Improvement Guidance**: After implementing new functionalities or UI changes, conduct unit tests or integration tests specifically against all interfaces to validate they perform as expected.

7. |Case|:**search_for_note**
   - **Error Analysis**: The test fails to find the "Search Notes" link, likely due to the user not being properly logged in.
   - **Improvement Guidance**: Regular checks of your UI against your functional requirements will help in catching issues early.
        """
        # ce_feedback = ce_feedbacks["code"]
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
