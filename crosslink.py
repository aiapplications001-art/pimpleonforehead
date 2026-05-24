import os
import re

base_dir = "."

# Longer/more specific keywords first to prevent partial matches
keywords_map = {
    r"\b1% vs 2% salicylic acid\b": "/acne/1-vs-2-percent-salicylic-acid/",
    r"\bsalicylic acid face wash\b": "/acne/best-salicylic-acid-face-wash-india/",
    r"\bbenzoyl peroxide face wash\b": "/acne/best-benzoyl-peroxide-face-wash-india/",
    r"\bnon-comedogenic moisturizer[s]?\b": "/acne/best-non-comedogenic-moisturizer-india/",
    r"\bniacinamide serum[s]?\b": "/acne/niacinamide-serums-india/",
    r"\bpimple patch(?:es)?\b": "/acne/best-pimple-patch-india/",
    r"\bforehead acne\b": "/acne/forehead-acne/",
    r"\bback acne\b": "/acne/back-acne/",
    r"\bbacne\b": "/acne/back-acne/",
    r"\bhormonal acne\b": "/acne/hormonal-acne-vs-oily-skin/",
    r"\bpcos acne\b": "/acne/acne-pcos-treatment-indian-skin/",
    r"\bcystic acne\b": "/acne/cystic-chin-pimple/",
    r"\badapalene\b": "/acne/adapalene-differin-adaferin-gel-comparison-india/",
    r"\bface mapping\b": "/acne/face-map/",
    r"\bpimple vs zit\b": "/acne/pimple-zit/",
    r"\bnodule vs cyst\b": "/acne/nodule-cyst/",
    r"\bblackheads\b": "/acne/blackheads-whiteheads/",
}

# The inline style makes the link invisible (no underline, inherits text color)
subtle_style = 'style="color: inherit; text-decoration: none;"'

def add_crosslinks(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Determine current page URL to avoid self-linking
    rel_path = filepath.replace("./", "/").replace("index.html", "")
    
    # Tokenize HTML to protect certain blocks from replacement
    # 1. <a>...</a>
    # 2. <h[1-6]>...</h[1-6]> (we don't want links in headings)
    # 3. <script>...</script>
    # 4. <style>...</style>
    # 5. <...> (any other HTML tag, ensuring we don't replace inside alt="...", href="...", etc.)
    token_pattern = re.compile(r'(<a\b[^>]*>.*?</a>|<h[1-6]\b[^>]*>.*?</h[1-6]>|<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<[^>]+>)', re.IGNORECASE | re.DOTALL)
    
    tokens = token_pattern.split(content)
    
    used_urls = set()
    changed = False
    
    for i in range(len(tokens)):
        if i % 2 == 0:
            # Even indices are pure text content outside of protected tags
            text = tokens[i]
            for pattern, url in keywords_map.items():
                # Don't link to the current page, and only link to a URL once per page
                if url == rel_path or url in used_urls:
                    continue
                
                # Check if keyword exists in this text block
                if re.search(pattern, text, re.IGNORECASE):
                    # Replace only the first occurrence in the text
                    text = re.sub(pattern, lambda m: f'<a href="{url}" {subtle_style}>{m.group(0)}</a>', text, count=1, flags=re.IGNORECASE)
                    used_urls.add(url)
                    changed = True
            tokens[i] = text

    if changed:
        new_content = "".join(tokens)
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
            # strictly exclude the scan directory
            if "/scan/" in path or "scan/index.html" in path:
                continue
            
            if add_crosslinks(path):
                print(f"Added subtle cross-links to: {path}")
                count += 1

print(f"Total pages cross-linked: {count}")
