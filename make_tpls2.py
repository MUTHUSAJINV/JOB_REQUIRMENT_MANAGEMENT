import os
T = r'c:\Users\SAJIN\OneDrive\Desktop\job\templates'
def w(n,c): 
    c = c.replace('PCT1','{%').replace('PCT2','{{').replace('PCT3','}}')
    open(os.path.join(T,n),'w',encoding='utf-8').write(c); print('OK',n)

w('smart-recommendations.html',"""PCT1 extends 'base.html' PCT1
PCT1 block title PCT1Smart Job Recommendations | CareerPulsePCT1 endblock PCT1
PCT1 block content PCT1
<div style="background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);padding:3rem 0 2rem;text-align:center;">
 <div class="container">
  <h1 style="font-size:2.5rem;font-weight:800;color:#fff;">Smart Job <span style="background:linear-gradient(135deg,#f59e0b,#fbbf24);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Recommendations</span></h1>
  <p style="color:var(--text-muted);margin-top:.5rem;">AI-matched jobs based on your skills, experience and education.</p>
 </div>
</div>
<div class="container" style="padding:2.5rem 0;">
 PCT1 if profile PCT1
 <div class="card" style="margin-bottom:2rem;border-color:rgba(245,158,11,.2);">
  <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
   <div><h3 style="color:#fff;">Your Match Profile</h3><p style="color:var(--text-muted);font-size:.88rem;">Update profile to improve AI recommendations.</p></div>
   <a href="PCT2 url_for('profile') PCT3" class="btn btn-outline btn-sm" id="recs-update-btn">Update Profile</a>
  </div>
  <div style="display:flex;flex-wrap:wrap;gap:1rem;margin-top:1rem;">
   PCT1 if profile.skills PCT1<span class="badge" style="padding:.4rem .8rem;">Skills: PCT2 profile.skills[:60] PCT3</span>PCT1 endif PCT1
   PCT1 if profile.experience_years PCT1<span class="badge" style="padding:.4rem .8rem;">PCT2 profile.experience_years PCT3 yrs exp</span>PCT1 endif PCT1
   PCT1 if profile.degree PCT1<span class="badge" style="padding:.4rem .8rem;">PCT2 profile.degree PCT3</span>PCT1 endif PCT1
   PCT1 if profile.degree_percentage PCT1<span class="badge" style="padding:.4rem .8rem;">PCT2 profile.degree_percentage PCT3%</span>PCT1 endif PCT1
  </div>
 </div>
 PCT1 endif PCT1
 PCT1 if recommendations PCT1
 <h2 style="color:#fff;margin-bottom:1.5rem;">PCT2 recommendations|length PCT3 Jobs Matched For You</h2>
 <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:1.5rem;">
  PCT1 for rec in recommendations PCT1
  PCT1 set job = rec.job PCT1
  <div class="card" style="border-left:4px solid PCT1 if rec.score>=70 PCT1#10b981PCT1 elif rec.score>=40 PCT1#f59e0bPCT1 else PCT1#6366f1PCT1 endif PCT1;transition:transform .2s;" onmouseover="this.style.transform='translateY(-4px)'" onmouseout="this.style.transform=''">
   <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1rem;">
    <h3 style="color:#fff;font-size:1.05rem;">PCT2 job.title PCT3</h3>
    <span style="background:PCT1 if rec.score>=70 PCT1rgba(16,185,129,.15)PCT1 elif rec.score>=40 PCT1rgba(245,158,11,.15)PCT1 else PCT1rgba(99,102,241,.15)PCT1 endif PCT1;color:PCT1 if rec.score>=70 PCT1#34d399PCT1 elif rec.score>=40 PCT1#fbbf24PCT1 else PCT1#a5b4fcPCT1 endif PCT1;border-radius:1rem;padding:.2rem .7rem;font-size:.82rem;font-weight:700;white-space:nowrap;margin-left:.5rem;">PCT2 rec.score PCT3% match</span>
   </div>
   <p style="color:#6366f1;font-weight:600;font-size:.88rem;margin-bottom:.8rem;">PCT2 job.company_name or 'Company' PCT3</p>
   <div style="display:flex;flex-wrap:wrap;gap:.4rem;margin-bottom:.8rem;">
    PCT1 if job.location PCT1<span class="badge">PCT2 job.location PCT3</span>PCT1 endif PCT1
    PCT1 if job.job_type PCT1<span class="badge">PCT2 job.job_type PCT3</span>PCT1 endif PCT1
    PCT1 if job.salary PCT1<span class="badge badge-success">PCT2 job.salary PCT3</span>PCT1 endif PCT1
    <span class="badge">PCT2 job.total_vacancy or 1 PCT3 openings</span>
   </div>
   PCT1 if job.skills PCT1<div style="display:flex;flex-wrap:wrap;gap:.3rem;margin-bottom:1rem;">PCT1 for sk in job.skills.split(',')[:5] PCT1<span class="skill-tag" style="font-size:.75rem;">PCT2 sk.strip() PCT3</span>PCT1 endfor PCT1</div>PCT1 endif PCT1
   <a href="PCT2 url_for('job_details',job_id=job.id) PCT3" class="btn btn-primary" style="width:100%;text-align:center;" id="rec-view-PCT2 job.id PCT3">View &amp; Apply</a>
  </div>
  PCT1 endfor PCT1
 </div>
 PCT1 else PCT1
 <div class="card" style="text-align:center;padding:4rem;">
  <div style="font-size:3rem;margin-bottom:1rem;">&#x1F3AF;</div>
  <h3 style="color:#fff;">Complete your profile to get AI-matched jobs</h3>
  <p style="color:var(--text-muted);margin:.5rem 0 1.5rem;">Add your skills, degree, and experience to enable smart recommendations.</p>
  <a href="PCT2 url_for('profile') PCT3" class="btn btn-primary">Update Profile</a>
 </div>
 PCT1 endif PCT1
</div>
PCT1 endblock PCT1""")

