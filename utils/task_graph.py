import networkx as nx
import matplotlib.pyplot as plt

# 数据输入
origin_tasks = {
        "T0": '|handle user authentication|implement login and registration functionality|[]|related files:["main.py", "templates/login.html", "templates/register.html"]',
        "T1": '|display charities and contributions|implement dashboard functionality|["T0"]|related files:["main.py", "templates/dashboard.html"]',
        "T2": '|show charity details|implement charity details functionality|["T1"]|related files:["main.py", "templates/charity_details.html"]',
        "T3": '|manage data storage|implement DataManager for loading and saving data|["T0"]|related files:["main.py"]',
        "T4": '|handle donations|implement donation functionality on charity details page|["T2"]|related files:["main.py"]',
        "T6": '|finalize application|test and debug the entire application|["T4", "T5"]|related files:["main.py"]',
    }



inter_tasks = {
    "T0": '|handle login part||[]|related files:["main.py", "templates/login.html"]',
    "T1": '|handle registration part|implement user registration functionality|["T0"]|related files:["main.py", "templates/register.html"]',
    "T2": '|setup home page|implement home page functionality|["T1"]|related files:["main.py", "templates/home.html"]',
    "T3": '|recipe submission|implement recipe submission functionality|["T2"]|related files:["main.py", "templates/submit_recipe.html"]',
    "T4": '|recipe browsing|implement recipe browsing functionality|["T2"]|related files:["main.py", "templates/browse_recipes.html"]',
    "T5": '|recipe details|implement recipe details functionality|["T4"]|related files:["main.py", "templates/recipe_details.html"]',
}

# 解析数据并创建图
G = nx.DiGraph()

for task, details in origin_tasks.items():
    # 提取任务描述和前置任务
    parts = details.split("|")
    description = parts[1].strip()
    predecessors = eval(parts[3])  # 解析前置任务

    # 添加节点
    G.add_node(task, label=description)

    # 添加边（任务依赖）
    for predecessor in predecessors:
        G.add_edge(task, predecessor)

# 绘制图
plt.figure(figsize=(6, 6))
pos = nx.circular_layout(G)


labels = nx.get_node_attributes(G, "label")
offset = -0.05
label_pos = {node: (x + offset, y + offset) for node, (x, y) in pos.items()}

nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=1500,
    node_color="lightblue",
    font_size=8,
    font_weight="bold",
    edge_color="gray",
)

nx.draw_networkx_labels(
    G,
    label_pos,
    labels=labels,
    font_size=9,
    font_color="black",
)

plt.title("Task Dependency Graph")
plt.show()
