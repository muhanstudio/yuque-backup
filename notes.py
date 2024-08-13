import os
import requests
import json
import yaml
import urllib.parse
from bs4 import BeautifulSoup

# 从 config.yml 加载配置
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

# 请求的URL
url = "https://www.yuque.com/api/modules/note/notes/NoteController/index?offset=0&q=&filter_type=all&status=0&merge_dynamic_data=0&order=content_updated_at&with_pinned_notes=true&limit=20"

# 从配置中获取请求头
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Cookie": config['headers']['Cookie'],
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "X-CSRF-Token": config['headers']['X-CSRF-Token'],
    "X-Login": config['headers']['X-Login']
}

# 发送GET请求
response = requests.get(url, headers=headers)


def parse_card(value):
    """解析卡片元素的value"""
    decoded_value = urllib.parse.unquote(value[5:])  # 去掉 'data:' 前缀并解码
    return json.loads(decoded_value)


def convert_to_html_and_md(abstract):
    """解析abstract并转换为HTML和Markdown格式"""
    soup = BeautifulSoup(abstract, 'html.parser')
    html_output = []
    md_output = []

    for element in soup.descendants:
        # 检查是否是最顶层的 <p><span></span></p>
        if element.name == 'span' and element.parent.name == 'p' and element.parent.parent is soup:
            text = element.get_text()
            html_output.append(f"<p>{text}</p>")
            md_output.append(text + "\n\n")

        elif element.name == 'table':
            html_output.append(str(element))
            rows = element.find_all('tr')
            if rows:
                # 处理表格标题行
                header_row = rows[0]
                headers = '| ' + ' | '.join(
                    cell.get_text(strip=True) for cell in header_row.find_all(['td', 'th'])) + ' |'
                separator = '| ' + ' | '.join('---' for _ in header_row.find_all(['td', 'th'])) + ' |'
                md_output.append(headers)
                md_output.append(separator)

                # 处理表格数据行
                for row in rows[1:]:
                    md_row = '| ' + ' | '.join(cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])) + ' |'
                    md_output.append(md_row)
                md_output.append('')

        elif element.name == 'blockquote':
            if 'lake-alert-tips' in element.get('class', []):
                text = element.get_text()
                html_output.append(f"<blockquote class='lake-alert lake-alert-tips'>{text}</blockquote>")
                md_output.append(f"!!! {text}\n\n")
            else:
                text = element.get_text()
                html_output.append(f"<blockquote>{text}</blockquote>")
                md_output.append(f"> {text}\n\n")

        elif element.name == 'card':
            card_type = element.get('name')
            value = element.get('value')
            if card_type in ['file', 'image']:
                card_data = parse_card(value)
                link = f'<a href="{card_data["src"]}" download>{card_data["name"]}</a>'
                html_output.append(link)
                md_output.append(f"[{card_data['name']}]({card_data['src']})\n\n")
            elif card_type == 'hr':
                html_output.append("<hr>")
                md_output.append("---\n\n")
            elif card_type == 'codeblock':
                card_data = parse_card(value)
                html_output.append(f"<pre><code class='{card_data['mode']}'>{card_data['code']}</code></pre>")
                md_output.append(f"```{card_data['mode']}\n{card_data['code']}\n```\n\n")

    return '\n'.join(html_output), '\n'.join(md_output)


# 检查请求是否成功
if response.status_code == 200:
    data = response.json()

    # 创建存储文件的文件夹
    os.makedirs("notes/html", exist_ok=True)
    os.makedirs("notes/md", exist_ok=True)

    # 遍历每个note
    for note in data.get("notes", []):
        abstract = note['content']['abstract']
        created_at = note['created_at']
        tags = [tag['name'] for tag in note.get('tags', [])]

        # 解析abstract并转换为HTML和Markdown
        html_content, md_content = convert_to_html_and_md(abstract)

        # 在文件开头添加created_at和tags
        tags_str = ', '.join(tags)
        html_header = f"<div><strong>Created At:</strong> {created_at}<br><strong>Tags:</strong> {tags_str}</div><hr>"
        md_header = f"**Created At:** {created_at}\n\n**Tags:** {tags_str}\n\n---\n\n"

        # 创建文件名，使用note的id
        html_file_name = f"notes/html/note_{note['id']}.html"
        md_file_name = f"notes/md/note_{note['id']}.md"

        # 写入HTML文件
        with open(html_file_name, 'w', encoding='utf-8') as f:
            f.write(html_header + html_content)

        # 写入Markdown文件
        with open(md_file_name, 'w', encoding='utf-8') as f:
            f.write(md_header + md_content)

        print(f'Saved: {html_file_name} and {md_file_name}')

else:
    print(f"Failed to retrieve notes. Status code: {response.status_code}")
