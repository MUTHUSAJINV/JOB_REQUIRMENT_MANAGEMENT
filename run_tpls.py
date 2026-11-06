import os, sys
T = r'c:\Users\SAJIN\OneDrive\Desktop\job\templates'
def w(n,c):
    with open(os.path.join(T,n),'w',encoding='utf-8') as f: f.write(c)
    print('Wrote', n, os.path.getsize(os.path.join(T,n)))
import importlib.util
spec = importlib.util.spec_from_file_location('tpl_data', r'c:\Users\SAJIN\OneDrive\Desktop\job\tpl_data.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for name, content in mod.templates.items():
    w(name, content)
print('ALL TEMPLATES WRITTEN')