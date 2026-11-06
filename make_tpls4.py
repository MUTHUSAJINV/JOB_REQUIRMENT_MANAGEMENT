import os
T = r'c:\Users\SAJIN\OneDrive\Desktop\job\templates'
def w(n,c): 
    c = c.replace('PCT1','{%').replace('PCT2','{{').replace('PCT3','}}')
    open(os.path.join(T,n),'w',encoding='utf-8').write(c); print('OK',n)

w('coding-tests.html',"""PCT1 extends 'base.html' PCT1
PCT1 block title PCT1Coding Tests | CareerPulsePCT1 endblock PCT1
PCT1 block content PCT1
<div style="background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);padding:3rem 0 2rem;text-align:center;">
 <div class="container">
  <h1 style="font-size:2.5rem;font-weight:800;color:#fff;">Coding <span style="background:linear-gradient(135deg,#06b6d4,#67e8f9);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Assessments</span></h1>
  <p style="color:var(--text-muted);margin-top:.5rem;">Timed MCQ tests to benchmark your skills and impress recruiters.</p>
 </div>
</div>
<div class="container" style="padding:2.5rem 0;">
 PCT1 if tests PCT1
 <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:1.5rem;">
  PCT1 for test in tests PCT1
  PCT1 set sub = sub_map.get(test.id) PCT1
  <div class="card" style="border-left:4px solid PCT1 if test.difficulty=='Easy' PCT1#10b981PCT1 elif test.difficulty=='Medium' PCT1#f59e0bPCT1 else PCT1#ef4444PCT1 endif PCT1;transition:transform .2s;" onmouseover="this.style.transform='translateY(-4px)'" onmouseout="this.style.transform=''">
   <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1rem;">
    <h3 style="color:#fff;font-size:1.1rem;">PCT2 test.title PCT3</h3>
    <span class="badge" style="background:PCT1 if test.difficulty=='Easy' PCT1rgba(16,185,129,.15)PCT1 elif test.difficulty=='Medium' PCT1rgba(245,158,11,.15)PCT1 else PCT1rgba(239,68,68,.15)PCT1 endif PCT1;color:PCT1 if test.difficulty=='Easy' PCT1#34d399PCT1 elif test.difficulty=='Medium' PCT1#fbbf24PCT1 else PCT1#f87171PCT1 endif PCT1;white-space:nowrap;">PCT2 test.difficulty PCT3</span>
   </div>
   <p style="color:var(--text-muted);font-size:.88rem;margin-bottom:1rem;">PCT2 test.description or 'Test your knowledge.' PCT3</p>
   <div style="display:flex;gap:.6rem;margin-bottom:1.2rem;flex-wrap:wrap;">
    <span class="badge">PCT2 test.category PCT3</span>
    <span class="badge">PCT2 test.time_limit PCT3 min</span>
    PCT1 if sub PCT1<span class="badge badge-success">Completed PCT2 sub.score PCT3/PCT2 sub.total_questions PCT3</span>PCT1 endif PCT1
   </div>
   PCT1 if sub PCT1
   <div style="background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.2);border-radius:.6rem;padding:.7rem;margin-bottom:1rem;">
    <div style="display:flex;justify-content:space-between;"><span style="color:#6ee7b7;font-size:.88rem;">Your Score</span><span style="color:#34d399;font-weight:700;">PCT2 sub.score PCT3/PCT2 sub.total_questions PCT3</span></div>
    <div style="background:rgba(255,255,255,.08);border-radius:1rem;height:6px;margin-top:.5rem;overflow:hidden;"><div style="background:#10b981;height:100%;width:PCT2 (sub.score/sub.total_questions*100)|int PCT3%;border-radius:1rem;"></div></div>
   </div>
   <a href="PCT2 url_for('take_test',test_id=test.id) PCT3" class="btn btn-outline" style="width:100%;text-align:center;">Review Answers</a>
   PCT1 else PCT1
   <a href="PCT2 url_for('take_test',test_id=test.id) PCT3" class="btn btn-primary" style="width:100%;text-align:center;" id="test-start-PCT2 test.id PCT3">Start Test</a>
   PCT1 endif PCT1
  </div>
  PCT1 endfor PCT1
 </div>
 PCT1 else PCT1
 <div class="card" style="text-align:center;padding:4rem;">
  <div style="font-size:3rem;margin-bottom:1rem;">&#x1F4BB;</div>
  <h3 style="color:#fff;">No coding tests available yet</h3>
  <p style="color:var(--text-muted);margin:.5rem 0 1.5rem;">Tests are added regularly. Check back soon!</p>
 </div>
 PCT1 endif PCT1
</div>
PCT1 endblock PCT1""")

