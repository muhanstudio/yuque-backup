import requests
import os
import yaml
import re


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


def find_doc_by_slug(docs, slug):
    """通过 slug 查找文档"""
    for doc in docs:
        if doc['slug'] == slug:
            return doc
    return None


def get_parent_path(doc, docs):
    """递归获取父路径"""
    if doc['depth'] == 1:
        return [doc['title']]
    parent_uuid = doc['parent_uuid']
    for p in docs:
        if p['uuid'] == parent_uuid:
            parent_path = get_parent_path(p, docs)
            return parent_path + [doc['title']]
    raise ValueError(f"找不到父文档 {parent_uuid}")


def find_doc_path(slug, book_id, token):
    """通过 slug 反查文档路径"""
    docs = get_docs(book_id, token)
    doc = find_doc_by_slug(docs, slug)
    if not doc:
        raise ValueError(f"找不到 slug 为 {slug} 的文档")
    path = get_parent_path(doc, docs)
    return os.path.join(*path) + ".md", doc


def search_and_replace_links(docs, book_id, token, output_dir):
    """搜索并替换链接"""
    for root, _, files in os.walk(output_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 查找所有包含 slug 的链接
                matches = re.findall(r'\(([^)]+)\)', content)
                for match in matches:
                    for doc in docs:
                        if doc['slug'] in match:
                            doc_path, _ = find_doc_path(doc['slug'], book_id, token)
                            content = content.replace(f"({match})", f"({doc_path})")

                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)


def main():
    config = load_config("config.yml")
    token = config['token']
    book_id = config['book_id']
    output_dir = "output"

    docs = get_docs(book_id, token)
    search_and_replace_links(docs, book_id, token, output_dir)


if __name__ == "__main__":
    main()
