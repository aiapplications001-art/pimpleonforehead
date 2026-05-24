import os
import re

base_dir = "."

premium_html = """
      <!-- Face AI Skin Analysis CTA -->
      <div class="face-ai-cta-wrapper reveal" style="transition-delay: 0.5s; margin-top: 2.5rem;">
        <a href="/scan" class="face-ai-btn">
          <span class="face-ai-btn-text">Start your free skin analysis now</span>
          <div class="face-ai-energy-rail"></div>
        </a>
        <p class="face-ai-subtext">Scan your face to understand visible acne, oiliness, marks, texture, and skin signals in about 60 seconds.</p>
      </div>
"""

premium_css = """
    /* Face AI CTA Styling - Premium Perimeter Rail Animation */
    .face-ai-cta-wrapper { display: flex; flex-direction: column; align-items: center; gap: 14px; margin: 3rem auto 0; text-align: center; width: 100%; position: relative; z-index: 50; }
    .face-ai-btn { 
      position: relative; 
      display: inline-flex; 
      align-items: center;
      justify-content: center;
      padding: 18px 44px; 
      background: #EC610E; 
      color: #ffffff !important; 
      text-decoration: none; 
      font-weight: 800; 
      font-size: 1.15rem; 
      border-radius: 9999px; 
      box-shadow: 0 10px 30px rgba(236,97,14,0.3); 
      transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
      z-index: 10;
      overflow: visible;
    }
    .face-ai-btn:hover { transform: translateY(-3px); box-shadow: 0 15px 40px rgba(236,97,14,0.5); }
    .face-ai-btn-text { position: relative; z-index: 12; }
    .face-ai-subtext { color: rgba(255,255,255,0.85); font-size: 13px; max-width: 480px; line-height: 1.5; margin: 0 auto; display: block !important; visibility: visible !important; }
    
    .face-ai-energy-rail { 
      position: absolute; 
      inset: -3px; 
      border-radius: 9999px; 
      pointer-events: none;
      z-index: 5;
      padding: 3px;
      overflow: hidden;
      mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
      -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
      mask-composite: exclude;
      -webkit-mask-composite: xor;
    }
    
    .face-ai-energy-rail::before {
      content: "";
      position: absolute;
      top: 50%;
      left: 50%;
      width: 400%; 
      height: 400%;
      background: conic-gradient(from 0deg, transparent 65%, #EC610E 80%, #FFE1CE 95%, #ffffff 100%);
      animation: energy-loop 3.5s ease-in-out forwards;
    }

    @keyframes energy-loop {
      0% { transform: translate(-50%, -50%) rotate(0deg); opacity: 0; }
      5% { opacity: 1; }
      90% { opacity: 1; }
      100% { transform: translate(-50%, -50%) rotate(765deg); opacity: 0.8; }
    }

    .face-ai-energy-rail::after {
      content: "";
      position: absolute;
      inset: 0;
      background: inherit;
      filter: blur(8px);
      opacity: 0.7;
    }

    @media (max-width: 768px) {
      .face-ai-btn { padding: 16px 32px; font-size: 1rem; width: 100%; max-width: 340px; }
      .face-ai-subtext { font-size: 12px; padding: 0 10px; }
    }
"""

def safe_inject(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip if already injected
    if "face-ai-cta-wrapper" in content:
        return False

    # 1. Update Hero Padding to ensure subtext fits
    # Global hero padding
    content = re.sub(r'(\.hero\s*\{[^}]*?padding:\s*)[^;]+?;', r'\1 6rem 2rem 10rem;', content)
    # Global full-hero padding (for Hindi guide)
    content = re.sub(r'(\.full-hero\s*\{[^}]*?padding:\s*)[^;]+?;', r'\1 6rem 2rem 10rem;', content)
    # Mobile hero padding
    content = re.sub(r'(@media \(max-width: 768px\) \{\s+\.hero\s*\{[^}]*?padding:\s*)[^;]+?;', r'\1 4rem 1.5rem 8rem;', content)

    # 2. Inject CSS right before </style>
    if "</style>" in content:
        content = content.replace("</style>", premium_css + "\n  </style>")
    else:
        return False # Should never happen, but safety first

    # 3. Inject HTML into Hero
    hero_patterns = [
        (r'(<section[^>]*?class="[^"]*?hero[^"]*?".*?)(</section>)'),
        (r'(<header[^>]*?class="[^"]*?hero[^"]*?".*?)(</header>)'),
        (r'(<header[^>]*?class="[^"]*?full-hero[^"]*?".*?)(</header>)')
    ]
    
    hero_injected = False
    for pattern_str in hero_patterns:
        match = re.search(pattern_str, content, re.DOTALL)
        if match:
            full_hero_block = match.group(0)
            inner_match = re.search(r'(<div[^>]*?class="[^"]*?(?:container|hero-inner|hero-content)[^"]*?".*?)(</div>)', full_hero_block, re.DOTALL)
            if inner_match:
                div_content = inner_match.group(0)
                new_div_content = div_content.replace(inner_match.group(2), premium_html + inner_match.group(2))
                content = content.replace(div_content, new_div_content)
                hero_injected = True
                break
            else:
                content = content.replace(match.group(2), premium_html + match.group(2))
                hero_injected = True
                break

    if not hero_injected:
        h1_match = re.search(r'</h1>', content)
        if h1_match:
            idx = h1_match.end()
            p_match = re.search(r'</p>', content[idx:idx+500])
            if p_match: idx += p_match.end()
            content = content[:idx] + premium_html + content[idx:]
            hero_injected = True

    if hero_injected:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

for root, dirs, files in os.walk(base_dir):
    if '.git' in root: continue
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            if "scan/index.html" in path: continue
            if safe_inject(path):
                print(f"Successfully safely injected into {path}")
