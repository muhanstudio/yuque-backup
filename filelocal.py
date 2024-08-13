import os
import re
import requests
from urllib.parse import urlparse


def download_file(url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.join(dest_folder, os.path.basename(urlparse(url).path))
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {url} to {filename}")
        return filename
    else:
        print(f"Failed to download {url}")
        return None


def extract_attachment_urls(md_content):
    # Regular expression to find all URLs in the markdown file
    url_pattern = re.compile(r'\[.*?]\((https?://.*?)\)')
    urls = url_pattern.findall(md_content)
    return urls


def update_md_links(md_content, url_to_local_path):
    for url, local_path in url_to_local_path.items():
        md_content = md_content.replace(url, './' + local_path)
    return md_content


def process_md_file(md_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Extract all attachment URLs
    urls = extract_attachment_urls(md_content)

    # Create the destination folder
    md_filename = os.path.basename(md_file)
    dest_folder = os.path.splitext(md_filename)[0] + '_attach'

    # Dictionary to map URLs to local paths
    url_to_local_path = {}

    # Download each URL and update the dictionary
    for url in urls:
        local_path = download_file(url, dest_folder)
        if local_path:
            url_to_local_path[url] = os.path.relpath(local_path, os.path.dirname(md_file))

    # Update the Markdown content with local paths
    updated_md_content = update_md_links(md_content, url_to_local_path)

    # Write the updated content back to the Markdown file
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(updated_md_content)


if __name__ == '__main__':
    md_file = ''  # Replace with your markdown file
    process_md_file(md_file)
