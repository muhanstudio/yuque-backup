from flask import Flask, render_template, redirect, url_for
import subprocess  # 用于运行外部脚本

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/backup')
def backup():
    # 运行备份脚本
    subprocess.run(['python', 'backup.py'])  # 替换为实际的备份脚本路径
    return redirect(url_for('index'))  # 运行后重定向回首页


@app.route('/refadd')
def refadd():
    # 运行添加引用脚本
    subprocess.run(['python', 'refadd.py'])  # 替换为实际的添加引用脚本路径
    return redirect(url_for('index'))


@app.route('/reflocal')
def reflocal():
    # 运行文档链接本地化脚本
    subprocess.run(['python', 'reflocal.py'])  # 替换为实际的链接本地化脚本路径
    return redirect(url_for('index'))


@app.route('/notes')
def notes():
    # 运行小记输出脚本
    subprocess.run(['python', 'notes.py'])  # 替换为实际的小记输出脚本路径
    return redirect(url_for('index'))


@app.route('/delete')
def delete():
    # 运行删除导出脚本
    subprocess.run(['python', 'delete.py'])  # 替换为实际的删除导出脚本路径
    return redirect(url_for('index'))


@app.route('/filelocal')
def filelocal():
    # 运行资源本地化脚本
    subprocess.run(['python', 'filelocal.py'])  # 替换为实际的资源本地化脚本路径
    return redirect(url_for('index'))


@app.route('/archives')
def archives():
    # 运行压缩导出脚本
    subprocess.run(['python', 'archives.py'])  # 替换为实际的压缩导出脚本路径
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