w('take-test.html',"""PCT1 extends 'base.html' PCT1
PCT1 block title PCT1PCT2 test.title PCT3 | CareerPulsePCT1 endblock PCT1
PCT1 block content PCT1
<div class="container" style="padding:2.5rem 0;max-width:800px;margin:0 auto;">
 <a href="PCT2 url_for('coding_tests') PCT3" style="color:var(--text-muted);text-decoration:none;font-size:.9rem;">Back to Tests</a>
 <h1 style="color:#fff;font-size:2rem;font-weight:800;margin:.5rem 0;">PCT2 test.title PCT3</h1>
 <div style="display:flex;gap:1rem;margin-bottom:1.5rem;flex-wrap:wrap;">
  <span class="badge">PCT2 test.category PCT3</span>
  <span class="badge">PCT2 test.time_limit PCT3 min limit</span>
  <span class="badge">PCT2 questions|length PCT3 questions</span>
 </div>
 PCT1 if result PCT1
 <div class="card" style="text-align:center;padding:2rem;margin-bottom:2rem;border-left:4px solid PCT1 if result.percentage>=70 PCT1#10b981PCT1 elif result.percentage>=40 PCT1#f59e0bPCT1 else PCT1#ef4444PCT1 endif PCT1;">
  <h2 style="color:#fff;font-size:2rem;font-weight:800;">PCT2 result.score PCT3 / PCT2 result.total PCT3</h2>
  <div style="font-size:1.3rem;font-weight:700;color:PCT1 if result.percentage>=70 PCT1#34d399PCT1 elif result.percentage>=40 PCT1#fbbf24PCT1 else PCT1#f87171PCT1 endif PCT1;margin:.3rem 0;">PCT2 result.percentage PCT3%</div>
  <p style="color:var(--text-muted);">PCT1 if result.percentage>=70 PCT1Excellent! You passed.PCT1 elif result.percentage>=40 PCT1Good effort! Review the answers below.PCT1 else PCT1Keep practicing! Study the concepts.PCT1 endif PCT1</p>
  <div style="background:rgba(255,255,255,.08);border-radius:1rem;height:10px;margin:1.5rem 0;overflow:hidden;">
   <div style="background:PCT1 if result.percentage>=70 PCT1#10b981PCT1 elif result.percentage>=40 PCT1#f59e0bPCT1 else PCT1#ef4444PCT1 endif PCT1;height:100%;width:PCT2 result.percentage PCT3%;border-radius:1rem;"></div>
  </div>
 </div>
 PCT1 for q in questions PCT1
 PCT1 set user_ans = result.answers.get(q.id|string,'') PCT1
 PCT1 set is_correct = user_ans.upper() == q.correct_option.upper() PCT1
 <div class="card" style="margin-bottom:1rem;border-left:4px solid PCT1 if is_correct PCT1#10b981PCT1 else PCT1#ef4444PCT1 endif PCT1;">
  <p style="color:#fff;font-weight:500;margin-bottom:1rem;">PCT2 loop.index PCT3. PCT2 q.question PCT3</p>
  PCT1 for opt,label in [('A',q.option_a),('B',q.option_b),('C',q.option_c),('D',q.option_d)] PCT1
  <div style="margin:.3rem 0;padding:.5rem .8rem;border-radius:.5rem;font-size:.9rem;background:PCT1 if opt==q.correct_option.upper() PCT1rgba(16,185,129,.15)PCT1 elif opt==user_ans.upper() and not is_correct PCT1rgba(239,68,68,.1)PCT1 else PCT1transparentPCT1 endif PCT1;color:PCT1 if opt==q.correct_option.upper() PCT1#34d399PCT1 elif opt==user_ans.upper() and not is_correct PCT1#f87171PCT1 else PCT1var(--text-muted)PCT1 endif PCT1;">
   <strong>PCT2 opt PCT3.</strong> PCT2 label PCT3PCT1 if opt==q.correct_option.upper() PCT1 &#x2713;PCT1 elif opt==user_ans.upper() and not is_correct PCT1 &#x2717;PCT1 endif PCT1
  </div>
  PCT1 endfor PCT1
  PCT1 if q.explanation PCT1<p style="color:var(--text-muted);font-size:.82rem;margin-top:.5rem;background:rgba(99,102,241,.08);border-radius:.4rem;padding:.4rem .7rem;">Hint: PCT2 q.explanation PCT3</p>PCT1 endif PCT1
 </div>
 PCT1 endfor PCT1
 PCT1 else PCT1
 <form method="POST" id="test-form" onsubmit="return confirmSubmit()">
  <div style="background:rgba(6,182,212,.05);border:1px solid rgba(6,182,212,.3);border-radius:.8rem;padding:.8rem 1.2rem;margin-bottom:1.5rem;display:flex;justify-content:space-between;align-items:center;">
   <span style="color:#67e8f9;font-weight:600;">Time Remaining</span>
   <span id="timer" style="color:#fff;font-size:1.3rem;font-weight:800;">PCT2 test.time_limit PCT3:00</span>
  </div>
  PCT1 for q in questions PCT1
  <div class="card" style="margin-bottom:1rem;" id="q-PCT2 loop.index PCT3">
   <p style="color:#fff;font-weight:600;margin-bottom:1rem;">PCT2 loop.index PCT3. PCT2 q.question PCT3</p>
   PCT1 for opt,label in [('A',q.option_a),('B',q.option_b),('C',q.option_c),('D',q.option_d)] PCT1
   <label style="display:flex;align-items:center;gap:.8rem;padding:.6rem .8rem;margin:.3rem 0;border-radius:.5rem;cursor:pointer;border:1px solid rgba(255,255,255,.06);transition:background .15s;" onmouseover="this.style.background='rgba(99,102,241,.1)'" onmouseout="this.style.background=''">
    <input type="radio" name="q_PCT2 q.id PCT3" value="PCT2 opt PCT3" style="accent-color:#6366f1;">
    <span style="color:var(--text-secondary);font-size:.92rem;"><strong style="color:#a5b4fc;">PCT2 opt PCT3.</strong> PCT2 label PCT3</span>
   </label>
   PCT1 endfor PCT1
  </div>
  PCT1 endfor PCT1
  <div style="text-align:center;margin-top:1.5rem;">
   <button type="submit" class="btn btn-primary" style="min-width:250px;font-size:1rem;" id="test-submit-btn">Submit Test</button>
  </div>
 </form>
 PCT1 endif PCT1
</div>
PCT1 endblock PCT1
PCT1 block scripts PCT1
<script>
PCT1 if not result PCT1
var mins=PCT2 test.time_limit PCT3,secs=0,el=document.getElementById('timer');
var iv=setInterval(function(){
 if(secs===0){if(mins===0){clearInterval(iv);document.getElementById('test-form').submit();return;}mins--;secs=59;}else{secs--;}
 el.textContent=String(mins).padStart(2,'0')+':'+String(secs).padStart(2,'0');
 if(mins<5)el.style.color='#f87171';
},1000);
function confirmSubmit(){clearInterval(iv);return confirm('Submit test? Answers cannot be changed after submission.');}
PCT1 endif PCT1
</script>
PCT1 endblock PCT1""")

