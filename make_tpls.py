import os, textwrap
T = r'c:\Users\SAJIN\OneDrive\Desktop\job\templates'
def w(n,c): 
    c = c.replace('PCT1','{%').replace('PCT2','{{').replace('PCT3','}}')
    open(os.path.join(T,n),'w',encoding='utf-8').write(c); print('OK',n)

w('messages.html',"""PCT1 extends 'base.html' PCT1
PCT1 block title PCT1Messages | CareerPulsePCT1 endblock PCT1
PCT1 block content PCT1
<div class="container" style="padding:2.5rem 0;">
 <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:2rem;">
  <h1 style="color:#fff;font-size:2rem;font-weight:800;">Messages</h1>
  <a href="PCT2 url_for('compose_message') PCT3" class="btn btn-primary" id="compose-msg-btn">Compose</a>
 </div>
 <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;">
  <div class="card"><h3 style="color:#fff;margin-bottom:1.2rem;">Inbox (PCT2 inbox|length PCT3)</h3>
   PCT1 for msg in inbox PCT1
   <a href="PCT2 url_for('view_message',msg_id=msg.id) PCT3" style="display:block;text-decoration:none;margin-bottom:.8rem;">
    <div style="background:PCT1 if not msg.is_read PCT1rgba(99,102,241,.1)PCT1 else PCT1rgba(255,255,255,.03)PCT1 endif PCT1;border:1px solid rgba(255,255,255,.1);border-radius:.8rem;padding:.9rem 1rem;">
     <div style="color:#fff;font-weight:PCT1 if not msg.is_read PCT1700PCT1 else PCT1400PCT1 endif PCT1;">PCT2 msg.sender_name PCT3 PCT1 if not msg.is_read PCT1<span style="background:#6366f1;width:8px;height:8px;border-radius:50%;display:inline-block;float:right;margin-top:4px;"></span>PCT1 endif PCT1</div>
     <div style="color:var(--text-muted);font-size:.83rem;">PCT2 msg.subject or '(No Subject)' PCT3</div>
     <div style="color:var(--text-muted);font-size:.75rem;margin-top:.3rem;">PCT2 msg.sent_at[:16] PCT3</div>
    </div>
   </a>
   PCT1 else PCT1<div style="text-align:center;padding:2rem;color:var(--text-muted);">No inbox messages</div>PCT1 endfor PCT1
  </div>
  <div class="card"><h3 style="color:#fff;margin-bottom:1.2rem;">Sent (PCT2 sent|length PCT3)</h3>
   PCT1 for msg in sent PCT1
   <a href="PCT2 url_for('view_message',msg_id=msg.id) PCT3" style="display:block;text-decoration:none;margin-bottom:.8rem;">
    <div style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:.8rem;padding:.9rem 1rem;">
     <div style="color:#fff;font-size:.9rem;">To: PCT2 msg.receiver_name PCT3</div>
     <div style="color:var(--text-muted);font-size:.83rem;">PCT2 msg.subject or '(No Subject)' PCT3</div>
     <div style="color:var(--text-muted);font-size:.75rem;margin-top:.3rem;">PCT2 msg.sent_at[:16] PCT3</div>
    </div>
   </a>
   PCT1 else PCT1<div style="text-align:center;padding:2rem;color:var(--text-muted);">No sent messages</div>PCT1 endfor PCT1
  </div>
 </div>
</div>
PCT1 endblock PCT1""")

