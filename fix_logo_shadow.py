import os
import re

base_dir = "."

def fix_logo(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip scan directory
    if "scan/index.html" in filepath or "/scan/" in filepath:
        return False
        
    # We want to add border-radius: 0, box-shadow: none, margin: 0 to .nav-logo img
    # Regex to find .nav-logo img { ... } and add the overrides inside it if they don't exist
    
    def replacer(match):
        inner = match.group(1)
        if "box-shadow: none" in inner:
            return match.group(0) # Already fixed
        return f".nav-logo img {{{inner} margin: 0; box-shadow: none; border-radius: 0; background: transparent; }}"

    new_content = re.sub(r'\.nav-logo img\s*\{([^}]*?)\}', replacer, content)

    # Let's also check if there are global img styles applying to the footer logo.
    # The footer logo usually looks like: <img src="/acne/forehead-acne/logo-v4.png" alt="mymirror" style="height:32px; opacity:0.5; margin-bottom:2rem;">
    # Let's fix that inline style to also prevent shadows/border-radius just in case.
    new_content = re.sub(
        r'(<img[^>]*?alt="mymirror"[^>]*?style=")([^"]*?)(")', 
        lambda m: m.group(1) + m.group(2) + ("; box-shadow: none; border-radius: 0;" if "box-shadow" not in m.group(2) else "") + m.group(3), 
        new_content
    )

    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False

count = 0
for root, dirs, files in os.walk(base_dir):
    if '.git' in root: continue
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            if fix_logo(path):
                print(f"Fixed logo in {path}")
                count += 1
print(f"Total fixed: {count}")
