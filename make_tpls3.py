import os
T = r'c:\Users\SAJIN\OneDrive\Desktop\job\templates'
def w(n,c): 
    c = c.replace('PCT1','{%').replace('PCT2','{{').replace('PCT3','}}')
    open(os.path.join(T,n),'w',encoding='utf-8').write(c); print('OK',n)

w('resume-builder.html',"""PCT1 extends 'base.html' PCT1
PCT1 block title PCT1Resume Builder | CareerPulsePCT1 endblock PCT1
PCT1 block content PCT1
<div style="background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);padding:3rem 0 2rem;text-align:center;">
 <div class="container">
  <h1 style="font-size:2.5rem;font-weight:800;color:#fff;">Professional <span style="background:linear-gradient(135deg,#10b981,#34d399);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Resume Builder</span></h1>
  <p style="color:var(--text-muted);margin-top:.5rem;">Build, preview and download your resume in minutes.</p>
 </div>
</div>
<div class="container" style="padding:2.5rem 0;">
 <form method="POST" id="resume-builder-form">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;">
   <div style="display:flex;flex-direction:column;gap:1.5rem;">
    <div class="card">
     <h3 style="color:#10b981;margin-bottom:1.2rem;">Personal Information</h3>
     <div class="form-group"><label class="form-label">Full Name *</label><input type="text" name="full_name" class="form-control" value="PCT2 saved_data.full_name if saved_data else (profile.name if profile else '') PCT3" required></div>
     <div class="form-group"><label class="form-label">Email *</label><input type="email" name="email" class="form-control" value="PCT2 saved_data.email if saved_data else (profile.email if profile else '') PCT3" required></div>
     <div class="form-group"><label class="form-label">Phone</label><input type="text" name="phone" class="form-control" value="PCT2 saved_data.phone if saved_data else (profile.phone if profile else '') PCT3"></div>
     <div class="form-group"><label class="form-label">Location</label><input type="text" name="location" class="form-control" value="PCT2 saved_data.location if saved_data else (profile.location if profile else '') PCT3"></div>
     <div class="form-group"><label class="form-label">LinkedIn</label><input type="url" name="linkedin" class="form-control" value="PCT2 saved_data.linkedin if saved_data else (profile.linkedin if profile else '') PCT3" placeholder="https://linkedin.com/in/..."></div>
     <div class="form-group"><label class="form-label">GitHub</label><input type="url" name="github" class="form-control" value="PCT2 saved_data.github if saved_data else (profile.github if profile else '') PCT3" placeholder="https://github.com/..."></div>
    </div>
    <div class="card">
     <h3 style="color:#10b981;margin-bottom:1.2rem;">Education</h3>
     <div class="form-group"><label class="form-label">Degree</label>
      <select name="degree" class="form-control">
       <option value="">-- Select Degree --</option>
       PCT1 for d in ['B.Tech / B.E.','B.Sc. / B.A.','M.Tech / M.E.','M.Sc. / M.A.','MBA','Ph.D.','Diploma','Other'] PCT1
       <option value="PCT2 d PCT3" PCT1 if (saved_data and saved_data.degree==d) or (profile and profile.degree==d) PCT1selected PCT1 endif PCT1>PCT2 d PCT3</option>
       PCT1 endfor PCT1
      </select>
     </div>
     <div class="form-group"><label class="form-label">College / University</label><input type="text" name="education" class="form-control" value="PCT2 saved_data.education if saved_data else (profile.education if profile else '') PCT3" placeholder="University Name, Year"></div>
     <div class="form-group"><label class="form-label">Percentage / CGPA</label><input type="text" name="percentage" class="form-control" value="PCT2 saved_data.percentage if saved_data else (profile.degree_percentage|string if profile and profile.degree_percentage else '') PCT3" placeholder="e.g. 82% or 8.5 CGPA"></div>
    </div>
    <div class="card">
     <h3 style="color:#10b981;margin-bottom:1.2rem;">Template Style</h3>
     <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:.8rem;">
      PCT1 for tid,tlabel,tcolor in [('modern','Modern','#6366f1'),('clean','Clean','#10b981'),('bold','Bold','#f59e0b')] PCT1
      <label style="cursor:pointer;">
       <input type="radio" name="template_id" value="PCT2 tid PCT3" PCT1 if (saved_data and saved_data.template_id==tid) or (not saved_data and tid=='modern') PCT1checked PCT1 endif PCT1 style="display:none;" class="tpl-radio" data-color="PCT2 tcolor PCT3">
       <div class="tpl-opt" data-id="PCT2 tid PCT3" style="border:2px solid PCT1 if (saved_data and saved_data.template_id==tid) or (not saved_data and tid=='modern') PCT1PCT2 tcolor PCT3PCT1 else PCT1rgba(255,255,255,.1)PCT1 endif PCT1;border-radius:.8rem;padding:1rem;text-align:center;transition:all .2s;">
        <div style="width:40px;height:50px;background:PCT2 tcolor PCT3;border-radius:.3rem;margin:0 auto .6rem;opacity:.7;"></div>
        <div style="color:#fff;font-size:.85rem;font-weight:600;">PCT2 tlabel PCT3</div>
       </div>
      </label>
      PCT1 endfor PCT1
     </div>
    </div>
   </div>
   <div style="display:flex;flex-direction:column;gap:1.5rem;">
    <div class="card"><h3 style="color:#10b981;margin-bottom:1.2rem;">Career Objective</h3><textarea name="objective" class="form-control" rows="4" placeholder="Summarize your professional goals..." style="resize:vertical;">PCT2 saved_data.objective if saved_data else (profile.bio if profile else '') PCT3</textarea></div>
    <div class="card"><h3 style="color:#10b981;margin-bottom:1.2rem;">Technical Skills</h3><textarea name="skills" class="form-control" rows="3" placeholder="Python, React, SQL, Docker..." style="resize:vertical;">PCT2 saved_data.skills if saved_data else (profile.skills if profile else '') PCT3</textarea></div>
    <div class="card"><h3 style="color:#10b981;margin-bottom:1.2rem;">Work Experience</h3><textarea name="experience" class="form-control" rows="5" placeholder="Company | Role | Duration&#10;- Achievement" style="resize:vertical;">PCT2 saved_data.experience if saved_data else (profile.experience if profile else '') PCT3</textarea></div>
    <div class="card"><h3 style="color:#10b981;margin-bottom:1.2rem;">Projects</h3><textarea name="projects" class="form-control" rows="4" placeholder="Project | Tech Stack&#10;- Description" style="resize:vertical;">PCT2 saved_data.projects if saved_data else '' PCT3</textarea></div>
    <div class="card">
     <h3 style="color:#10b981;margin-bottom:1rem;">Certifications</h3>
     <textarea name="certifications" class="form-control" rows="3" placeholder="AWS Certified, Google ML..." style="resize:vertical;">PCT2 saved_data.certifications if saved_data else '' PCT3</textarea>
     <h3 style="color:#10b981;margin:.8rem 0;">Achievements</h3>
     <textarea name="achievements" class="form-control" rows="3" placeholder="Awards, publications..." style="resize:vertical;">PCT2 saved_data.achievements if saved_data else '' PCT3</textarea>
    </div>
   </div>
  </div>
  <div style="display:flex;gap:1rem;margin-top:1.5rem;justify-content:center;">
   <button type="submit" class="btn btn-primary" style="min-width:200px;" id="resume-save-btn">Save Resume</button>
   PCT1 if saved_data PCT1<a href="PCT2 url_for('resume_builder_preview') PCT3" class="btn btn-outline" style="min-width:200px;" id="resume-preview-btn">Preview &amp; Download</a>PCT1 endif PCT1
  </div>
 </form>
</div>
PCT1 endblock PCT1
PCT1 block scripts PCT1
<script>
document.querySelectorAll('.tpl-radio').forEach(r=>{
 r.addEventListener('change',()=>{
  document.querySelectorAll('.tpl-opt').forEach(o=>o.style.borderColor='rgba(255,255,255,.1)');
  const s=document.querySelector(.tpl-opt[data-id='']);
  if(s)s.style.borderColor=r.dataset.color;
 });
});
</script>
PCT1 endblock PCT1""")

