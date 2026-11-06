import os
T = r'c:\Users\SAJIN\OneDrive\Desktop\job\templates'
def w(n,c):
    # PCT1='{%', PCT2='{{', PCT3='}}', PCT4='%}'
    c = c.replace('PCT1','{%').replace('PCT4','%}').replace('PCT2','{{').replace('PCT3','}}')
    open(os.path.join(T,n),'w',encoding='utf-8').write(c)
    print('FIXED',n)

# Fix internships.html - was written by old script with wrong placeholders
w('internships.html',"""PCT1 extends 'base.html' PCT4
PCT1 block title PCT4Internships | CareerPulsePCT1 endblock PCT4
PCT1 block content PCT4
<div style="background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);padding:3rem 0 2rem;text-align:center;">
 <div class="container">
  <h1 style="font-size:2.5rem;font-weight:800;color:#fff;">Internship <span style="background:linear-gradient(135deg,#6366f1,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Opportunities</span></h1>
  <p style="color:var(--text-muted);margin-top:.5rem;">Real-world experience with leading companies. Build your portfolio.</p>
 </div>
</div>
<div class="container" style="padding:2.5rem 0;">
 PCT1 if internships PCT4
 <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:1.5rem;">
  PCT1 for job in internships PCT4
  <div class="card" style="border-left:4px solid #6366f1;transition:transform .2s;" onmouseover="this.style.transform='translateY(-4px)'" onmouseout="this.style.transform=''">
   <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1rem;">
    <div style="background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:.7rem;padding:.6rem;font-size:1.3rem;">&#127891;</div>
    <span class="badge" style="background:rgba(99,102,241,.15);color:#a5b4fc;border:1px solid rgba(99,102,241,.3);">INTERNSHIP</span>
   </div>
   <h3 style="color:#fff;font-size:1.1rem;margin-bottom:.3rem;">PCT2 job.title PCT3</h3>
   <p style="color:#6366f1;font-weight:600;margin-bottom:.8rem;">PCT2 job.company_name or 'Company' PCT3</p>
   <div style="display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:1rem;">
    PCT1 if job.location PCT4<span class="badge">&#x1F4CD; PCT2 job.location PCT3</span>PCT1 endif PCT4
    PCT1 if job.internship_duration PCT4<span class="badge" style="background:rgba(6,182,212,.15);color:#67e8f9;">&#x23F1; PCT2 job.internship_duration PCT3</span>PCT1 endif PCT4
    PCT1 if job.stipend PCT4<span class="badge badge-success">&#x1F4B0; PCT2 job.stipend PCT3</span>PCT1 endif PCT4
    <span class="badge" style="background:rgba(251,191,36,.15);color:#fde68a;">PCT2 job.total_vacancy or 1 PCT3 openings</span>
   </div>
   <p style="color:var(--text-muted);font-size:.9rem;margin-bottom:1.2rem;">PCT2 job.description[:120] PCT3...</p>
   PCT1 if job.skills PCT4
   <div style="display:flex;flex-wrap:wrap;gap:.4rem;margin-bottom:1rem;">
    PCT1 for sk in job.skills.split(',')[:4] PCT4<span class="skill-tag">PCT2 sk.strip() PCT3</span>PCT1 endfor PCT4
   </div>
   PCT1 endif PCT4
   <a href="PCT2 url_for('job_details', job_id=job.id) PCT3" class="btn btn-primary" style="width:100%;text-align:center;">View &amp; Apply</a>
  </div>
  PCT1 endfor PCT4
 </div>
 PCT1 else PCT4
 <div class="card" style="text-align:center;padding:4rem;">
  <div style="font-size:3rem;margin-bottom:1rem;">&#127891;</div>
  <h3 style="color:#fff;margin-bottom:.5rem;">No internships available right now</h3>
  <p style="color:var(--text-muted);margin-bottom:1.5rem;">Check back soon or browse all open positions.</p>
  <a href="PCT2 url_for('jobs') PCT3" class="btn btn-primary">Browse All Jobs</a>
 </div>
 PCT1 endif PCT4
</div>
PCT1 endblock PCT4""")

# Also check and fix all other templates - ensure they have proper {% %} syntax
import re
other = ['messages.html','compose-message.html','view-message.html','report-fraud.html',
         'admin-fraud-reports.html','smart-recommendations.html','skill-gap.html',
         'resume-builder.html','resume-preview.html','coding-tests.html',
         'take-test.html','mock-interview.html','mock-interview-session.html']
for fname in other:
    path = os.path.join(T, fname)
    with open(path, encoding='utf-8') as f:
        content = f.read()
    # Fix pattern: {%...{%  should be {%...%}
    # The make_tpls scripts used PCT1='{%' and  PCT4 not set, so closing was missing
    # Check for malformed blocks: '{%' followed eventually by '{%' without '%}'
    fixed = re.sub(r'\{%([^%]*)\{%', r'{%\1%}', content)  # fix {%...{%
    if fixed != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(fixed)
        print(f'PATCHED {fname}')
    else:
        print(f'OK {fname}')