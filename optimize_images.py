import os
import re

base_dir = "."

def optimize_images(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content

    # Find all img tags using a non-greedy regex
    img_tags = re.findall(r'<img[^>]+>', content)
    
    hero_img_src = None
    hero_found_for_page = False
    
    for img in img_tags:
        new_img = img
        
        # Extract src
        src_match = re.search(r'src="([^"]+)"', img)
        src = src_match.group(1) if src_match else ""
        
        # Remove existing loading, decoding, fetchpriority attributes to avoid duplicates
        new_img = re.sub(r'\s+loading="[^"]+"', '', new_img)
        new_img = re.sub(r'\s+decoding="[^"]+"', '', new_img)
        new_img = re.sub(r'\s+fetchpriority="[^"]+"', '', new_img)
        
        # Determine image type
        if "logo" in src.lower():
            # Logos: Fast decoding, no lazy loading (usually in header/footer)
            new_img = new_img.replace('<img ', '<img fetchpriority="high" decoding="async" ')
        elif not hero_found_for_page:
            # First non-logo image is assumed to be the Hero/LCP image
            # Crucial for Web Vitals: High fetch priority, NO lazy loading, async decoding
            new_img = new_img.replace('<img ', '<img fetchpriority="high" decoding="async" ')
            hero_img_src = src
            hero_found_for_page = True
        else:
            # All other images are below the fold
            # Use native browser lazy loading to defer loading until scroll
            new_img = new_img.replace('<img ', '<img loading="lazy" decoding="async" ')
            
        content = content.replace(img, new_img)
        
    # Inject a preload tag for the Hero/LCP image in the <head> to start fetching it before the HTML finishes parsing
    if hero_img_src and "</head>" in content:
        # Check if already preloaded
        preload_tag = f'<link rel="preload" as="image" href="{hero_img_src}">'
        if preload_tag not in content:
            # Insert before </head>
            content = content.replace("</head>", f"  {preload_tag}\n</head>")

    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

count = 0
for root, dirs, files in os.walk(base_dir):
    if '.git' in root: continue
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            # STRICT EXCLUSION: Do not touch the /scan directory
            if "/scan/" in path or "scan/index.html" in path:
                continue
            
            if optimize_images(path):
                print(f"Optimized images in: {path}")
                count += 1
                
print(f"Total files optimized for Core Web Vitals: {count}")