w('resume-preview.html',"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Resume - PCT2 data.full_name PCT3</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Segoe UI',Arial,sans-serif;background:#f5f7fa;}
.ctrl{background:#1e293b;padding:1rem 2rem;display:flex;justify-content:space-between;align-items:center;}
.ctrl h3{color:#fff;font-size:1rem;}
.btns{display:flex;gap:.8rem;}
.btn-p{background:#6366f1;color:#fff;padding:.5rem 1.2rem;border-radius:.5rem;font-size:.85rem;font-weight:600;cursor:pointer;border:none;}
.btn-b{background:transparent;color:#94a3b8;border:1px solid #334155;padding:.5rem 1.2rem;border-radius:.5rem;font-size:.85rem;text-decoration:none;}
.resume{max-width:800px;margin:2rem auto;background:#fff;box-shadow:0 4px 20px rgba(0,0,0,.15);}
PCT1 if template_id=='clean' PCT1
.hdr{background:#fff;padding:2.5rem;border-bottom:4px solid #10b981;}
.hdr h1{font-size:2.2rem;font-weight:800;color:#0f172a;}
.hdr .ct{color:#475569;}
.sec h2{color:#10b981;border-bottom:2px solid #d1fae5;}
PCT1 elif template_id=='bold' PCT1
.hdr{background:#0f172a;padding:2.5rem;}
.hdr h1{font-size:2.5rem;font-weight:900;color:#f59e0b;}
.hdr .ct{color:#94a3b8;}
.sec h2{color:#f59e0b;}
PCT1 else PCT1
.hdr{background:linear-gradient(135deg,#6366f1,#8b5cf6);padding:2.5rem;}
.hdr h1{font-size:2.2rem;font-weight:800;color:#fff;}
.hdr .ct{color:rgba(255,255,255,.9);}
.sec h2{color:#6366f1;border-bottom:2px solid #e0e7ff;}
PCT1 endif PCT1
.hdr .ct{display:flex;flex-wrap:wrap;gap:.8rem;margin-top:.8rem;font-size:.88rem;}
.sec{padding:1.5rem 2.5rem;border-bottom:1px solid #f1f5f9;}
.sec h2{font-size:.95rem;text-transform:uppercase;letter-spacing:.08em;font-weight:700;margin-bottom:.8rem;padding-bottom:.3rem;}
.sec p,.sec li{color:#374151;font-size:.9rem;line-height:1.7;}
.sk-grid{display:flex;flex-wrap:wrap;gap:.4rem;}
.sk{background:#f1f5f9;color:#1e293b;border-radius:2rem;padding:.2rem .7rem;font-size:.82rem;}
@media print{.ctrl{display:none;}.resume{box-shadow:none;margin:0;}}
</style></head><body>
<div class="ctrl">
 <h3>Resume Preview: PCT2 data.full_name PCT3</h3>
 <div class="btns">
  <button class="btn-p" onclick="window.print()">Print / Save PDF</button>
  <a href="PCT2 url_for('resume_builder') PCT3" class="btn-b">Edit Resume</a>
 </div>
</div>
<div class="resume">
 <div class="hdr">
  <h1>PCT2 data.full_name PCT3</h1>
  PCT1 if data.degree PCT1<div style="font-size:.9rem;margin:.3rem 0;PCT1 if template_id!='bold' PCT1color:rgba(255,255,255,.85)PCT1 else PCT1color:#94a3b8PCT1 endif PCT1;">PCT2 data.degree PCT3PCT1 if data.percentage PCT1 &bull; PCT2 data.percentage PCT3PCT1 endif PCT1</div>PCT1 endif PCT1
  <div class="ct">
   PCT1 if data.email PCT1<span>PCT2 data.email PCT3</span>PCT1 endif PCT1
   PCT1 if data.phone PCT1<span>PCT2 data.phone PCT3</span>PCT1 endif PCT1
   PCT1 if data.location PCT1<span>PCT2 data.location PCT3</span>PCT1 endif PCT1
   PCT1 if data.linkedin PCT1<span>PCT2 data.linkedin PCT3</span>PCT1 endif PCT1
   PCT1 if data.github PCT1<span>PCT2 data.github PCT3</span>PCT1 endif PCT1
  </div>
 </div>
 PCT1 if data.objective PCT1<div class="sec"><h2>Summary</h2><p>PCT2 data.objective PCT3</p></div>PCT1 endif PCT1
 PCT1 if data.skills PCT1<div class="sec"><h2>Skills</h2><div class="sk-grid">PCT1 for sk in data.skills.split(',') PCT1PCT1 if sk.strip() PCT1<span class="sk">PCT2 sk.strip() PCT3</span>PCT1 endif PCT1PCT1 endfor PCT1</div></div>PCT1 endif PCT1
 PCT1 if data.experience PCT1<div class="sec"><h2>Experience</h2><p style="white-space:pre-wrap;">PCT2 data.experience PCT3</p></div>PCT1 endif PCT1
 PCT1 if data.education PCT1<div class="sec"><h2>Education</h2><p><strong>PCT2 data.degree or '' PCT3</strong>PCT1 if data.degree and data.percentage PCT1 &mdash; PCT2 data.percentage PCT3PCT1 endif PCT1</p><p>PCT2 data.education PCT3</p></div>PCT1 endif PCT1
 PCT1 if data.projects PCT1<div class="sec"><h2>Projects</h2><p style="white-space:pre-wrap;">PCT2 data.projects PCT3</p></div>PCT1 endif PCT1
 PCT1 if data.certifications PCT1<div class="sec"><h2>Certifications</h2><p style="white-space:pre-wrap;">PCT2 data.certifications PCT3</p></div>PCT1 endif PCT1
 PCT1 if data.achievements PCT1<div class="sec"><h2>Achievements</h2><p style="white-space:pre-wrap;">PCT2 data.achievements PCT3</p></div>PCT1 endif PCT1
</div></body></html>""")

print('Batch 3 done')