w('mock-interview.html',"""PCT1 extends 'base.html' PCT1
PCT1 block title PCT1Mock Interview | CareerPulsePCT1 endblock PCT1
PCT1 block content PCT1
<div style="background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);padding:3rem 0 2rem;text-align:center;">
 <div class="container">
  <h1 style="font-size:2.5rem;font-weight:800;color:#fff;">Mock <span style="background:linear-gradient(135deg,#8b5cf6,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Interview</span></h1>
  <p style="color:var(--text-muted);margin-top:.5rem;">AI-powered practice interviews with instant scoring and personalized feedback.</p>
 </div>
</div>
<div class="container" style="padding:2.5rem 0;">
 <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-bottom:2rem;">
  <div class="card">
   <h3 style="color:#8b5cf6;margin-bottom:1.5rem;">Schedule New Interview</h3>
   <form method="POST">
    <input type="hidden" name="action" value="schedule">
    <div class="form-group">
     <label class="form-label">Category *</label>
     <select name="category" class="form-control" id="mi-category" required>
      PCT1 for cat in categories PCT1<option value="PCT2 cat PCT3">PCT2 cat PCT3</option>PCT1 endfor PCT1
     </select>
    </div>
    <div class="form-group"><label class="form-label">Date *</label><input type="date" name="scheduled_date" class="form-control" id="mi-date" required></div>
    <div class="form-group"><label class="form-label">Time *</label><input type="time" name="scheduled_time" class="form-control" id="mi-time" required></div>
    <button type="submit" class="btn btn-primary" style="width:100%;" id="mi-schedule-btn">Schedule Interview</button>
   </form>
  </div>
  <div class="card" style="background:rgba(139,92,246,.03);border-color:rgba(139,92,246,.2);">
   <h3 style="color:#c4b5fd;margin-bottom:1.2rem;">How It Works</h3>
   PCT1 for step,desc in [('1. Schedule','Choose a category and preferred date/time.'),('2. Start','See 5 AI-generated interview questions.'),('3. Answer','Write detailed responses to each question.'),('4. Feedback','Get instant AI scoring and personalized tips.')] PCT1
   <div style="display:flex;gap:1rem;margin-bottom:1rem;">
    <div style="background:rgba(139,92,246,.2);border-radius:.6rem;padding:.3rem .7rem;font-weight:700;color:#a78bfa;font-size:.82rem;white-space:nowrap;flex-shrink:0;">PCT2 step PCT3</div>
    <p style="color:var(--text-muted);font-size:.88rem;margin:0;padding-top:.1rem;">PCT2 desc PCT3</p>
   </div>
   PCT1 endfor PCT1
  </div>
 </div>
 PCT1 if past_interviews PCT1
 <div class="card">
  <h3 style="color:#fff;margin-bottom:1.5rem;">Your Interviews</h3>
  PCT1 for iv in past_interviews PCT1
  <div style="display:flex;justify-content:space-between;align-items:center;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:.8rem;padding:1rem 1.2rem;margin-bottom:.8rem;flex-wrap:wrap;gap:.8rem;">
   <div>
    <span style="color:#fff;font-weight:600;">PCT2 iv.category PCT3</span>
    <span style="color:var(--text-muted);font-size:.82rem;margin-left:.8rem;">PCT2 iv.scheduled_date PCT3 PCT2 iv.scheduled_time PCT3</span>
    <div style="margin-top:.3rem;">
     PCT1 if iv.status=='Completed' PCT1<span class="badge badge-success">Completed</span>PCT1 else PCT1<span class="badge">Scheduled</span>PCT1 endif PCT1
    </div>
    PCT1 if iv.feedback PCT1<div style="color:var(--text-muted);font-size:.82rem;margin-top:.3rem;">PCT2 iv.feedback PCT3</div>PCT1 endif PCT1
   </div>
   <div style="display:flex;align-items:center;gap:1rem;">
    PCT1 if iv.score is not none PCT1<span style="color:#a78bfa;font-size:1.1rem;font-weight:700;">PCT2 iv.score PCT3%</span>PCT1 endif PCT1
    PCT1 if iv.status != 'Completed' PCT1
    <a href="PCT2 url_for('start_mock_interview',interview_id=iv.id) PCT3" class="btn btn-primary btn-sm">Start Now</a>
    PCT1 else PCT1
    <a href="PCT2 url_for('start_mock_interview',interview_id=iv.id) PCT3" class="btn btn-outline btn-sm">Review</a>
    PCT1 endif PCT1
   </div>
  </div>
  PCT1 endfor PCT1
 </div>
 PCT1 endif PCT1
</div>
PCT1 endblock PCT1""")

