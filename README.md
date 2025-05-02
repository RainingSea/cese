### CESE 说明文档
#### 在 utils / essay.ipynb 这个文件下(最后Prompt for Sumary部分)，调一调总结的prompt，看改成extract会不会好一些

## 主要更改：
（1）保留了RTADev的代码，但全部注释掉了，不敢删
（2）控制流程还是在 **Team.run()** 方法中，具体的流程主要如下：
    1. inter_launch = True / False 还是不变，就是是否复制已经有的其他文件，这样相关的Agent直接复制就可以，不用prompt LLM
    2. Product Manager，Architect，Project Manager 三个角色生成完毕后，就进入**counter example**环节
（3）counter example 主要分为两个部分
    1. make_ce_dirs，这个函数复制对计划执行一些干扰策略，会在原项目目录下建ce/ce_{index}几个目录，index表示example的数量，可以在ce_generate里指定
    2. 创建完之后，紧跟着的for循环负责切入到对应的目录里，但是不用os.chdir()，然后生成代码，目录依旧是code目录
（4）然后是ceaug部分，counter example augment
    1. 这部分就是逐个生成上一步的代码的单元测试，并执行，最后挑选出一个得分最高的，代表对应项目暴露的问题影响最大
    1. 这个函数传入的参数很多，因为项目的测试用例对格式和路径要求很高
（5）ceaug执行完毕后得到一个反馈，把这个反馈加入到programmer的prompt里，然后生成代码

## 非主要更改
log还没有同步
然后programmer的code提取，以前是###，这个会和python的注释冲突，为了防止GPT发癫，改成***了
并且正则匹配捎作修改
加了代码对比

## 重要
有几个关键的路径需要设置好

| 文件名               | 变量名(所属函数)           | 说明                               |
|----------------------|----------------------------|------------------------------------|
| start_by_file.py      | project_description_path   | 数据集的目录                       |
|                      | projdir                    | 项目目录，需用绝对路径             |
|                      | category                   | 项目种类，帮助创建，最重要的是帮助找测试用例 |
|                      | name                       | 项目名，帮助创建，最重要的是帮助找测试用例 |
| ceaug/auto_test.py    | testcase_path(autogen)     | 测试用例目录路径                   |



(1)发现一些共性错误，例如route login


2025-04-28 game
跑之前是￥56

漏算了用call openai api 以及 ChatLLM 的token
以及时间

生成测试代码的花费
测试反馈生成和总结的花费