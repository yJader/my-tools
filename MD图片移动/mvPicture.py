import os
import re
import shutil

def move_images(md_file):
    # 获取.md文件名（不包含扩展名）
    md_file_name = os.path.splitext(md_file)[0]

    # 创建.assets文件夹（如果不存在）
    assets_folder = md_file_name + ".assets"
    if not os.path.exists(assets_folder):
        os.makedirs(assets_folder)

    # 打开.md文件并读取内容
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

        # 使用正则表达式匹配图片引用
        img_pattern = r'(\\./)?(assets|media)/(.+?)\.(png|jpg|gif|webp)'
        img_matches = re.findall(img_pattern, content)

        # 遍历匹配到的图片引用
        for img_match in img_matches:
            # 获取图片文件名和新的路径
            img_name = img_match[2] + '.' + img_match[3]
            img_path = img_match[1] + '/'+ img_name
            new_img_path = os.path.join(assets_folder, img_name)

            # 移动图片文件并更新图片引用
            if os.path.exists(img_path):
                shutil.move(img_path, new_img_path)
                content = content.replace(img_path, new_img_path)

    # 将更新后的内容写回.md文件
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(content)

def move_md_and_assets(md_file):
    # 获取文件夹名（不包含扩展名）
    folder_name = os.path.splitext(md_file)[0]

    # 创建文件夹（如果不存在）
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # 将.md文件移动到相应文件夹内
    shutil.move(md_file, os.path.join(folder_name, md_file))

    # 将.assets文件夹内的文件移动到相应文件夹内
    assets_folder = folder_name + ".assets"
    target_assets_folder = os.path.join(folder_name, assets_folder)
    if not os.path.exists(target_assets_folder):
        os.makedirs(target_assets_folder)
    
    if os.path.exists(assets_folder):
        for file_name in os.listdir(assets_folder):
            file_path = os.path.join(assets_folder, file_name)
            shutil.move(file_path, os.path.join(target_assets_folder, file_name))

        # 删除空的.assets文件夹
        os.rmdir(assets_folder)



def main():
    # 列出当前文件夹下的所有.md文件
    files = [file for file in os.listdir() if file.endswith('.md')]
    if not files:
        print("当前文件夹下不存在任何 .md 文件")
        return

    # 打印.md文件列表
    print("当前文件夹下的 .md 文件:")
    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")

    # 让用户选择文件
    choice = input("请选择要移动的文件编号: ")

    try:
        choice_index = int(choice)
        if choice_index < 1 or choice_index > len(files):
            print("选择的文件编号无效")
            return
        selected_file = files[choice_index - 1]
    except ValueError:
        print("请输入有效的数字")
        return

    # 执行移动文件的操作
    move_images(selected_file)
    move_md_and_assets(selected_file)
    print(f"文件 '{selected_file}' 移动完成")

if __name__ == "__main__":
    main()