w('compose-message.html',"""PCT1 extends 'base.html' PCT1
PCT1 block title PCT1Compose Message | CareerPulsePCT1 endblock PCT1
PCT1 block content PCT1
<div class="container" style="padding:2.5rem 0;max-width:680px;margin:0 auto;">
 <a href="PCT2 url_for('messages') PCT3" style="color:var(--text-muted);text-decoration:none;">Back to Messages</a>
 <h1 style="color:#fff;font-size:2rem;font-weight:800;margin:.5rem 0;">Compose Message</h1>
 <div class="card">
  <form method="POST">
   <div class="form-group"><label class="form-label">Recipient *</label>
    <select name="receiver_id" class="form-control" id="msg-receiver" required>
     <option value="">-- Select recipient --</option>
     PCT1 for r in recipients PCT1<option value="PCT2 r.id PCT3" PCT1 if prefill_receiver==r.id|string PCT1selected PCT1 endif PCT1>PCT2 r.name PCT3 (PCT2 r.role|title PCT3)</option>PCT1 endfor PCT1
    </select>
   </div>
   <div class="form-group"><label class="form-label">Subject</label><input type="text" name="subject" class="form-control" value="PCT2 prefill_subject PCT3" id="msg-subject"></div>
   <div class="form-group"><label class="form-label">Message *</label><textarea name="body" class="form-control" rows="8" required id="msg-body" style="resize:vertical;"></textarea></div>
   <div style="display:flex;gap:1rem;">
    <button type="submit" class="btn btn-primary" style="flex:1;" id="msg-send-btn">Send Message</button>
    <a href="PCT2 url_for('messages') PCT3" class="btn btn-outline">Cancel</a>
   </div>
  </form>
 </div>
</div>
PCT1 endblock PCT1""")

w('view-message.html',"""PCT1 extends 'base.html' PCT1
PCT1 block title PCT1View Message | CareerPulsePCT1 endblock PCT1
PCT1 block content PCT1
<div class="container" style="padding:2.5rem 0;max-width:720px;margin:0 auto;">
 <a href="PCT2 url_for('messages') PCT3" style="color:var(--text-muted);text-decoration:none;font-size:.9rem;">Back to Messages</a>
 <div class="card" style="margin-top:1.5rem;">
  <div style="border-bottom:1px solid rgba(255,255,255,.08);padding-bottom:1.2rem;margin-bottom:1.5rem;">
   <h2 style="color:#fff;font-size:1.4rem;margin-bottom:.8rem;">PCT2 msg.subject or '(No Subject)' PCT3</h2>
   <div style="color:var(--text-muted);font-size:.88rem;">From: <strong style="color:#a5b4fc;">PCT2 msg.sender_name PCT3</strong> &lt;PCT2 msg.sender_email PCT3&gt;</div>
   <div style="color:var(--text-muted);font-size:.88rem;">To: <strong style="color:#a5b4fc;">PCT2 msg.receiver_name PCT3</strong></div>
   <div style="color:var(--text-muted);font-size:.82rem;margin-top:.3rem;">PCT2 msg.sent_at[:16] PCT3</div>
  </div>
  <div style="color:var(--text-secondary);line-height:1.8;white-space:pre-wrap;">PCT2 msg.body PCT3</div>
  <div style="margin-top:2rem;padding-top:1.2rem;border-top:1px solid rgba(255,255,255,.08);display:flex;gap:1rem;">
   <a href="PCT2 url_for('compose_message') PCT3?to=PCT2 msg.sender_id PCT3&subject=Re: PCT2 msg.subject or '' PCT3" class="btn btn-primary" id="msg-reply-btn">Reply</a>
   <a href="PCT2 url_for('messages') PCT3" class="btn btn-outline">Back</a>
  </div>
 </div>
</div>
PCT1 endblock PCT1""")

w('report-fraud.html',"""PCT1 extends 'base.html' PCT1
PCT1 block title PCT1Report Fraud | CareerPulsePCT1 endblock PCT1
PCT1 block content PCT1
<div class="container" style="padding:2.5rem 0;max-width:680px;margin:0 auto;">
 <h1 style="color:#fff;font-size:2rem;font-weight:800;margin-bottom:1.5rem;">Report Suspicious Activity</h1>
 <div class="card">
  <form method="POST" id="fraud-report-form">
   <div class="form-group"><label class="form-label">Related Job (optional)</label>
    <select name="job_id" class="form-control" id="fraud-job-select">
     <option value="">-- Select job --</option>
     PCT1 for j in jobs PCT1<option value="PCT2 j.id PCT3">PCT2 j.title PCT3</option>PCT1 endfor PCT1
    </select>
   </div>
   <div class="form-group"><label class="form-label">Reason *</label>
    <select name="reason" class="form-control" id="fraud-reason" required>
     <option value="">-- Select reason --</option>
     PCT1 for r in ['Fake job posting','Request for money','Misleading salary','Identity fraud','Harassment','Phishing/scam','Other'] PCT1<option value="PCT2 r PCT3">PCT2 r PCT3</option>PCT1 endfor PCT1
    </select>
   </div>
   <div class="form-group"><label class="form-label">Details</label><textarea name="evidence" class="form-control" rows="5" id="fraud-evidence" placeholder="Describe suspicious activity..."></textarea></div>
   <div style="background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.2);border-radius:.6rem;padding:.7rem;margin-bottom:1.2rem;"><p style="color:#fbbf24;font-size:.85rem;margin:0;">False reports may result in account suspension.</p></div>
   <button type="submit" class="btn btn-primary" style="width:100%;background:linear-gradient(135deg,#ef4444,#dc2626);border:none;" id="fraud-submit-btn">Submit Fraud Report</button>
  </form>
 </div>
</div>
PCT1 endblock PCT1""")

