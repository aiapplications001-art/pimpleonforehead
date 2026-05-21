import os
import re

base_dir = "."
base_url = "https://mymirror.fit"

for root, dirs, files in os.walk(base_dir):
    if '.git' in root:
        continue
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Find first valid image
            img_matches = re.findall(r'<img[^>]+src="([^"]+)"', content)
            hero_img = None
            for img in img_matches:
                if "logo" not in img.lower() and "favicon" not in img.lower():
                    hero_img = img
                    break
            
            if not hero_img:
                continue
            
            # Ensure absolute URL
            if hero_img.startswith("/"):
                abs_img_url = base_url + hero_img
            elif hero_img.startswith("http"):
                abs_img_url = hero_img
            else:
                abs_img_url = base_url + "/" + hero_img

            changed = False
            
            # Check og:image
            if 'property="og:image"' not in content:
                og_tag = f'  <meta property="og:image" content="{abs_img_url}" />\n  <meta name="twitter:image" content="{abs_img_url}" />'
                if '<link rel="icon"' in content:
                    content = content.replace('<link rel="icon"', f'{og_tag}\n  <link rel="icon"')
                else:
                    content = content.replace('</head>', f'{og_tag}\n</head>')
                changed = True
            elif 'name="twitter:image"' not in content:
                 tw_tag = f'  <meta name="twitter:image" content="{abs_img_url}" />'
                 content = content.replace('</head>', f'{tw_tag}\n</head>')
                 changed = True
                 
            # Add image to JSON-LD if not present
            if 'application/ld+json' in content and '"image"' not in content:
                content = re.sub(r'("description"\s*:\s*"[^"]+",)', r'\1\n        "image": "' + abs_img_url + '",', content, count=1)
                changed = True

            if changed:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Updated {filepath} with image {abs_img_url}")
