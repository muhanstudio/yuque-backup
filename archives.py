import os
import zipfile


def zip_folder(folder_path, output_path):
    # 创建一个 ZipFile 对象
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 遍历文件夹及其子文件夹
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # 获取文件的完整路径
                file_path = os.path.join(root, file)
                # 将文件添加到 zip 文件中
                # arcname 参数用于去除文件夹前缀，使压缩包中的文件结构保持一致
                zipf.write(file_path, os.path.relpath(file_path, folder_path))


if __name__ == "__main__":
    # 定义要压缩的文件夹和输出 zip 文件的路径
    folder_to_zip = 'output'
    output_zip_file = 'archives.zip'

    # 调用函数进行压缩
    zip_folder(folder_to_zip, output_zip_file)

    print(f"文件夹 '{folder_to_zip}' 已成功压缩为 '{output_zip_file}'")