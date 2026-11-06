import os
T = r'c:\Users\SAJIN\OneDrive\Desktop\job\templates'

with open(os.path.join(T, 'base.html'), 'r', encoding='utf-8') as f:
    content = f.read()

# I want to rewrite the body of base.html.
# Instead of replacing strings, I will write the whole file since it's around 165 lines.

base_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}CareerPulse | Modern Job Portal & Hiring Platform{% endblock %}</title>
  <meta name="description" content="Next-generation job search, AI resume analysis, recruiter management, and candidate tracking system.">
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
</head>
<body>

{% if session.get('role') == 'seeker' %}
  <!-- SEEKER PORTAL LAYOUT (Sidebar + Topbar) -->
  <div class="seeker-layout">
    <!-- Left Sidebar -->
    <aside class="seeker-sidebar">
      <div class="sidebar-brand">
        <div class="logo-icon" style="width:28px;height:28px;margin-right:8px;">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
            <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
          </svg>
        </div>
        Career<span class="brand-accent">Pulse</span>
      </div>
      <ul class="sidebar-links">
        <li><a href="{{ url_for('seeker_dashboard') }}" class="nav-link {% if request.endpoint == 'seeker_dashboard' %}active{% endif %}">Dashboard</a></li>
        <li><a href="{{ url_for('jobs') }}" class="nav-link {% if request.endpoint == 'jobs' %}active{% endif %}">Search Jobs</a></li>
        <li><a href="{{ url_for('smart_recommendations') }}" class="nav-link {% if request.endpoint == 'smart_recommendations' %}active{% endif %}">🎯 Smart Jobs</a></li>
        <li><a href="{{ url_for('resume_analyzer') }}" class="nav-link {% if request.endpoint in ['resume_analyzer','analyzer'] %}active{% endif %}">✨ AI Analyzer</a></li>
        <li><a href="{{ url_for('resume_builder') }}" class="nav-link {% if request.endpoint in ['resume_builder','resume_builder_preview'] %}active{% endif %}">📄 Resume Builder</a></li>
        <li><a href="{{ url_for('skill_gap') }}" class="nav-link {% if request.endpoint == 'skill_gap' %}active{% endif %}">📊 Skill Gap</a></li>
        <li><a href="{{ url_for('coding_tests') }}" class="nav-link {% if request.endpoint in ['coding_tests','take_test'] %}active{% endif %}">💻 Coding Tests</a></li>
        <li><a href="{{ url_for('mock_interview') }}" class="nav-link {% if request.endpoint in ['mock_interview','start_mock_interview'] %}active{% endif %}">🎤 Mock Interview</a></li>
        <li><a href="{{ url_for('messages') }}" class="nav-link {% if request.endpoint in ['messages','compose_message','view_message'] %}active{% endif %}">✉️ Messages</a></li>
        <li><a href="{{ url_for('internships') }}" class="nav-link {% if request.endpoint == 'internships' %}active{% endif %}">🎓 Internships</a></li>
        <li><a href="{{ url_for('profile') }}" class="nav-link {% if request.endpoint == 'profile' %}active{% endif %}">Profile</a></li>
      </ul>
    </aside>

    <!-- Main Content Area -->
    <div class="seeker-main-wrapper">
      <!-- Topbar -->
      <header class="seeker-topbar">
        <div class="topbar-center">
          <h2>CareerPulse Portal</h2>
        </div>
        <div class="topbar-right">
          <span class="user-name">👤 {{ session.get('name') }}</span>
          <a href="{{ url_for('logout') }}" class="btn btn-outline btn-sm" id="nav-logout-btn">Log Out</a>
        </div>
      </header>

      <!-- Main Body -->
      <main class="seeker-content">
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            <div class="flash-container">
              {% for category, message in messages %}
                <div class="alert alert-{{ category }}">
                  <div style="display: flex; align-items: center; gap: 0.6rem;">
                    <span>{{ message }}</span>
                  </div>
                  <button class="alert-close" aria-label="Close alert">&times;</button>
                </div>
              {% endfor %}
            </div>
          {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
      </main>
      
      <!-- Footer -->
      <footer class="footer seeker-footer">
        <div class="container" style="text-align:center; padding:1rem;">
          <div style="color:var(--text-muted); font-size:0.85rem;">&copy; 2026 CareerPulse Technologies Inc. All rights reserved.</div>
        </div>
      </footer>
    </div>
  </div>

{% else %}
  <!-- ORIGINAL NAVIGATION FOR NON-SEEKERS -->
  <nav class="navbar">
    <div class="nav-container">
      <a href="{{ url_for('index') }}" class="brand-logo" id="nav-brand-logo">
        <div class="logo-icon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
            <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
          </svg>
        </div>
        <span>Career<span class="brand-accent">Pulse</span></span>
      </a>

      <ul class="nav-links">
        <li><a href="{{ url_for('jobs') }}" class="nav-link {% if request.endpoint == 'jobs' %}active{% endif %}">Find Jobs</a></li>
        
        {% if session.get('role') == 'recruiter' %}
          <li><a href="{{ url_for('recruiter_dashboard') }}" class="nav-link {% if request.endpoint == 'recruiter_dashboard' %}active{% endif %}">Job Postings</a></li>
          <li><a href="{{ url_for('recruiter_applicants') }}" class="nav-link {% if request.endpoint == 'recruiter_applicants' %}active{% endif %}">Candidates</a></li>
          <li><a href="{{ url_for('recruiter_company') }}" class="nav-link {% if request.endpoint == 'recruiter_company' %}active{% endif %}">Company Profile</a></li>
          <li><a href="{{ url_for('messages') }}" class="nav-link {% if request.endpoint in ['messages','compose_message','view_message'] %}active{% endif %}">✉️ Messages</a></li>
        {% elif session.get('role') == 'admin' %}
          <li><a href="{{ url_for('admin_dashboard') }}" class="nav-link {% if request.endpoint == 'admin_dashboard' %}active{% endif %}">Overview</a></li>
          <li><a href="{{ url_for('admin_users') }}" class="nav-link {% if request.endpoint == 'admin_users' %}active{% endif %}">Users</a></li>
          <li><a href="{{ url_for('admin_jobs') }}" class="nav-link {% if request.endpoint == 'admin_jobs' %}active{% endif %}">Jobs</a></li>
          <li><a href="{{ url_for('admin_fraud_reports') }}" class="nav-link {% if request.endpoint == 'admin_fraud_reports' %}active{% endif %}">🚨 Fraud Reports</a></li>
          <li><a href="{{ url_for('messages') }}" class="nav-link {% if request.endpoint in ['messages','compose_message','view_message'] %}active{% endif %}">✉️ Messages</a></li>
        {% endif %}
      </ul>

      <div class="nav-actions">
        {% if session.get('user_id') %}
          <div class="user-badge">
            <span>{{ session.get('name') }}</span>
            <span class="role-tag {{ session.get('role') }}">{{ session.get('role') }}</span>
          </div>

          {% if session.get('role') == 'recruiter' %}
            <a href="{{ url_for('create_job') }}" class="btn btn-primary btn-sm" id="nav-post-job-btn">
              Post a Job
            </a>
          {% endif %}

          <a href="{{ url_for('logout') }}" class="btn btn-outline btn-sm" id="nav-logout-btn">Log Out</a>
        {% else %}
          <a href="{{ url_for('login') }}" class="btn btn-outline btn-sm" id="nav-login-btn">Log In</a>
          <a href="{{ url_for('register') }}" class="btn btn-primary btn-sm" id="nav-register-btn">Get Started</a>
        {% endif %}
      </div>
    </div>
  </nav>

  <!-- Flash Toast Notifications -->
  {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      <div class="flash-container">
        {% for category, message in messages %}
          <div class="alert alert-{{ category }}">
            <div style="display: flex; align-items: center; gap: 0.6rem;">
              <span>{{ message }}</span>
            </div>
            <button class="alert-close" aria-label="Close alert">&times;</button>
          </div>
        {% endfor %}
      </div>
    {% endif %}
  {% endwith %}

  <!-- Main Body Content -->
  <main class="main-content">
    {% block content %}{% endblock %}
  </main>

  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col">
          <div class="brand-logo" style="margin-bottom: 0.8rem;">
            <div class="logo-icon" style="width: 32px; height: 32px;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="2" y="7" width="20" height="14" rx="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>
            </div>
            <span>Career<span class="brand-accent">Pulse</span></span>
          </div>
          <p style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.6; max-width: 340px;">
            The all-in-one recruitment ecosystem.
          </p>
        </div>
      </div>
      <div class="footer-bottom">
        <div>&copy; 2026 CareerPulse Technologies Inc. All rights reserved.</div>
      </div>
    </div>
  </footer>
{% endif %}

  <script src="{{ url_for('static', filename='js/main.js') }}"></script>
  {% block scripts %}{% endblock %}
</body>
</html>
"""

with open(os.path.join(T, 'base.html'), 'w', encoding='utf-8') as f:
    f.write(base_content)

# Now inject the CSS for the seeker layout into style.css
css_addition = """
/* ==========================================================================
   SEEKER PORTAL SPECIFIC LAYOUT (Sidebar + Topbar)
   ========================================================================== */
.seeker-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.seeker-sidebar {
  width: 260px;
  background: var(--bg-surface);
  border-right: 1px solid var(--border-subtle);
  display: flex;
  flex-direction: column;
  padding: 1.5rem 0;
  flex-shrink: 0;
}

.sidebar-brand {
  padding: 0 1.5rem;
  font-size: 1.3rem;
  font-weight: 800;
  color: #fff;
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
}

.sidebar-links {
  list-style: none;
  padding: 0 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  overflow-y: auto;
}

.sidebar-links .nav-link {
  padding: 0.75rem 1rem;
  border-radius: var(--radius-sm);
  color: var(--text-muted);
  transition: all 0.2s;
  font-weight: 500;
  display: flex;
  align-items: center;
}

.sidebar-links .nav-link:hover, .sidebar-links .nav-link.active {
  background: rgba(99, 102, 241, 0.15);
  color: #fff;
}

.seeker-main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  background: var(--bg-dark);
}

.seeker-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  background: var(--bg-glass);
  border-bottom: 1px solid var(--border-subtle);
  backdrop-filter: blur(16px);
  position: sticky;
  top: 0;
  z-index: 10;
}

.topbar-center h2 {
  font-size: 1.2rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.5px;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-left: auto;
}

.user-name {
  font-weight: 600;
  color: #fff;
  font-size: 0.95rem;
}

.seeker-content {
  flex: 1;
  padding: 0;
}

.seeker-footer {
  margin-top: auto;
}
"""

with open(r'c:\Users\SAJIN\OneDrive\Desktop\job\static\css\style.css', 'a', encoding='utf-8') as f:
    f.write(css_addition)
print('Layout updated successfully')