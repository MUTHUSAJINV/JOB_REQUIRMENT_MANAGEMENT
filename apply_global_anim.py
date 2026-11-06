import os

index_path = r'c:\Users\SAJIN\OneDrive\Desktop\job\templates\index.html'
base_path = r'c:\Users\SAJIN\OneDrive\Desktop\job\templates\base.html'

with open(index_path, 'r', encoding='utf-8') as f:
    index_html = f.read()

# Extract the additions
canvas_html = '<!-- Interactive Canvas Background -->\n<canvas id="bg-canvas"></canvas>'
style_start = index_html.find('#bg-canvas {')
style_end = index_html.find('/* Scroll Animation Classes */')

js_start = index_html.find('<script>\n// --- Canvas Particle/Network System ---')
js_end = index_html.find('</script>', js_start) + 9

if style_start != -1 and js_start != -1:
    # 1. Clean index.html
    style_block = index_html[style_start:style_end]
    js_block = index_html[js_start:js_end]
    
    clean_index = index_html.replace(canvas_html, '')
    clean_index = clean_index.replace(style_block, '')
    clean_index = clean_index.replace(js_block, '')
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(clean_index)
        
    # 2. Inject into base.html
    with open(base_path, 'r', encoding='utf-8') as f:
        base_html = f.read()
        
    # Inject Canvas right after <body>
    if canvas_html not in base_html:
        base_html = base_html.replace('<body', canvas_html + '\n<body')
        
    # Inject CSS into <head>
    if '#bg-canvas {' not in base_html:
        css_inject = f"<style>\n{style_block}\n</style>"
        base_html = base_html.replace('</head>', css_inject + '\n</head>')
        
    # Inject JS before </body>
    if '// --- Canvas Particle/Network System ---' not in base_html:
        base_html = base_html.replace('</body>', js_block + '\n</body>')
        
    # Make sure body has a transparent background so canvas shows through
    if 'body {' not in base_html: # if inline styling isn't there, we just add it to css_inject
        pass 
        
    with open(base_path, 'w', encoding='utf-8') as f:
        f.write(base_html)

    print("Global animation applied to base.html")
else:
    print("Could not find blocks in index.html")
