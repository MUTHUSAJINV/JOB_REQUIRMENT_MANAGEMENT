import os

css_path = r'c:\Users\SAJIN\OneDrive\Desktop\job\static\css\style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# We will replace the entire variable block
root_start = css.find(':root, [data-theme="dark"] {')
root_end = css.find('/* Base Reset */')

if root_start != -1 and root_end != -1:
    new_vars = """
:root, [data-theme="dark"] {
  /* Colors - Sky Blue Dark Theme */
  --bg-dark: #040f1a;
  --bg-surface: #0a192f;
  --bg-card: #0d213b;
  --bg-card-hover: #122b4a;
  --bg-glass: rgba(10, 25, 47, 0.75);
  --border-subtle: rgba(56, 189, 248, 0.15);
  --border-focus: rgba(14, 165, 233, 0.5);

  --text-main: #f0f9ff;
  --text-muted: #bae6fd;
  --text-subtle: #7dd3fc;

  /* Accents - Sky Blue focused */
  --primary: #0ea5e9;
  --primary-hover: #0284c7;
  --primary-light: rgba(14, 165, 233, 0.2);
  --secondary: #38bdf8;
  --secondary-hover: #0ea5e9;
  --secondary-light: rgba(56, 189, 248, 0.2);
  
  --accent-purple: #818cf8;
  --accent-emerald: #34d399;
  --accent-amber: #fbbf24;
  --accent-rose: #fb7185;

  /* Status Colors */
  --status-applied: #38bdf8;
  --status-applied-bg: rgba(56, 189, 248, 0.15);
  --status-shortlisted: #fbbf24;
  --status-shortlisted-bg: rgba(251, 191, 36, 0.15);
  --status-interview: #818cf8;
  --status-interview-bg: rgba(129, 140, 248, 0.15);
  --status-selected: #34d399;
  --status-selected-bg: rgba(52, 211, 153, 0.15);
  --status-rejected: #fb7185;
  --status-rejected-bg: rgba(251, 113, 133, 0.15);

  /* Shadows */
  --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 16px 40px rgba(0, 0, 0, 0.5);
  --glow-primary: 0 0 24px rgba(14, 165, 233, 0.35);

  /* Custom Backgrounds for templates */
  --bg-gradient-hero: linear-gradient(135deg, rgba(14, 165, 233, 0.15), rgba(56, 189, 248, 0.1));
  --bg-gradient-header: linear-gradient(135deg, #071a2f, #0d2a4a, #040f1a);
  --bg-rgba-5: rgba(255,255,255,0.05);
  --bg-rgba-8: rgba(255,255,255,0.08);

  /* Layout */
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 20px;
  --radius-full: 9999px;
  --transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

[data-theme="light"] {
  --bg-dark: #f0f9ff;
  --bg-surface: #ffffff;
  --bg-card: #ffffff;
  --bg-card-hover: #f0f9ff;
  --bg-glass: rgba(255, 255, 255, 0.85);
  --border-subtle: rgba(14, 165, 233, 0.2);
  --border-focus: rgba(14, 165, 233, 0.5);

  --text-main: #0c4a6e;
  --text-muted: #0369a1;
  --text-subtle: #0284c7;

  --primary: #0ea5e9;
  --primary-hover: #0284c7;
  --primary-light: rgba(14, 165, 233, 0.15);
  --secondary: #38bdf8;
  --secondary-hover: #0ea5e9;
  --secondary-light: rgba(56, 189, 248, 0.15);

  --shadow-sm: 0 2px 4px rgba(14, 165, 233, 0.05);
  --shadow-md: 0 8px 24px rgba(14, 165, 233, 0.1);
  --shadow-lg: 0 16px 40px rgba(14, 165, 233, 0.15);
  --glow-primary: 0 0 24px rgba(14, 165, 233, 0.2);

  --bg-gradient-hero: linear-gradient(135deg, #e0f2fe, #bae6fd);
  --bg-gradient-header: linear-gradient(135deg, #e0f2fe, #bae6fd, #e0f2fe);
  --bg-rgba-5: rgba(0,0,0,0.03);
  --bg-rgba-8: rgba(0,0,0,0.06);
}
"""
    css = css[:root_start] + new_vars + css[root_end:]
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)
    print("Sky Blue Dark UI applied.")
else:
    print("Failed to find CSS block")