w('admin-fraud-reports.html',"""PCT1 extends 'base.html' PCT1
PCT1 block title PCT1Fraud Reports | AdminPCT1 endblock PCT1
PCT1 block content PCT1
<div class="container" style="padding:2.5rem 0;">
 <h1 style="color:#fff;font-size:2rem;font-weight:800;margin-bottom:1.5rem;">Fraud Reports</h1>
 PCT1 if reports PCT1
 <div style="display:flex;flex-direction:column;gap:1rem;">
  PCT1 for r in reports PCT1
  <div class="card" style="border-left:4px solid PCT1 if r.status=='Pending' PCT1#ef4444PCT1 elif r.status=='Reviewed' PCT1#f59e0bPCT1 else PCT1#10b981PCT1 endif PCT1;">
   <div style="display:flex;justify-content:space-between;margin-bottom:1rem;flex-wrap:wrap;gap:.5rem;">
    <span class="badge" style="background:PCT1 if r.status=='Pending' PCT1rgba(239,68,68,.15)PCT1 else PCT1rgba(16,185,129,.15)PCT1 endif PCT1;color:PCT1 if r.status=='Pending' PCT1#f87171PCT1 else PCT1#34d399PCT1 endif PCT1;">PCT2 r.status PCT3</span>
    <span style="color:var(--text-muted);font-size:.8rem;">Report #PCT2 r.id PCT3</span>
   </div>
   <p style="color:#fff;font-weight:600;margin-bottom:.4rem;">PCT2 r.reason PCT3</p>
   PCT1 if r.job_title PCT1<p style="color:#6366f1;font-size:.88rem;margin-bottom:.4rem;">Job: PCT2 r.job_title PCT3</p>PCT1 endif PCT1
   <p style="color:var(--text-muted);font-size:.82rem;margin-bottom:.8rem;">Reporter: PCT2 r.reporter_name PCT3 | PCT2 r.created_at[:16] PCT3</p>
   PCT1 if r.evidence PCT1<p style="color:var(--text-secondary);font-size:.88rem;background:rgba(255,255,255,.03);border-radius:.4rem;padding:.5rem;margin-bottom:1rem;">PCT2 r.evidence PCT3</p>PCT1 endif PCT1
   <form method="POST" action="PCT2 url_for('update_fraud_report',rid=r.id) PCT3" style="display:flex;gap:.8rem;flex-wrap:wrap;align-items:flex-end;">
    <div class="form-group" style="margin-bottom:0;flex:1;"><label class="form-label" style="font-size:.8rem;">Notes</label><input type="text" name="admin_notes" class="form-control" value="PCT2 r.admin_notes or '' PCT3"></div>
    <div class="form-group" style="margin-bottom:0;"><label class="form-label" style="font-size:.8rem;">Status</label>
     <select name="status" class="form-control">PCT1 for s in ['Pending','Reviewed','Dismissed','Resolved'] PCT1<option value="PCT2 s PCT3" PCT1 if r.status==s PCT1selected PCT1 endif PCT1>PCT2 s PCT3</option>PCT1 endfor PCT1</select>
    </div>
    <button type="submit" class="btn btn-primary btn-sm" style="align-self:flex-end;">Update</button>
   </form>
  </div>
  PCT1 endfor PCT1
 </div>
 PCT1 else PCT1<div class="card" style="text-align:center;padding:4rem;"><h3 style="color:#fff;">No fraud reports</h3><p style="color:var(--text-muted);">All clear.</p></div>PCT1 endif PCT1
</div>
PCT1 endblock PCT1""")

print('Batch 1 done')