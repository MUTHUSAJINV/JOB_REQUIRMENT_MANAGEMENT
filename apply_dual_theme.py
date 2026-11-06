import os, glob

# 1. Update style.css
css_path = r'c:\Users\SAJIN\OneDrive\Desktop\job\static\css\style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# We will replace the entire :root block with a new dynamic one.
root_start = css.find(':root {')
root_end = css.find('/* Base Reset */')

if root_start != -1 and root_end != -1:
    new_vars = """
:root, [data-theme="light"] {
  /* Colors - Light Theme */
  --bg-dark: #f4f7fb;
  --bg-surface: #ffffff;
  --bg-card: #ffffff;
  --bg-card-hover: #f8fafc;
  --bg-glass: rgba(255, 255, 255, 0.85);
  --border-subtle: rgba(148, 163, 184, 0.25);
  --border-focus: rgba(99, 102, 241, 0.5);

  --text-main: #0f172a;
  --text-muted: #475569;
  --text-subtle: #64748b;

  /* Accents */
  --primary: #6366f1;
  --primary-hover: #4f46e5;
  --primary-light: rgba(99, 102, 241, 0.15);
  --secondary: #06b6d4;
  --secondary-hover: #0891b2;
  --secondary-light: rgba(6, 182, 212, 0.15);
  --accent-purple: #a855f7;
  --accent-emerald: #10b981;
  --accent-amber: #f59e0b;
  --accent-rose: #f43f5e;

  /* Status Colors */
  --status-applied: #38bdf8;
  --status-applied-bg: rgba(56, 189, 248, 0.12);
  --status-shortlisted: #fbbf24;
  --status-shortlisted-bg: rgba(251, 191, 36, 0.12);
  --status-interview: #c084fc;
  --status-interview-bg: rgba(192, 132, 252, 0.15);
  --status-selected: #34d399;
  --status-selected-bg: rgba(52, 211, 153, 0.15);
  --status-rejected: #fb7185;
  --status-rejected-bg: rgba(251, 113, 133, 0.12);

  /* Shadows */
  --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 16px 40px rgba(0, 0, 0, 0.12);
  --glow-primary: 0 0 24px rgba(99, 102, 241, 0.2);

  /* Custom Backgrounds for templates */
  --bg-gradient-hero: linear-gradient(135deg, #f0fdfa, #e0e7ff);
  --bg-gradient-header: linear-gradient(135deg, #e0e7ff, #c7d2fe, #a5b4fc);
  --bg-rgba-5: rgba(0,0,0,0.05);
  --bg-rgba-8: rgba(0,0,0,0.08);

  /* Layout */
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 20px;
  --radius-full: 9999px;
  --transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

[data-theme="dark"] {
  --bg-dark: #090d16;
  --bg-surface: #101626;
  --bg-card: #151d30;
  --bg-card-hover: #1b253d;
  --bg-glass: rgba(21, 29, 48, 0.75);
  --border-subtle: rgba(255, 255, 255, 0.08);

  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --text-subtle: #64748b;

  --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.2);
  --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.35);
  --shadow-lg: 0 16px 40px rgba(0, 0, 0, 0.45);
  --glow-primary: 0 0 24px rgba(99, 102, 241, 0.3);

  --bg-gradient-hero: linear-gradient(135deg, rgba(99, 102, 241, 0.18), rgba(6, 182, 212, 0.15));
  --bg-gradient-header: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
  --bg-rgba-5: rgba(255,255,255,0.05);
  --bg-rgba-8: rgba(255,255,255,0.08);
}
"""
    css = css[:root_start] + new_vars + css[root_end:]
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)


# 2. Add Theme Toggle to base.html & Inject script
base_path = r'c:\Users\SAJIN\OneDrive\Desktop\job\templates\base.html'
with open(base_path, 'r', encoding='utf-8') as f:
    base_html = f.read()

toggle_html = """
          <button id="theme-toggle" class="btn btn-outline btn-sm" style="padding:0.4rem; border-radius:50%; width:34px; height:34px; display:flex; align-items:center; justify-content:center;">
            <svg id="theme-icon-light" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display:none;"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
            <svg id="theme-icon-dark" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
          </button>
"""

# Insert into Seeker Topbar
if 'id="nav-logout-btn"' in base_html:
    base_html = base_html.replace('id="nav-logout-btn">Log Out</a>', 'id="nav-logout-btn">Log Out</a>\n' + toggle_html)
elif '<a href="{{ url_for(\'login\') }}"' in base_html:
    # Insert for non-logged in users
    base_html = base_html.replace('<a href="{{ url_for(\'login\') }}"', toggle_html + '\n          <a href="{{ url_for(\'login\') }}"')

# Add theme script
theme_script = """
  <script>
    const toggleBtn = document.getElementById('theme-toggle');
    const iconLight = document.getElementById('theme-icon-light');
    const iconDark = document.getElementById('theme-icon-dark');
    
    // Check saved theme
    const savedTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateIcon(savedTheme);

    if(toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        let currentTheme = document.documentElement.getAttribute('data-theme');
        let newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateIcon(newTheme);
      });
    }

    function updateIcon(theme) {
      if(!iconLight || !iconDark) return;
      if (theme === 'dark') {
        iconLight.style.display = 'block';
        iconDark.style.display = 'none';
      } else {
        iconLight.style.display = 'none';
        iconDark.style.display = 'block';
      }
    }
  </script>
"""
if "const toggleBtn =" not in base_html:
    base_html = base_html.replace('</body>', theme_script + '\n</body>')

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(base_html)

# 3. Update Templates to use CSS variables for inline backgrounds
template_dir = r'c:\Users\SAJIN\OneDrive\Desktop\job\templates'
for filepath in glob.glob(os.path.join(template_dir, '*.html')):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    html = html.replace('background:linear-gradient(135deg,#e0e7ff,#c7d2fe,#a5b4fc);', 'background:var(--bg-gradient-header);')
    html = html.replace('background: linear-gradient(135deg, #f0fdfa, #e0e7ff);', 'background:var(--bg-gradient-hero);')
    html = html.replace('rgba(0, 0, 0, 0.05)', 'var(--bg-rgba-5)')
    html = html.replace('rgba(0,0,0,.05)', 'var(--bg-rgba-5)')
    html = html.replace('rgba(0, 0, 0, 0.08)', 'var(--bg-rgba-8)')
    html = html.replace('rgba(0,0,0,.08)', 'var(--bg-rgba-8)')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

print("Dual Theme setup complete.")