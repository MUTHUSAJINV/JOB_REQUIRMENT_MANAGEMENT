import os
path = r'c:\Users\SAJIN\OneDrive\Desktop\job\app.py'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# find if __name__=="__main__":
idx = -1
for i, line in enumerate(lines):
    if line.startswith('if __name__=="__main__":'):
        idx = i
        break

if idx != -1:
    main_block = lines[idx:idx+4]
    # remove main block from current position
    lines = lines[:idx] + lines[idx+4:]
    # append main block to the end
    lines.extend(main_block)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Fixed order")