w('skill-gap.html',"""PCT1 extends 'base.html' PCT1
PCT1 block title PCT1Skill Gap Analyzer | CareerPulsePCT1 endblock PCT1
PCT1 block content PCT1
<div style="background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);padding:3rem 0 2rem;text-align:center;">
 <div class="container">
  <h1 style="font-size:2.5rem;font-weight:800;color:#fff;">Skill Gap <span style="background:linear-gradient(135deg,#10b981,#34d399);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Analyzer</span></h1>
  <p style="color:var(--text-muted);margin-top:.5rem;">Discover what you need to land your dream role. Get learning resources.</p>
 </div>
</div>
<div class="container" style="padding:2.5rem 0;max-width:900px;margin:0 auto;">
 <div class="card" style="margin-bottom:2rem;">
  <h3 style="color:#10b981;margin-bottom:1.5rem;">Analyze Your Skill Gap</h3>
  <form method="POST" id="skill-gap-form">
   <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.2rem;margin-bottom:1.2rem;">
    <div class="form-group" style="margin-bottom:0;">
     <label class="form-label">Target Role *</label>
     <select name="target_role" class="form-control" id="sg-target-role" required>
      <option value="">-- Select target role --</option>
      PCT1 for role in ['Software Engineer','Frontend Developer','Backend Developer','Full Stack Developer','Data Scientist','Machine Learning Engineer','DevOps Engineer','UI/UX Designer','Cloud Architect','Mobile Developer','Cybersecurity Analyst','Product Manager'] PCT1
      <option value="PCT2 role PCT3">PCT2 role PCT3</option>PCT1 endfor PCT1
     </select>
    </div>
    <div class="form-group" style="margin-bottom:0;">
     <label class="form-label">Current Skills (optional)</label>
     <input type="text" name="current_skills" class="form-control" id="sg-skills" placeholder="Python, React, SQL..." value="PCT2 profile.skills if profile else '' PCT3">
    </div>
   </div>
   <button type="submit" class="btn btn-primary" id="sg-analyze-btn">Analyze Skill Gap</button>
  </form>
 </div>
 PCT1 if analysis PCT1
 <div class="card" style="margin-bottom:1.5rem;border-left:4px solid PCT1 if analysis.match_score>=70 PCT1#10b981PCT1 elif analysis.match_score>=40 PCT1#f59e0bPCT1 else PCT1#ef4444PCT1 endif PCT1;">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem;flex-wrap:wrap;gap:1rem;">
   <div><h2 style="color:#fff;">PCT2 analysis.target_role PCT3</h2><p style="color:var(--text-muted);">PCT2 analysis.present_skills|length PCT3 / PCT2 analysis.required_skills|length PCT3 skills matched</p></div>
   <div style="text-align:center;">
    <div style="font-size:2.5rem;font-weight:800;color:PCT1 if analysis.match_score>=70 PCT1#34d399PCT1 elif analysis.match_score>=40 PCT1#fbbf24PCT1 else PCT1#f87171PCT1 endif PCT1;">PCT2 analysis.match_score PCT3%</div>
    <div style="color:var(--text-muted);font-size:.82rem;">match score</div>
   </div>
  </div>
  <div style="background:rgba(255,255,255,.08);border-radius:1rem;height:8px;margin-bottom:1.5rem;overflow:hidden;">
   <div style="background:PCT1 if analysis.match_score>=70 PCT1#10b981PCT1 elif analysis.match_score>=40 PCT1#f59e0bPCT1 else PCT1#ef4444PCT1 endif PCT1;height:100%;width:PCT2 analysis.match_score PCT3%;border-radius:1rem;"></div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-bottom:1.5rem;">
   <div>
    <h4 style="color:#34d399;margin-bottom:.8rem;font-size:.9rem;">Skills You Have</h4>
    <div style="display:flex;flex-wrap:wrap;gap:.4rem;">
     PCT1 for sk in analysis.present_skills PCT1<span class="badge badge-success">PCT2 sk PCT3</span>PCT1 endfor PCT1
     PCT1 if not analysis.present_skills PCT1<p style="color:var(--text-muted);font-size:.88rem;">None yet. Update your profile.</p>PCT1 endif PCT1
    </div>
   </div>
   <div>
    <h4 style="color:#f87171;margin-bottom:.8rem;font-size:.9rem;">Skills to Acquire</h4>
    <div style="display:flex;flex-wrap:wrap;gap:.4rem;">
     PCT1 for sk in analysis.missing_skills PCT1<span class="badge" style="background:rgba(239,68,68,.15);color:#fca5a5;border:1px solid rgba(239,68,68,.3);">PCT2 sk PCT3</span>PCT1 endfor PCT1
     PCT1 if not analysis.missing_skills PCT1<p style="color:#34d399;font-size:.88rem;">You have all required skills!</p>PCT1 endif PCT1
    </div>
   </div>
  </div>
  PCT1 if analysis.recommendations PCT1
  <h4 style="color:#a5b4fc;margin-bottom:1rem;font-size:.9rem;">Learning Resources</h4>
  <div style="display:flex;flex-direction:column;gap:.6rem;">
   PCT1 for rec in analysis.recommendations PCT1
   <div style="display:flex;align-items:center;justify-content:space-between;background:rgba(99,102,241,.08);border:1px solid rgba(99,102,241,.2);border-radius:.6rem;padding:.7rem 1rem;">
    <span style="color:#fff;font-weight:500;">PCT2 rec.skill PCT3</span>
    <a href="PCT2 rec.resource PCT3" target="_blank" class="btn btn-outline btn-sm">Learn Now</a>
   </div>
   PCT1 endfor PCT1
  </div>
  PCT1 endif PCT1
 </div>
 PCT1 endif PCT1
 PCT1 if past_analyses PCT1
 <div class="card">
  <h3 style="color:#fff;margin-bottom:1.2rem;">Recent Analyses</h3>
  PCT1 for pa in past_analyses PCT1
  <div style="display:flex;justify-content:space-between;align-items:center;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:.6rem;padding:.7rem 1rem;margin-bottom:.5rem;">
   <span style="color:#fff;font-weight:500;">PCT2 pa.target_role PCT3 <span style="color:var(--text-muted);font-size:.82rem;">PCT2 pa.created_at[:10] PCT3</span></span>
   <span style="background:PCT1 if pa.match_score>=70 PCT1rgba(16,185,129,.15)PCT1 elif pa.match_score>=40 PCT1rgba(245,158,11,.15)PCT1 else PCT1rgba(239,68,68,.15)PCT1 endif PCT1;color:PCT1 if pa.match_score>=70 PCT1#34d399PCT1 elif pa.match_score>=40 PCT1#fbbf24PCT1 else PCT1#f87171PCT1 endif PCT1;border-radius:1rem;padding:.2rem .7rem;font-size:.82rem;font-weight:700;">PCT2 pa.match_score PCT3%</span>
  </div>
  PCT1 endfor PCT1
 </div>
 PCT1 endif PCT1
</div>
PCT1 endblock PCT1""")

print('Batch 2 done')