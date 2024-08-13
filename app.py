import subprocess

from flask import Flask, render_template, request

app = Flask(__name__)

# 定义一个字典来存储按钮对应的处理函数
button_handlers = {}

def register_handler(button_id):
    def decorator(func):
        button_handlers[button_id] = func
        return func
    return decorator

@app.route('/')
def index():
    # 渲染主页
    return render_template('index.html', buttons=button_handlers.keys())

@app.route('/handle_button', methods=['POST'])
def handle_button():
    button_id = request.form['button_id']
    if button_id in button_handlers:
        handler = button_handlers[button_id]
        handler()
    return "操作成功"

# 示例：注册按钮处理函数
@register_handler('备份')
def handle_button1():
    subprocess.run(['python', 'backup.py'])

@register_handler('添加引用')
def handle_button2():
    subprocess.run(['python', 'refadd.py'])

# 其他按钮处理函数类似

if __name__ == '__main__':
    app.run(debug=True)
