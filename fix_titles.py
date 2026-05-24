import os
import re

base_dir = "."

def fix_titles(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    changed = False
    
    # Find <title> tags and strip any <a> tags inside them
    def strip_a_tags(match):
        inner_text = match.group(1)
        cleaned_text = re.sub(r'<a[^>]*>', '', inner_text)
        cleaned_text = cleaned_text.replace('</a>', '')
        return f"<title>{cleaned_text}</title>"

    new_content = re.sub(r'<title>(.*?)</title>', strip_a_tags, content, flags=re.IGNORECASE | re.DOTALL)
    
    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False

for root, dirs, files in os.walk(base_dir):
    if '.git' in root: continue
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            if fix_titles(path):
                print(f"Fixed title in {path}")
