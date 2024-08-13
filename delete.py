import os
import shutil


def delete_output(output_dir):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print('删除output文件夹成功')
    else:
        print('output文件夹不存在')


if __name__ == '__main__':
    delete_output('output')
