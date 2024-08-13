import requests
import os
import yaml

def load_config(config_path):
    """从配置文件加载参数"""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config

def get_docs(book_id, token):
    """获取知识库所有文档及其父子关系"""
    headers = {
        'X-Auth-Token': token
    }
    url = f"https://www.yuque.com/api/v2/repos/{book_id}/toc"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['data']

def get_doc_details(book_id, token, slug):
    """获取文档详情"""
    headers = {
        'X-Auth-Token': token
    }
    url = f"https://www.yuque.com/api/v2/repos/{book_id}/docs/{slug}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['data']

def get_parent_path(doc, docs, output_dir):
    """递归获取父路径"""
    if doc['depth'] == 1:
        return output_dir
    parent_uuid = doc['parent_uuid']
    for p in docs:
        if p['uuid'] == parent_uuid:
            parent_path = get_parent_path(p, docs, output_dir)
            return os.path.join(parent_path, p['title'])
    raise ValueError(f"找不到父文档 {parent_uuid}")

def save_docs(docs, book_id, token, output_dir):
    """根据父子关系保存文档"""
    for doc in docs:
        parent_path = get_parent_path(doc, docs, output_dir)
        path = os.path.join(parent_path, f"{doc['title']}.md")
        os.makedirs(os.path.dirname(path), exist_ok=True)  # 确保父目录存在
        with open(path, 'w', encoding='utf-8') as f:
            f.write(get_doc_details(book_id, token, doc['slug'])['body'])

def main():
    config = load_config("config.yml")
    token = config['token']
    book_id = config['book_id']
    output_dir = "output"
    docs = get_docs(book_id, token)
    save_docs(docs, book_id, token, output_dir)

if __name__ == "__main__":
    main()