w('mock-interview-session.html',"""PCT1 extends 'base.html' PCT1
PCT1 block title PCT1Interview Session | CareerPulsePCT1 endblock PCT1
PCT1 block content PCT1
<div class="container" style="padding:2.5rem 0;max-width:800px;margin:0 auto;">
 <a href="PCT2 url_for('mock_interview') PCT3" style="color:var(--text-muted);text-decoration:none;font-size:.9rem;">Back to Interviews</a>
 <h1 style="color:#fff;font-size:2rem;font-weight:800;margin:.5rem 0;">PCT2 interview.category PCT3 Interview</h1>
 <div style="display:flex;gap:1rem;margin-bottom:1.5rem;flex-wrap:wrap;">
  <span class="badge">PCT2 interview.scheduled_date PCT3 PCT2 interview.scheduled_time PCT3</span>
  <span class="badge" style="background:rgba(139,92,246,.15);color:#c4b5fd;">PCT2 interview.status PCT3</span>
 </div>
 PCT1 if interview.status=='Completed' PCT1
 <div class="card" style="text-align:center;padding:2rem;margin-bottom:1.5rem;border-left:4px solid #8b5cf6;">
  <h2 style="color:#a78bfa;font-size:2rem;">PCT2 interview.score PCT3%</h2>
  <p style="color:var(--text-muted);">PCT2 interview.feedback PCT3</p>
 </div>
 PCT1 endif PCT1
 <form method="POST" action="PCT2 url_for('mock_interview') PCT3" id="interview-form">
  <input type="hidden" name="action" value="submit">
  <input type="hidden" name="interview_id" value="PCT2 interview.id PCT3">
  PCT1 for q in questions PCT1
  <div class="card" style="margin-bottom:1.2rem;border-left:4px solid #8b5cf6;">
   <div style="display:flex;align-items:flex-start;gap:1rem;margin-bottom:1rem;">
    <span style="background:rgba(139,92,246,.2);border-radius:.5rem;padding:.3rem .7rem;color:#a78bfa;font-weight:700;font-size:.85rem;white-space:nowrap;flex-shrink:0;">Q PCT2 loop.index PCT3</span>
    <p style="color:#fff;font-weight:600;line-height:1.5;">PCT2 q.q PCT3</p>
   </div>
   PCT1 if q.hint PCT1<p style="color:var(--text-muted);font-size:.82rem;background:rgba(139,92,246,.06);border-radius:.4rem;padding:.4rem .7rem;margin-bottom:.8rem;">Hint: PCT2 q.hint PCT3</p>PCT1 endif PCT1
   PCT1 if interview.status == 'Completed' PCT1
   <div style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:.6rem;padding:.8rem;color:var(--text-secondary);min-height:60px;">Interview completed. See score above.</div>
   PCT1 else PCT1
   <textarea name="answer_PCT2 loop.index0 PCT3" class="form-control" rows="5" placeholder="Write your detailed answer (aim for 50+ words)..." style="resize:vertical;" required></textarea>
   PCT1 endif PCT1
  </div>
  PCT1 endfor PCT1
  PCT1 if interview.status != 'Completed' PCT1
  <div style="text-align:center;margin-top:1.5rem;">
   <button type="submit" class="btn btn-primary" style="min-width:250px;" id="interview-submit-btn" onclick="return confirm('Submit this interview? Score will be calculated immediately.')">Submit Interview</button>
  </div>
  PCT1 endif PCT1
 </form>
</div>
PCT1 endblock PCT1""")

print('Batch 4 done - ALL TEMPLATES COMPLETE')