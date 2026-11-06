import os

path = r'c:\Users\SAJIN\OneDrive\Desktop\job\templates\index.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

styles = """
<style>
/* Front Page Animations */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes scaleUp {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}

.anim-fade-up { opacity: 0; animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
.anim-fade-down { opacity: 0; animation: fadeInDown 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
.anim-scale-up { opacity: 0; animation: scaleUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
.anim-float { animation: float 4s ease-in-out infinite; }

.delay-100 { animation-delay: 100ms; }
.delay-200 { animation-delay: 200ms; }
.delay-300 { animation-delay: 300ms; }
.delay-400 { animation-delay: 400ms; }
.delay-500 { animation-delay: 500ms; }
.delay-600 { animation-delay: 600ms; }
</style>
"""

# Replace tags to add animation classes
content = content.replace('{% block content %}', '{% block content %}' + styles)

content = content.replace('class="hero-pill"', 'class="hero-pill anim-fade-down"')
content = content.replace('class="hero-title"', 'class="hero-title anim-fade-up delay-100"')
content = content.replace('class="hero-subtitle"', 'class="hero-subtitle anim-fade-up delay-200"')
content = content.replace('class="search-box"', 'class="search-box anim-fade-up delay-300"')
content = content.replace('<!-- AI Analyzer Spotlight Banner -->\n    <div style="max-width', '<!-- AI Analyzer Spotlight Banner -->\n    <div class="anim-scale-up delay-400" style="max-width')

# Stat cards
content = content.replace('<div class="stat-card" style="--stat-glow: rgba(99, 102, 241, 0.2);">', '<div class="stat-card anim-fade-up delay-300 anim-float" style="--stat-glow: rgba(99, 102, 241, 0.2);">')
content = content.replace('<div class="stat-card" style="--stat-glow: rgba(6, 182, 212, 0.2);">', '<div class="stat-card anim-fade-up delay-400 anim-float" style="--stat-glow: rgba(6, 182, 212, 0.2); animation-delay: 400ms, 200ms;">')
content = content.replace('<div class="stat-card" style="--stat-glow: rgba(168, 85, 247, 0.2);">', '<div class="stat-card anim-fade-up delay-500 anim-float" style="--stat-glow: rgba(168, 85, 247, 0.2); animation-delay: 500ms, 400ms;">')
content = content.replace('<div class="stat-card" style="--stat-glow: rgba(16, 185, 129, 0.2);">', '<div class="stat-card anim-fade-up delay-600 anim-float" style="--stat-glow: rgba(16, 185, 129, 0.2); animation-delay: 600ms, 600ms;">')

# Featured jobs header
content = content.replace('class="page-title"', 'class="page-title anim-fade-up"')
content = content.replace('class="page-subtitle"', 'class="page-subtitle anim-fade-up delay-100"')

# Job cards
content = content.replace('<div class="job-card">', '<div class="job-card anim-fade-up delay-200">')

# Bottom section cards
content = content.replace('class="card" style="border-top: 3px solid #38bdf8;"', 'class="card anim-fade-up delay-300" style="border-top: 3px solid #38bdf8;"')
content = content.replace('class="card" style="border-top: 3px solid #c084fc;"', 'class="card anim-fade-up delay-400" style="border-top: 3px solid #c084fc;"')
content = content.replace('class="card" style="border-top: 3px solid #fbbf24;"', 'class="card anim-fade-up delay-500" style="border-top: 3px solid #fbbf24;"')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Animations applied.")