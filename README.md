## Hub for the paper "RTADev: Intention Aligned Multi-Agent Framework for Software Development"
> record our anonymous link for convenience
> https://anonymous.4open.science/r/RTAdev-6EC6
### Tutorial

```
├─0_config
├─agents 
├─align_flow # the alignment control process for agents other than the programmer.
├─messages
├─model # base model of project
├─project_dir # dir of generated projects
├─prompt # including each agent's generating prompt and alignment prompt
├─utils

```

### Generating Process

The prompts for the generation process of each agent are stored in the corresponding action files within the **prompt** folder.

### Alignment Process

The prompts for the alignment process (including checking and multi agent debate) of each agent are stored in the **align_prompt.py** file within the **prompt** folder.

#### Alignment Process Control

1. First, in the **/agents/team.py** file, specify which roles will undergo the alignment process. The operation involves designating the target role for the **self.roles[Reviewer]** and then executing this reviewer.

   > for example, the code to activate alignment process for Architect is 
   >
   > ```python
   > self.roles["Reviewer"].target = self.roles["Architect"]
   > self.roles["Reviewer"].go()
   > ```

2. Second, also in the **/agents/team.py** file, specify the number of alignment checking and the number of multi agents discussion rounds. Set the values for these two variables: **align_check_num** and **mad_num**

3. Finally, the control of the alignment process involves two files: one is **align_flow/align_flow.py** file in folder A, which controls the alignment process for all agents other than the programmer.  The other is **agents/programmer.py**, due to the complexity of the programmer's process, it has been extracted separately.

4. 2 ways to launch project: 
   [1] run /start_by_file.py and assign **name** and **project** within code
   [2] launch project in shell, see **/start_by_shell.py** to get information and refer **run.bat** to get format. 



## Counter Example Logic
>前提说明：程序员已经被替换为c_programmer，功能更多

1. 运行主程序，但是不用设置程序员 | 这样会得到需求文档，架构，计划
   1. （可选）将计划（字典形式的task list）复制到 utils.task_graph.py里，可以画图
2. 复制一个文件夹，(记录干扰任务是第几个) 并干扰节点 | 这样会得到干扰后的计划，以及不变的需求，架构（后续统一称这三份文档为计划）
3. 运行**增量主程序**，手动设置干扰任务（**trigger_task**变量），将**增量目录**设置为上一步的干扰目录，并注意运行c_programmer的是c_go()方法，基于干扰后的计划来生成代码，此代码生成过程在生成到对应的干扰计划时会停止，并仅将此过程的代码保存在本地
4. 运行主程序，手动设置干扰任务（**trigger_task**变量），将增量目录调回最初的目录（task没被干扰的），设置c_程序员，然后使用程序员原本的go()方法，此方法在进行到干扰任务那里时，将会把上一步生成的代码作为counter example，加入到prompt中去，（期望增强生成功能）

   
