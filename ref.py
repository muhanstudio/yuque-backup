import os
from pathlib import Path

def append_references_to_md_files(output_dir):
    """
    递归遍历指定目录及其子目录下的所有 .md 文件，在每个文件末尾添加三行空行，
    并引用同一目录下与该文件同名的子文件夹中的所有 .md 文件。
    """
    for entry in os.scandir(output_dir):
        if entry.is_dir(follow_symlinks=False):
            # 递归处理子目录
            append_references_to_md_files(entry.path)
        elif entry.name.endswith('.md'):
            process_md_file(entry.path)

def process_md_file(file_path):
    """
    处理单个 .md 文件，添加三行空行，并引用同一目录下的所有 .md 文件。
    """
    file_name = Path(file_path).name
    folder_name = file_name[:-3]  # 去掉 .md 扩展名
    folder_path = Path(file_path).parent / folder_name

    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 在文件末尾添加三行空行
    new_content = content.rstrip() + '\n\n\n'

    # 添加引用
    if folder_path.is_dir():
        sub_files = [f for f in os.listdir(folder_path) if f.endswith('.md')]
        for sub_file in sub_files:
            ref_file = sub_file[:-3]  # 去掉 .md 扩展名
            new_content += f'[{ref_file}](./{folder_name}/{sub_file})\n\n'

    # 写入新内容
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

if __name__ == "__main__":
    output_dir = './output'
    append_references_to_md_files(output_dir)

