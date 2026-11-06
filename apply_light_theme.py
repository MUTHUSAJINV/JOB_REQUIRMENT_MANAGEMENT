import os, glob

# 1. Update style.css
css_path = r'c:\Users\SAJIN\OneDrive\Desktop\job\static\css\style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace hardcoded colors in CSS
css = css.replace('color: #fff;', 'color: var(--text-main);')
css = css.replace('color: #e2e8f0;', 'color: var(--text-main);')
css = css.replace('color: #cbd5e1;', 'color: var(--text-muted);')
css = css.replace('rgba(255, 255, 255, 0.05)', 'rgba(0, 0, 0, 0.03)')
css = css.replace('rgba(255, 255, 255, 0.08)', 'rgba(0, 0, 0, 0.05)')
css = css.replace('rgba(255, 255, 255, 0.15)', 'rgba(0, 0, 0, 0.08)')
css = css.replace('rgba(255, 255, 255, 0.1)', 'rgba(0, 0, 0, 0.06)')
css = css.replace('rgba(255, 255, 255, 0.2)', 'rgba(0, 0, 0, 0.1)')
css = css.replace('rgba(255, 255, 255, 0.3)', 'rgba(0, 0, 0, 0.15)')
css = css.replace('rgba(255, 255, 255, 0.04)', 'rgba(0, 0, 0, 0.03)')
css = css.replace('rgba(255, 255, 255, 0.03)', 'rgba(0, 0, 0, 0.02)')
css = css.replace('rgba(255, 255, 255, 0.02)', 'rgba(0, 0, 0, 0.01)')
css = css.replace('rgba(255, 255, 255, 0.06)', 'rgba(0, 0, 0, 0.04)')
css = css.replace('rgba(255, 255, 255, 0.12)', 'rgba(0, 0, 0, 0.05)')
css = css.replace('rgba(255, 255, 255, 0.18)', 'rgba(0, 0, 0, 0.08)')
css = css.replace('background: rgba(16, 22, 38, 0.85);', 'background: #ffffff;')

# Fix shadows for light theme
css = css.replace('box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);', 'box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);')
css = css.replace('box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);', 'box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);')
css = css.replace('box-shadow: var(--shadow-md);', 'box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);')

# Card hover borders
css = css.replace('border-color: rgba(255, 255, 255, 0.14);', 'border-color: rgba(0, 0, 0, 0.08);')
css = css.replace('border-color: rgba(255, 255, 255, 0.18);', 'border-color: rgba(0, 0, 0, 0.1);')

# Other elements
css = css.replace('border: 1px solid rgba(255, 255, 255, 0.15)', 'border: 1px solid var(--border-subtle)')

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

# 2. Update Templates (Inline styles)
template_dir = r'c:\Users\SAJIN\OneDrive\Desktop\job\templates'
for filepath in glob.glob(os.path.join(template_dir, '*.html')):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Text colors
    html = html.replace('color:#fff;', 'color:var(--text-main);')
    html = html.replace('color: #fff;', 'color: var(--text-main);')
    html = html.replace('color: #e2e8f0;', 'color: var(--text-main);')
    html = html.replace('color: #cbd5e1;', 'color: var(--text-muted);')
    
    # Backgrounds and borders
    html = html.replace('rgba(255, 255, 255, 0.05)', 'rgba(0, 0, 0, 0.03)')
    html = html.replace('rgba(255, 255, 255, 0.08)', 'rgba(0, 0, 0, 0.05)')
    html = html.replace('rgba(255, 255, 255, 0.15)', 'rgba(0, 0, 0, 0.08)')
    html = html.replace('rgba(255, 255, 255, 0.1)', 'rgba(0, 0, 0, 0.06)')
    html = html.replace('rgba(255,255,255,.08)', 'rgba(0,0,0,.05)')
    html = html.replace('rgba(255,255,255,.15)', 'rgba(0,0,0,.08)')
    html = html.replace('background: rgba(16, 22, 38, 0.6);', 'background: var(--bg-surface);')
    html = html.replace('background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);', 'background:linear-gradient(135deg,#e0e7ff,#c7d2fe,#a5b4fc);')
    html = html.replace('background: linear-gradient(135deg, rgba(99, 102, 241, 0.18), rgba(6, 182, 212, 0.15));', 'background: linear-gradient(135deg, #f0fdfa, #e0e7ff);')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

print("Light theme applied globally.")