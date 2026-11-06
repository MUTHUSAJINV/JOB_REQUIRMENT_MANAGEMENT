import os

css_path = r'c:\Users\SAJIN\OneDrive\Desktop\job\static\css\style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Swap the root variables to make Dark the default
new_css = css.replace(':root, [data-theme="light"] {', '/* temp_light */')
new_css = new_css.replace('[data-theme="dark"] {', ':root, [data-theme="dark"] {')
new_css = new_css.replace('/* temp_light */', '[data-theme="light"] {')

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(new_css)

base_path = r'c:\Users\SAJIN\OneDrive\Desktop\job\templates\base.html'
with open(base_path, 'r', encoding='utf-8') as f:
    base = f.read()

# Default to dark instead of auto-detecting light
base = base.replace("const savedTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');",
                    "const savedTheme = localStorage.getItem('theme') || 'dark';")

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(base)

print("Defaulted to attractable dark UI.")