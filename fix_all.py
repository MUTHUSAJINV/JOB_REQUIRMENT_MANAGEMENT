import os, re
T = r'c:\Users\SAJIN\OneDrive\Desktop\job\templates'

# Validate each template by checking for known bad patterns
issues = []
for fname in os.listdir(T):
    if not fname.endswith('.html'): continue
    path = os.path.join(T, fname)
    with open(path, encoding='utf-8') as f:
        c = f.read()
    # Count opening {%  vs closing %}
    opens = c.count('{%')
    closes = c.count('%}')
    if opens != closes:
        issues.append(f'MISMATCH {fname}: {opens} opens vs {closes} closes')
    elif '{%{%' in c or re.search(r'\{%[^%]*\{%', c):
        issues.append(f'NESTED_BLOCK {fname}')
    else:
        print(f'OK  {fname}: {opens} blocks matched')

if issues:
    print()
    for i in issues: print('  ', i)
else:
    print()
    print('All templates valid!')