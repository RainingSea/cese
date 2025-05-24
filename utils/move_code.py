import os
import shutil


# 定义源文件夹和目标文件夹的路径


def generate():

    file_names = [
        "BusinessTaskScheduler.md",
        "DataSummarizer.md",
        "DataVisualizer.md",
        "DayPlanner.md",
        "ExpenseCategorizer.md",
        "ExpenseComparator.md",
        "ExpensePlanner.md",
        "InvestmentTracker.md",
        "KnowledgeTracker.md",
        "MedicalHealthTracker.md",
        "NoteArchiver.md",
        "NotepadPlus.md",
        "OfficeStockManager.md",
        "PaintPal.md",
        "PhotoStickerMaker.md",
        "QuickTimer.md",
        "RandomPasswordGenerator.md",
        "ScienceExperimentPlanner.md",
        "ScienceLibrary.md",
        "SecretNoteKeeper.md",
        "SecurePasswordVault.md",
        "ShapeMaster.md",
        "ShoppingPlanner.md",
        "SmartRecipt.md",
        "SportsEquipmentInventoryTracker.md",
        "TaskTracker.md",
        "TextSnippetOrganizer.md",
        "TimeConverter.md",
        "TimeSaver.md",
        "TimeTracker.md",
        "UnitConverter.md",
    ]

    category = "gui"
    for i in range(len(file_names)):
        source_dir = "../project/" + category + "/" + str(file_names[i][:-3]) + "_code"
        destination_dir = "../project/" + category + "/" + str(file_names[i][:-3])

        # 遍历源文件夹中的所有文件和文件夹
        for item in os.listdir(source_dir):
            s = os.path.join(source_dir, item)

            # 特殊处理log.log文件
            if item == "log.log":
                destination_log = os.path.join(destination_dir, item)
                # 如果目标目录中已存在log.log，则追加内容；否则直接复制
                if os.path.exists(destination_log):
                    try:
                        with open(
                            s, "r", encoding="utf-8", errors="replace"
                        ) as src_log, open(
                            destination_log, "a", encoding="utf-8", errors="replace"
                        ) as dest_log:
                            dest_log.write(src_log.read())
                    except Exception as e:
                        print(f"处理 {s} 时发生错误: {e}")
                else:
                    shutil.copy2(s, destination_log)
            # 跳过prd.md文件
            elif item == "prd.md":
                continue
            # 对于其他文件或文件夹
            else:
                d = os.path.join(destination_dir, item)
                if os.path.isfile(s):
                    shutil.copy2(s, d)  # 使用copy2保留文件的元数据
                elif os.path.isdir(s):
                    if os.path.exists(d):
                        shutil.rmtree(d)  # 如果目标文件夹已存在，则先删除
                    shutil.copytree(s, d)  # 复制文件夹及其内容
        print(i)

    print("复制完成")


def delete_files():
    file_names = [
        "BusinessTaskScheduler.md",
        "DataSummarizer.md",
        "DataVisualizer.md",
        "DayPlanner.md",
        "ExpenseCategorizer.md",
        "ExpenseComparator.md",
        "ExpensePlanner.md",
        "InvestmentTracker.md",
        "KnowledgeTracker.md",
        "MedicalHealthTracker.md",
        "NoteArchiver.md",
        "NotepadPlus.md",
        "OfficeStockManager.md",
        "PaintPal.md",
        "PhotoStickerMaker.md",
        "QuickTimer.md",
        "RandomPasswordGenerator.md",
        "ScienceExperimentPlanner.md",
        "ScienceLibrary.md",
        "SecretNoteKeeper.md",
        "SecurePasswordVault.md",
        "ShapeMaster.md",
        "ShoppingPlanner.md",
        "SmartRecipt.md",
        "SportsEquipmentInventoryTracker.md",
        "TaskTracker.md",
        "TextSnippetOrganizer.md",
        "TimeConverter.md",
        "TimeSaver.md",
        "TimeTracker.md",
        "UnitConverter.md",
    ]

    for i in range(len(file_names)):
        source_dir = "../project/gui/" + str(file_names[i][:-3]) + "_code"
        if os.path.exists(source_dir):
            shutil.rmtree(source_dir)
            print(f"文件夹 {source_dir} 已成功删除")
        else:
            print(f"文件夹 {source_dir} 不存在")


def read_files(folder_path):
    file_count = 0  # 初始化文件计数器

    # 遍历给定目录下的所有文件
    file_names = []
    for filename in os.listdir(folder_path):
        file_names.append(filename)
    print(len(file_names))
    return file_names


if __name__ == "__main__":
    # print(read_files("D:\Project\CE\CE\dataset\FSD-bench\dataset\gui"))
    # generate()
    delete_files()
