from flask import (Flask,render_template,request,redirect,url_for,session,flash,send_from_directory,jsonify,abort)
import sqlite3,os,uuid,json,re
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import ai_analyzer

app=Flask(__name__)
app.secret_key="careerpulse-super-secret-key-prod-randomized-seed"
BASE_DIR=os.path.abspath(os.path.dirname(__file__))
DATABASE=os.path.join(BASE_DIR,"database","jobportal.db")
UPLOAD_FOLDER=os.path.join(BASE_DIR,"uploads","resumes")
ALLOWED_EXTENSIONS={"pdf","doc","docx"}
app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"]=10*1024*1024
os.makedirs(os.path.join(BASE_DIR,"database"),exist_ok=True)
os.makedirs(UPLOAD_FOLDER,exist_ok=True)

def get_db():
    conn=sqlite3.connect(DATABASE)
    conn.row_factory=sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def allowed_file(fn):
    return "." in fn and fn.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(role=None):
    def deco(func):
        from functools import wraps
        @wraps(func)
        def wrapper(*args,**kwargs):
            if "user_id" not in session:
                flash("Please log in to access the portal.","warning")
                return redirect(url_for("login",next=request.path))
            if role and session.get("role")!=role:
                flash("Unauthorized access.","danger")
                return redirect(url_for("index"))
            return func(*args,**kwargs)
        return wrapper
    return deco

def compute_smart_recommendations(prof,all_jobs,limit=6):
    if not prof: return []
    usk=set(s.strip().lower() for s in (prof.get("skills") or "").split(",") if s.strip())
    uexp=prof.get("experience_years") or 0
    udeg=(prof.get("degree") or "").strip()
    upct=prof.get("degree_percentage") or 0
    scored=[]
    for job in all_jobs:
        jd = dict(job)
        sc=0
        jsk=set(s.strip().lower() for s in (jd.get("skills") or "").split(",") if s.strip())
        if jsk and usk:
            sc+=min(60,int((len(usk&jsk)/max(len(jsk),1))*60))
        me=jd.get("min_experience") or 0
        sc+=25 if uexp>=me else (10 if uexp>=me-1 else 0)
        rd=jd.get("required_degree") or ""
        sc+=(10 if not rd or rd==udeg else 3 if rd and udeg else 0)
        if upct>=(jd.get("min_percentage") or 0): sc+=5
        scored.append((sc,job))
    scored.sort(key=lambda x:x[0],reverse=True)
    return [{"job":dict(j),"score":s} for s,j in scored[:limit] if s>0]

def detect_fraud_signals(job):
    job = dict(job)
    signals=[]
    text=f"{job.get('title','')} {job.get('description','')} {job.get('requirements','') or ''} {job.get('salary','') or ''}".lower()
    for phrase,reason in [("guaranteed income","Income guarantee is a scam signal"),("send money","Payment request is a red flag"),
                          ("wire transfer","Financial transaction is suspicious"),("pay to apply","Charging to apply is unethical"),
                          ("get rich","Get-rich scheme indicator"),("unlimited earning","MLM/pyramid scheme language")]:
        if phrase in text: signals.append(reason)
    if len(job.get("description",""))<80: signals.append("Job description is unusually short")
    return signals

def analyze_skill_gap(usk_str,target_role):
    role_map={"Software Engineer":["Python","Java","SQL","Git","Data Structures","Algorithms","REST APIs"],
              "Frontend Developer":["HTML","CSS","JavaScript","React","TypeScript","Git","Responsive Design"],
              "Backend Developer":["Python","Node.js","SQL","REST APIs","Docker","Git","Database Design"],
              "Full Stack Developer":["HTML","CSS","JavaScript","React","Python","SQL","Git","Docker","REST APIs"],
              "Data Scientist":["Python","Machine Learning","Statistics","SQL","Pandas","NumPy","Data Visualization"],
              "Machine Learning Engineer":["Python","TensorFlow","PyTorch","Machine Learning","Deep Learning","Statistics","SQL"],
              "DevOps Engineer":["Docker","Kubernetes","CI/CD","Linux","AWS","Terraform","Monitoring"],
              "UI/UX Designer":["Figma","User Research","Prototyping","Design Systems","Wireframing","Usability Testing"],
              "Cloud Architect":["AWS","Azure","GCP","Kubernetes","Docker","Terraform","Security"],
              "Mobile Developer":["React Native","Flutter","iOS","Android","Mobile UI","REST APIs","Git"],
              "Cybersecurity Analyst":["Network Security","Penetration Testing","SIEM","Firewalls","Cryptography","Risk Assessment"],
              "Product Manager":["Product Strategy","User Research","Agile","Data Analysis","Roadmapping","Stakeholder Management"]}
    required=role_map.get(target_role,[])
    usk=[s.strip() for s in (usk_str or "").split(",") if s.strip()]
    usk_lo=[s.lower() for s in usk]
    missing,present=[],[]
    for sk in required: (present if sk.lower() in usk_lo else missing).append(sk)
    match_pct=int((len(present)/max(len(required),1))*100)
    res={"Python":"https://docs.python.org/3/tutorial/","JavaScript":"https://javascript.info/","React":"https://react.dev/learn",
         "Machine Learning":"https://www.coursera.org/learn/machine-learning","Docker":"https://docs.docker.com/get-started/",
         "SQL":"https://www.w3schools.com/sql/","Git":"https://git-scm.com/book/en/v2","AWS":"https://aws.amazon.com/training/",
         "Kubernetes":"https://kubernetes.io/docs/tutorials/","Figma":"https://www.figma.com/resources/learn-design/",
         "TypeScript":"https://www.typescriptlang.org/docs/handbook/intro.html","Node.js":"https://nodejs.dev/en/learn/"}
    recs=[{"skill":sk,"resource":res.get(sk,f"https://www.google.com/search?q=learn+{sk.replace(' ','+')}")} for sk in missing[:5]]
    return {"target_role":target_role,"required_skills":required,"present_skills":present,"missing_skills":missing,"match_score":match_pct,"recommendations":recs}

def generate_mock_questions(category):
    bank={"Software Engineering":[{"q":"Explain OOP and its four pillars.","hint":"Encapsulation, Inheritance, Polymorphism, Abstraction"},
            {"q":"Difference between process and thread?","hint":"Memory sharing and isolation"},
            {"q":"Describe SOLID principles.","hint":"Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion"},
            {"q":"How to debug a production issue?","hint":"Logs, monitoring, isolation, reproduce, fix, test"},
            {"q":"REST vs GraphQL APIs?","hint":"Data fetching patterns and over/under-fetching"}],
          "Data Science":[{"q":"Supervised vs unsupervised learning?","hint":"Labeled vs unlabeled data"},
            {"q":"Explain overfitting and prevention.","hint":"Regularization, cross-validation, more data"},
            {"q":"What is a confusion matrix?","hint":"Precision, Recall, F1, Accuracy"},
            {"q":"How to handle missing data?","hint":"Imputation, dropping, domain knowledge"},
            {"q":"Bias-variance tradeoff?","hint":"Model complexity vs generalization"}],
          "System Design":[{"q":"Design a URL shortener.","hint":"Hashing, database, redirection, scalability"},
            {"q":"Design a scalable chat app.","hint":"WebSockets, message queues, storage"},
            {"q":"Design a distributed cache.","hint":"Consistency, eviction policies, replication"},
            {"q":"Architecture for e-commerce at scale?","hint":"Load balancing, CDN, database sharding"},
            {"q":"Explain CAP theorem.","hint":"Consistency vs Availability tradeoff"}],
          "Behavioral":[{"q":"Tell me about a team conflict.","hint":"STAR method: Situation, Task, Action, Result"},
            {"q":"Describe your biggest professional failure.","hint":"Be honest, show growth"},
            {"q":"How do you prioritize multiple deadlines?","hint":"Urgency vs importance matrix"},
            {"q":"Example of showing leadership.","hint":"Initiative, impact without authority"},
            {"q":"Where do you see yourself in 5 years?","hint":"Align with company growth and skills"}],
          "Frontend Development":[{"q":"What is the virtual DOM and why React uses it?","hint":"Performance optimization, diffing"},
            {"q":"Explain CSS specificity.","hint":"Inline > ID > Class > Element"},
            {"q":"What are Web Workers?","hint":"Background JS execution, heavy computations"},
            {"q":"Explain the JavaScript event loop.","hint":"Call stack, web APIs, callback queue, microtasks"},
            {"q":"What is lazy loading?","hint":"Load on demand, Intersection Observer"}]}
    return bank.get(category,bank["Behavioral"])

def init_db():
    conn=get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,email TEXT UNIQUE NOT NULL,password TEXT NOT NULL,role TEXT NOT NULL CHECK(role IN('seeker','recruiter','admin')),created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS profiles(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER UNIQUE NOT NULL,headline TEXT,phone TEXT,skills TEXT,education TEXT,degree TEXT,degree_percentage REAL,experience TEXT,experience_years INTEGER DEFAULT 0,bio TEXT,resume TEXT,location TEXT,github TEXT,linkedin TEXT,FOREIGN KEY(user_id)REFERENCES users(id)ON DELETE CASCADE)""")
    ec=[r[1] for r in conn.execute("PRAGMA table_info(profiles)").fetchall()]
    for c,d in [("degree","TEXT"),("degree_percentage","REAL"),("experience_years","INTEGER DEFAULT 0"),("location","TEXT"),("github","TEXT"),("linkedin","TEXT")]:
        if c not in ec: conn.execute(f"ALTER TABLE profiles ADD COLUMN {c} {d}")
    conn.execute("""CREATE TABLE IF NOT EXISTS companies(id INTEGER PRIMARY KEY AUTOINCREMENT,recruiter_id INTEGER UNIQUE NOT NULL,company_name TEXT NOT NULL,industry TEXT,description TEXT,website TEXT,location TEXT,FOREIGN KEY(recruiter_id)REFERENCES users(id)ON DELETE CASCADE)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS jobs(id INTEGER PRIMARY KEY AUTOINCREMENT,recruiter_id INTEGER NOT NULL,title TEXT NOT NULL,description TEXT NOT NULL,requirements TEXT,skills TEXT,location TEXT,job_type TEXT,salary TEXT,status TEXT DEFAULT 'Open',total_vacancy INTEGER DEFAULT 1,min_experience INTEGER DEFAULT 0,required_degree TEXT,min_percentage REAL DEFAULT 0,is_internship INTEGER DEFAULT 0,internship_duration TEXT,stipend TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(recruiter_id)REFERENCES users(id)ON DELETE CASCADE)""")
    ej=[r[1] for r in conn.execute("PRAGMA table_info(jobs)").fetchall()]
    for c,d in [("total_vacancy","INTEGER DEFAULT 1"),("min_experience","INTEGER DEFAULT 0"),("required_degree","TEXT"),("min_percentage","REAL DEFAULT 0"),("is_internship","INTEGER DEFAULT 0"),("internship_duration","TEXT"),("stipend","TEXT")]:
        if c not in ej: conn.execute(f"ALTER TABLE jobs ADD COLUMN {c} {d}")
    conn.execute("""CREATE TABLE IF NOT EXISTS applications(id INTEGER PRIMARY KEY AUTOINCREMENT,job_id INTEGER NOT NULL,seeker_id INTEGER NOT NULL,resume TEXT,cover_note TEXT,status TEXT DEFAULT 'Applied',interview_date TEXT,interview_time TEXT,interview_mode TEXT,interview_link TEXT,interview_notes TEXT,applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(job_id)REFERENCES jobs(id)ON DELETE CASCADE,FOREIGN KEY(seeker_id)REFERENCES users(id)ON DELETE CASCADE,UNIQUE(job_id,seeker_id))""")
    conn.execute("""CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY AUTOINCREMENT,sender_id INTEGER NOT NULL,receiver_id INTEGER NOT NULL,subject TEXT,body TEXT NOT NULL,is_read INTEGER DEFAULT 0,sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(sender_id)REFERENCES users(id)ON DELETE CASCADE,FOREIGN KEY(receiver_id)REFERENCES users(id)ON DELETE CASCADE)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS coding_tests(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,description TEXT,difficulty TEXT DEFAULT 'Medium',category TEXT,time_limit INTEGER DEFAULT 60,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS coding_questions(id INTEGER PRIMARY KEY AUTOINCREMENT,test_id INTEGER,question TEXT NOT NULL,option_a TEXT,option_b TEXT,option_c TEXT,option_d TEXT,correct_option TEXT,explanation TEXT,question_type TEXT DEFAULT 'mcq',FOREIGN KEY(test_id)REFERENCES coding_tests(id)ON DELETE CASCADE)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS test_submissions(id INTEGER PRIMARY KEY AUTOINCREMENT,test_id INTEGER NOT NULL,seeker_id INTEGER NOT NULL,score INTEGER DEFAULT 0,total_questions INTEGER DEFAULT 0,answers TEXT,submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(test_id)REFERENCES coding_tests(id)ON DELETE CASCADE,FOREIGN KEY(seeker_id)REFERENCES users(id)ON DELETE CASCADE)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS mock_interviews(id INTEGER PRIMARY KEY AUTOINCREMENT,seeker_id INTEGER NOT NULL,category TEXT NOT NULL,scheduled_date TEXT,scheduled_time TEXT,status TEXT DEFAULT 'Pending',feedback TEXT,score INTEGER,questions TEXT,answers TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(seeker_id)REFERENCES users(id)ON DELETE CASCADE)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS fraud_reports(id INTEGER PRIMARY KEY AUTOINCREMENT,reporter_id INTEGER NOT NULL,job_id INTEGER,user_id INTEGER,reason TEXT NOT NULL,evidence TEXT,status TEXT DEFAULT 'Pending',admin_notes TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(reporter_id)REFERENCES users(id)ON DELETE CASCADE)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS skill_gap_analyses(id INTEGER PRIMARY KEY AUTOINCREMENT,seeker_id INTEGER NOT NULL,target_role TEXT NOT NULL,current_skills TEXT,required_skills TEXT,missing_skills TEXT,match_score INTEGER DEFAULT 0,recommendations TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(seeker_id)REFERENCES users(id)ON DELETE CASCADE)""")
    conn.execute('''CREATE TABLE IF NOT EXISTS follows(id INTEGER PRIMARY KEY AUTOINCREMENT,follower_id INTEGER NOT NULL,followed_id INTEGER NOT NULL,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(follower_id)REFERENCES users(id)ON DELETE CASCADE,FOREIGN KEY(followed_id)REFERENCES users(id)ON DELETE CASCADE,UNIQUE(follower_id,followed_id))''')
    conn.execute("""CREATE TABLE IF NOT EXISTS resume_builder(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER UNIQUE NOT NULL,template_id TEXT DEFAULT 'modern',data TEXT,updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(user_id)REFERENCES users(id)ON DELETE CASCADE)""")

    # SEED
    if not conn.execute("SELECT id FROM users WHERE email=?",("admin@jobportal.local",)).fetchone():
        conn.execute("INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",("Portal Administrator","admin@jobportal.local",generate_password_hash("admin123"),"admin"))
    if not conn.execute("SELECT id FROM users WHERE email=?",("recruiter@techcorp.com",)).fetchone():
        rp=generate_password_hash("recruiter123")
        r1=conn.execute("INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",("Sarah Jenkins","recruiter@techcorp.com",rp,"recruiter")).lastrowid
        conn.execute("INSERT INTO companies(recruiter_id,company_name,industry,description,website,location) VALUES(?,?,?,?,?,?)",(r1,"TechCorp Solutions","Cloud & AI","TechCorp powers global enterprise cloud infrastructure.","https://techcorp.example.com","San Francisco, CA"))
        r2=conn.execute("INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",("Marcus Vance","recruiter@innovate.io",rp,"recruiter")).lastrowid
        conn.execute("INSERT INTO companies(recruiter_id,company_name,industry,description,website,location) VALUES(?,?,?,?,?,?)",(r2,"Innovate AI Labs","AI & Web3","Innovate AI builds cutting-edge neural models and autonomous systems.","https://innovatelabs.example.com","New York, NY"))
        sp=generate_password_hash("seeker123")
        s1=conn.execute("INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",("Alex Morgan","seeker@example.com",sp,"seeker")).lastrowid
        conn.execute("INSERT INTO profiles(user_id,headline,phone,skills,education,degree,degree_percentage,experience,experience_years,bio,resume) VALUES(?,?,?,?,?,?,?,?,?,?,?)",(s1,"Senior Full Stack Engineer","+1 555-234-8901","Python, React, TypeScript, Node.js, PostgreSQL, Docker, AWS","B.S. Computer Science - UC Berkeley (2019)","B.Tech / B.E.",82.5,"5+ years full-stack. Led microservices refactor reducing latency 40%.",5,"Passionate engineer focused on distributed systems and clean architecture.","sample_resume.pdf"))
        s2=conn.execute("INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",("Elena Rostova","elena@example.com",sp,"seeker")).lastrowid
        conn.execute("INSERT INTO profiles(user_id,headline,phone,skills,education,degree,degree_percentage,experience,experience_years,bio,resume) VALUES(?,?,?,?,?,?,?,?,?,?,?)",(s2,"UI/UX Designer & Product Specialist","+1 555-789-1234","Figma, UI/UX Design, Design Systems, HTML/CSS, User Research, Prototyping","B.A. Interactive Media - RISD (2020)","B.A. / B.Sc.",79.0,"4 years designing SaaS interfaces and mobile applications.",4,"Designer focused on intuitive interfaces and elegant micro-interactions.","sample_resume.pdf"))
        j1=conn.execute("INSERT INTO jobs(recruiter_id,title,description,requirements,skills,location,job_type,salary,status,total_vacancy,min_experience,required_degree,min_percentage) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",(r1,"Senior Full Stack Python/React Engineer","We need a Senior FS Engineer to modernize our platform and architect end-to-end features.","4+ yrs software dev\nPython(Flask/Django)+React\nPostgreSQL, Redis, Docker","Python, React, Flask, PostgreSQL, Docker, REST APIs","San Francisco, CA / Remote","Full-time","$140,000-$175,000/yr","Open",5,4,"B.Tech / B.E.",60.0)).lastrowid
        j2=conn.execute("INSERT INTO jobs(recruiter_id,title,description,requirements,skills,location,job_type,salary,status,total_vacancy,min_experience,required_degree,min_percentage) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",(r1,"Lead Cloud DevOps & Infrastructure Specialist","Architect resilient multi-region infra, improve CI/CD, ensure 99.99% uptime.","5+ yrs AWS/GCP\nKubernetes, Terraform, Docker\nCI/CD & secure networks","AWS, Kubernetes, Terraform, Docker, CI/CD, Linux","Remote (US/Canada)","Full-time","$150,000-$185,000/yr","Open",3,5,"B.Tech / B.E.",65.0)).lastrowid
        j3=conn.execute("INSERT INTO jobs(recruiter_id,title,description,requirements,skills,location,job_type,salary,status,total_vacancy,min_experience,required_degree,min_percentage) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",(r2,"Principal AI / Machine Learning Researcher","Pioneer generative model training, fine-tune LLMs, deploy inference architectures.","PhD/Masters in CS or AI\nPyTorch, Transformers\nPublications or open-source","PyTorch, LLMs, Python, Deep Learning, GPU Optimization","New York, NY (Hybrid)","Full-time","$170,000-$220,000/yr","Open",2,5,"M.Tech / M.Sc.",70.0)).lastrowid
        j4=conn.execute("INSERT INTO jobs(recruiter_id,title,description,requirements,skills,location,job_type,salary,status,total_vacancy,min_experience,required_degree,min_percentage) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",(r2,"Senior UI/UX & Design Systems Lead","Lead design system, create frictionless user journeys, mentor junior designers.","4+ yrs SaaS product design\nFigma mastery\nFrontend understanding","Figma, UI Design, Design Systems, User Research, Prototyping","Remote","Contract","$80-$110/hr","Open",1,4,"B.A. / B.Sc.",55.0)).lastrowid
        j5=conn.execute("INSERT INTO jobs(recruiter_id,title,description,requirements,skills,location,job_type,salary,status,total_vacancy,min_experience,required_degree,min_percentage,is_internship,internship_duration,stipend) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(r1,"Frontend Developer Internship","Learn modern web dev alongside senior engineering mentors.","HTML, CSS, JavaScript basics\nEagerness to learn React\nTeam collaboration","JavaScript, HTML5, CSS3, Git, Responsive Web","Austin, TX","Internship","$30-$40/hr","Open",10,0,"B.Tech / B.E.",55.0,1,"6 Months","$2000/month")).lastrowid
        conn.execute("INSERT INTO applications(job_id,seeker_id,resume,cover_note,status,interview_date,interview_time,interview_mode,interview_link,interview_notes) VALUES(?,?,?,?,?,?,?,?,?,?)",(j1,s1,"sample_resume.pdf","Excited! Python & React matches your mission.","Interview","2026-10-02","14:00 EST","Google Meet","https://meet.google.com/abc-defg-hij","Technical round. Have dev environment ready."))
        conn.execute("INSERT INTO applications(job_id,seeker_id,resume,cover_note,status) VALUES(?,?,?,?,?)",(j3,s1,"sample_resume.pdf","Interested in ML inference platform.","Shortlisted"))
        conn.execute("INSERT INTO applications(job_id,seeker_id,resume,cover_note,status,interview_date,interview_time,interview_mode,interview_link,interview_notes) VALUES(?,?,?,?,?,?,?,?,?,?)",(j4,s2,"sample_resume.pdf","Built design systems for 3 SaaS platforms.","Selected","2026-09-18","11:00 EST","Zoom","https://zoom.us/j/987654321","Offer dispatched."))
        t1=conn.execute("INSERT INTO coding_tests(title,description,difficulty,category,time_limit) VALUES(?,?,?,?,?)",("Python Fundamentals","Core Python concepts","Easy","Python",30)).lastrowid
        for q in [("Output of print(type([]))?","<class 'list'>","<class 'tuple'>","<class 'dict'>","<class 'array'>","A","Lists use []."),("Keyword to define a function?","func","define","def","function","C","def is for functions."),("What does len('hello') return?","4","5","6","Error","B","'hello' has 5 chars."),("How to create a dictionary?","{}","[]","()","<>","A","Curly braces {}."),("What is a lambda function?","Built-in function","Anonymous function","Class method","Module","B","Lambda = nameless function.")]:
            conn.execute("INSERT INTO coding_questions(test_id,question,option_a,option_b,option_c,option_d,correct_option,explanation,question_type) VALUES(?,?,?,?,?,?,?,?,?)",(t1,)+q+("mcq",))
        t2=conn.execute("INSERT INTO coding_tests(title,description,difficulty,category,time_limit) VALUES(?,?,?,?,?)",("Data Structures & Algorithms","Core DSA","Medium","DSA",45)).lastrowid
        for q in [("Time complexity of binary search?","O(n)","O(log n)","O(n log n)","O(1)","B","Halves each step."),("Which uses LIFO?","Queue","Array","Stack","Linked List","C","Stack=LIFO."),("What is a hash table?","Sorted array","Tree","Key-value via hashing","Graph","C","O(1) lookups."),("O(n log n) sort?","Bubble","Merge","Insertion","Selection","B","Merge Sort."),("Binary tree property?","2 roots","At most 2 children","Always balanced","Always sorted","B","Max 2 children.")]:
            conn.execute("INSERT INTO coding_questions(test_id,question,option_a,option_b,option_c,option_d,correct_option,explanation,question_type) VALUES(?,?,?,?,?,?,?,?,?)",(t2,)+q+("mcq",))
        t3=conn.execute("INSERT INTO coding_tests(title,description,difficulty,category,time_limit) VALUES(?,?,?,?,?)",("Web Development Essentials","HTML, CSS, JS fundamentals","Easy","Web Dev",30)).lastrowid
        for q in [("HTML stands for?","HyperText Markup Language","High Text Markup Language","HyperText Machine Language","HyperLink Markup Language","A","HyperText Markup Language."),("CSS for text size?","text-size","font-size","text-height","font-weight","B","font-size."),("DOM stands for?","Document Object Model","Data Object Module","Dynamic Object Method","Display Output Model","A","HTML tree."),("Add to end of array?","push()","append()","add()","insert()","A","Array.push()."),("REST stands for?","Server language","Database type","Representational State Transfer","CSS framework","C","API architecture style.")]:
            conn.execute("INSERT INTO coding_questions(test_id,question,option_a,option_b,option_c,option_d,correct_option,explanation,question_type) VALUES(?,?,?,?,?,?,?,?,?)",(t3,)+q+("mcq",))
    conn.commit()
    conn.close()

# ---- PUBLIC ROUTES ----
@app.route("/")
def index():
    conn=get_db()
    jobs=conn.execute("""SELECT jobs.*,companies.company_name,companies.location AS comp_location FROM jobs LEFT JOIN companies ON jobs.recruiter_id=companies.recruiter_id WHERE jobs.status='Open' ORDER BY jobs.created_at DESC LIMIT 6""").fetchall()
    stats={"jobs":conn.execute("SELECT COUNT(*) FROM jobs WHERE status='Open'").fetchone()[0],"companies":conn.execute("SELECT COUNT(DISTINCT recruiter_id) FROM jobs").fetchone()[0],"seekers":conn.execute("SELECT COUNT(*) FROM users WHERE role='seeker'").fetchone()[0],"placements":conn.execute("SELECT COUNT(*) FROM applications WHERE status='Selected'").fetchone()[0]}
    conn.close()
    return render_template("index.html",jobs=jobs,stats=stats)

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        name=request.form.get("name","").strip(); email=request.form.get("email","").strip().lower()
        password=request.form.get("password",""); role=request.form.get("role","seeker")
        company_name=request.form.get("company_name","").strip()
        degree=request.form.get("degree","").strip(); dp=request.form.get("degree_percentage","").strip()
        ey=request.form.get("experience_years","0").strip()
        if not name or not email or not password: flash("All fields required.","danger"); return redirect(url_for("register"))
        if role not in ["seeker","recruiter","admin"]: flash("Invalid role.","danger"); return redirect(url_for("register"))
        if role=="recruiter" and not company_name: flash("Company name required.","danger"); return redirect(url_for("register"))
        conn=get_db()
        if conn.execute("SELECT id FROM users WHERE email=?",(email,)).fetchone():
            conn.close(); flash("Email already registered.","warning"); return redirect(url_for("login"))
        uid=conn.execute("INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",(name,email,generate_password_hash(password),role)).lastrowid
        if role=="seeker":
            conn.execute("INSERT INTO profiles(user_id,degree,degree_percentage,experience_years) VALUES(?,?,?,?)",(uid,degree or None,float(dp) if dp else None,int(ey) if ey.isdigit() else 0))
        else:
            conn.execute("INSERT INTO companies(recruiter_id,company_name) VALUES(?,?)",(uid,company_name))
        conn.commit(); conn.close(); flash("Account created! Please log in.","success"); return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if "user_id" in session:
        r=session.get("role")
        if r=="seeker": return redirect(url_for("seeker_dashboard"))
        if r=="recruiter": return redirect(url_for("recruiter_dashboard"))
        if r=="admin": return redirect(url_for("admin_dashboard"))
    next_url=request.args.get("next") or request.form.get("next")
    if request.method=="POST":
        email=request.form.get("email","").strip().lower(); password=request.form.get("password","")
        conn=get_db(); user=conn.execute("SELECT * FROM users WHERE email=?",(email,)).fetchone(); conn.close()
        if user and check_password_hash(user["password"],password):
            session.clear(); session["user_id"]=user["id"]; session["name"]=user["name"]; session["email"]=user["email"]; session["role"]=user["role"]
            flash(f"Welcome back, {user['name']}!","success")
            if next_url and next_url.startswith("/") and not next_url.startswith("//"): return redirect(next_url)
            if user["role"]=="seeker": return redirect(url_for("seeker_dashboard"))
            if user["role"]=="recruiter": return redirect(url_for("recruiter_dashboard"))
            if user["role"]=="admin": return redirect(url_for("admin_dashboard"))
        flash("Invalid email or password.","danger")
    return render_template("login.html",next=next_url)

@app.route("/logout")
def logout():
    session.clear(); flash("Logged out successfully.","success"); return redirect(url_for("index"))

@app.route("/jobs")
def jobs():
    kw=request.args.get("keyword","").strip(); loc=request.args.get("location","").strip()
    jtype=request.args.get("job_type","").strip(); sal=request.args.get("salary_filter","").strip()
    exp=request.args.get("experience","").strip(); deg=request.args.get("degree","").strip()
    intern_only=request.args.get("internship","").strip()
    conn=get_db()
    q="""SELECT jobs.*,companies.company_name,companies.location AS comp_location FROM jobs LEFT JOIN companies ON jobs.recruiter_id=companies.recruiter_id WHERE jobs.status='Open'"""
    p=[]
    if kw:
        q+=" AND (jobs.title LIKE ? OR jobs.description LIKE ? OR jobs.skills LIKE ? OR companies.company_name LIKE ?)"; k=f"%{kw}%"; p.extend([k,k,k,k])
    if loc:
        q+=" AND (jobs.location LIKE ? OR companies.location LIKE ?)"; p.extend([f"%{loc}%",f"%{loc}%"])
    if jtype: q+=" AND jobs.job_type=?"; p.append(jtype)
    if sal: q+=" AND jobs.salary LIKE ?"; p.append(f"%{sal}%")
    if exp: q+=" AND jobs.min_experience<=?"; p.append(int(exp))
    if deg: q+=" AND (jobs.required_degree=? OR jobs.required_degree IS NULL OR jobs.required_degree='')"; p.append(deg)
    if intern_only=="1": q+=" AND jobs.is_internship=1"
    q+=" ORDER BY jobs.created_at DESC"
    jlist=conn.execute(q,p).fetchall()
    avail_types=conn.execute("SELECT DISTINCT job_type FROM jobs WHERE job_type IS NOT NULL").fetchall()
    conn.close()
    return render_template("jobs.html",jobs=jlist,keyword=kw,location=loc,job_type=jtype,salary_filter=sal,experience_filter=exp,degree_filter=deg,internship_only=intern_only,available_types=[t[0] for t in avail_types])

@app.route("/internships")
def internships():
    conn=get_db()
    il=conn.execute("""SELECT jobs.*,companies.company_name,companies.location AS comp_location FROM jobs LEFT JOIN companies ON jobs.recruiter_id=companies.recruiter_id WHERE jobs.status='Open' AND jobs.is_internship=1 ORDER BY jobs.created_at DESC""").fetchall()
    conn.close(); return render_template("internships.html",internships=il)

@app.route("/job/<int:job_id>")
def job_details(job_id):
    conn=get_db()
    job=conn.execute("""SELECT jobs.*,companies.company_name,companies.description AS company_description,companies.website,companies.location AS company_location,companies.industry AS company_industry FROM jobs LEFT JOIN companies ON jobs.recruiter_id=companies.recruiter_id WHERE jobs.id=?""",(job_id,)).fetchone()
    if not job: conn.close(); flash("Job not found.","danger"); return redirect(url_for("jobs"))
    fraud_signals=detect_fraud_signals(dict(job))
    has_applied=False; application=None; seeker_profile=None
    if "user_id" in session and session.get("role")=="seeker":
        application=conn.execute("SELECT * FROM applications WHERE job_id=? AND seeker_id=?",(job_id,session["user_id"])).fetchone()
        has_applied=application is not None
        seeker_profile=conn.execute("SELECT * FROM profiles WHERE user_id=?",(session["user_id"],)).fetchone()
    total_apps=conn.execute("SELECT COUNT(*) FROM applications WHERE job_id=?",(job_id,)).fetchone()[0]
    similar=conn.execute("""SELECT jobs.*,companies.company_name FROM jobs LEFT JOIN companies ON jobs.recruiter_id=companies.recruiter_id WHERE jobs.id!=? AND jobs.status='Open' ORDER BY jobs.created_at DESC LIMIT 3""",(job_id,)).fetchall()
    conn.close()
    return render_template("job-details.html",job=job,has_applied=has_applied,application=application,seeker_profile=seeker_profile,similar_jobs=similar,fraud_signals=fraud_signals,total_apps=total_apps)

@app.route("/job/<int:job_id>/apply",methods=["POST"])
@login_required("seeker")
def apply_job(job_id):
    sid=session["user_id"]; conn=get_db()
    job=conn.execute("SELECT * FROM jobs WHERE id=?",(job_id,)).fetchone()
    if not job or job["status"]!="Open": conn.close(); flash("Job closed.","warning"); return redirect(url_for("job_details",job_id=job_id))
    if conn.execute("SELECT id FROM applications WHERE job_id=? AND seeker_id=?",(job_id,sid)).fetchone():
        conn.close(); flash("Already applied.","warning"); return redirect(url_for("job_details",job_id=job_id))
    profile=conn.execute("SELECT * FROM profiles WHERE user_id=?",(sid,)).fetchone()
    cover_note=request.form.get("cover_note","").strip(); resume_source=request.form.get("resume_source","profile"); rfn=None
    if resume_source=="upload" and "custom_resume" in request.files:
        f=request.files["custom_resume"]
        if f and f.filename and allowed_file(f.filename):
            sn=f"app_{uuid.uuid4().hex[:8]}_{secure_filename(f.filename)}"; f.save(os.path.join(app.config["UPLOAD_FOLDER"],sn)); rfn=sn
        else: conn.close(); flash("Invalid file.","danger"); return redirect(url_for("job_details",job_id=job_id))
    else:
        if profile and profile["resume"]: rfn=profile["resume"]
        else: conn.close(); flash("Upload a resume first.","danger"); return redirect(url_for("job_details",job_id=job_id))
    try:
        conn.execute("INSERT INTO applications(job_id,seeker_id,resume,cover_note,status) VALUES(?,?,?,?,'Applied')",(job_id,sid,rfn,cover_note)); conn.commit()
        flash(f"Applied to '{job['title']}'!","success")
    except: flash("Duplicate application prevented.","warning")
    finally: conn.close()
    return redirect(url_for("seeker_dashboard"))

@app.route("/api/job/<int:job_id>/vacancies")
def api_job_vacancies(job_id):
    conn=get_db()
    job=conn.execute("SELECT total_vacancy FROM jobs WHERE id=?",(job_id,)).fetchone()
    total_apps=conn.execute("SELECT COUNT(*) FROM applications WHERE job_id=?",(job_id,)).fetchone()[0]
    conn.close()
    if not job: return jsonify({"error":"Not found"}),404
    tv=job["total_vacancy"] or 1
    return jsonify({"total_vacancy":tv,"applications":total_apps,"remaining":max(0,tv-total_apps)})

# ---- SEEKER ----
@app.route("/seeker/dashboard")
@login_required("seeker")
def seeker_dashboard():
    conn=get_db(); uid=session["user_id"]
    apps=conn.execute("""SELECT applications.*,jobs.title AS job_title,jobs.location AS job_location,jobs.job_type,jobs.salary,companies.company_name,companies.website AS company_website FROM applications JOIN jobs ON applications.job_id=jobs.id LEFT JOIN companies ON jobs.recruiter_id=companies.recruiter_id WHERE applications.seeker_id=? ORDER BY applications.applied_at DESC""",(uid,)).fetchall()
    profile=conn.execute("""SELECT profiles.*,users.name,users.email FROM profiles JOIN users ON profiles.user_id=users.id WHERE profiles.user_id=?""",(uid,)).fetchone()
    counts={"total":len(apps),"applied":sum(1 for a in apps if a["status"]=="Applied"),"shortlisted":sum(1 for a in apps if a["status"]=="Shortlisted"),"interview":sum(1 for a in apps if a["status"]=="Interview"),"selected":sum(1 for a in apps if a["status"]=="Selected"),"rejected":sum(1 for a in apps if a["status"]=="Rejected")}
    open_jobs=conn.execute("""SELECT jobs.*,companies.company_name,companies.location AS comp_location FROM jobs LEFT JOIN companies ON jobs.recruiter_id=companies.recruiter_id WHERE jobs.status='Open'""").fetchall()
    recs=compute_smart_recommendations(dict(profile) if profile else {},open_jobs,limit=4)
    unread=conn.execute("SELECT COUNT(*) FROM messages WHERE receiver_id=? AND is_read=0",(uid,)).fetchone()[0]
    conn.close()
    return render_template("seeker-dashboard.html",applications=apps,profile=profile,counts=counts,recommendations=recs,unread_msgs=unread)

@app.route("/profile",methods=["GET","POST"])
@login_required("seeker")
def profile():
    conn=get_db(); uid=session["user_id"]
    if request.method=="POST":
        name=request.form.get("name","").strip()
        if name: conn.execute("UPDATE users SET name=? WHERE id=?",(name,uid)); session["name"]=name
        dp=request.form.get("degree_percentage","").strip()
        ey=request.form.get("experience_years","0").strip()
        conn.execute("""UPDATE profiles SET headline=?,phone=?,skills=?,education=?,degree=?,degree_percentage=?,experience=?,experience_years=?,bio=?,location=?,github=?,linkedin=? WHERE user_id=?""",
                     (request.form.get("headline","").strip(),request.form.get("phone","").strip(),request.form.get("skills","").strip(),request.form.get("education","").strip(),request.form.get("degree","").strip(),float(dp) if dp else None,request.form.get("experience","").strip(),int(ey) if ey.isdigit() else 0,request.form.get("bio","").strip(),request.form.get("location","").strip(),request.form.get("github","").strip(),request.form.get("linkedin","").strip(),uid))
        if "resume_file" in request.files:
            f=request.files["resume_file"]
            if f and f.filename:
                if allowed_file(f.filename):
                    sn=f"user_{uid}_{uuid.uuid4().hex[:6]}_{secure_filename(f.filename)}"; f.save(os.path.join(app.config["UPLOAD_FOLDER"],sn))
                    conn.execute("UPDATE profiles SET resume=? WHERE user_id=?",(sn,uid)); flash("Profile & resume updated!","success")
                else: flash("Resume must be PDF/DOC/DOCX.","warning")
            else: flash("Profile updated!","success")
        else: flash("Profile updated!","success")
        conn.commit()
    pd=conn.execute("""SELECT profiles.*,users.name,users.email FROM profiles JOIN users ON profiles.user_id=users.id WHERE profiles.user_id=?""",(uid,)).fetchone()
    conn.close(); return render_template("profile.html",profile=pd)

@app.route("/recommendations")
@login_required("seeker")
def smart_recommendations():
    conn=get_db(); uid=session["user_id"]
    profile=conn.execute("""SELECT profiles.*,users.name,users.email FROM profiles JOIN users ON profiles.user_id=users.id WHERE profiles.user_id=?""",(uid,)).fetchone()
    open_jobs=conn.execute("""SELECT jobs.*,companies.company_name,companies.location AS comp_location FROM jobs LEFT JOIN companies ON jobs.recruiter_id=companies.recruiter_id WHERE jobs.status='Open'""").fetchall()
    recs=compute_smart_recommendations(dict(profile) if profile else {},open_jobs,limit=12)
    conn.close(); return render_template("smart-recommendations.html",recommendations=recs,profile=profile)

@app.route("/resume-builder",methods=["GET","POST"])
@login_required("seeker")
def resume_builder():
    conn=get_db(); uid=session["user_id"]
    profile=conn.execute("""SELECT profiles.*,users.name,users.email FROM profiles JOIN users ON profiles.user_id=users.id WHERE profiles.user_id=?""",(uid,)).fetchone()
    bd=conn.execute("SELECT * FROM resume_builder WHERE user_id=?",(uid,)).fetchone()
    saved_data=json.loads(bd["data"]) if bd and bd["data"] else None
    if request.method=="POST":
        data={k:request.form.get(k,"") for k in ["full_name","email","phone","location","linkedin","github","objective","skills","education","degree","percentage","experience","projects","certifications","achievements","template_id"]}
        dj=json.dumps(data)
        if bd: conn.execute("UPDATE resume_builder SET data=?,template_id=?,updated_at=CURRENT_TIMESTAMP WHERE user_id=?",(dj,data["template_id"],uid))
        else: conn.execute("INSERT INTO resume_builder(user_id,template_id,data) VALUES(?,?,?)",(uid,data["template_id"],dj))
        conn.commit(); flash("Resume saved! Click 'Preview & Download' to view.","success"); saved_data=data
    conn.close(); return render_template("resume-builder.html",profile=profile,saved_data=saved_data)

@app.route("/resume-builder/preview")
@login_required("seeker")
def resume_builder_preview():
    conn=get_db(); bd=conn.execute("SELECT * FROM resume_builder WHERE user_id=?",(session["user_id"],)).fetchone(); conn.close()
    if not bd or not bd["data"]: flash("Fill resume builder first.","warning"); return redirect(url_for("resume_builder"))
    data=json.loads(bd["data"]); return render_template("resume-preview.html",data=data,template_id=data.get("template_id","modern"))

@app.route("/skill-gap",methods=["GET","POST"])
@login_required("seeker")
def skill_gap():
    conn=get_db(); uid=session["user_id"]
    profile=conn.execute("""SELECT profiles.*,users.name,users.email FROM profiles JOIN users ON profiles.user_id=users.id WHERE profiles.user_id=?""",(uid,)).fetchone()
    analysis=None; past=conn.execute("SELECT * FROM skill_gap_analyses WHERE seeker_id=? ORDER BY created_at DESC LIMIT 5",(uid,)).fetchall()
    if request.method=="POST":
        target_role=request.form.get("target_role","").strip()
        if not target_role: flash("Select a target role.","danger")
        else:
            usk=request.form.get("current_skills","").strip() or (profile["skills"] if profile else "")
            analysis=analyze_skill_gap(usk,target_role)
            conn.execute("INSERT INTO skill_gap_analyses(seeker_id,target_role,current_skills,required_skills,missing_skills,match_score,recommendations) VALUES(?,?,?,?,?,?,?)",(uid,target_role,usk,json.dumps(analysis["required_skills"]),json.dumps(analysis["missing_skills"]),analysis["match_score"],json.dumps(analysis["recommendations"])))
            conn.commit(); flash(f"Analysis complete! Match: {analysis['match_score']}%","success")
    conn.close(); return render_template("skill-gap.html",profile=profile,analysis=analysis,past_analyses=past)

@app.route("/resume-analyzer",methods=["GET","POST"])
@app.route("/analyzer",methods=["GET","POST"])
@login_required()
def resume_analyzer():
    conn=get_db(); uid=session["user_id"]
    profile=conn.execute("SELECT * FROM profiles WHERE user_id=?",(uid,)).fetchone()
    open_jobs=conn.execute("""SELECT jobs.*,companies.company_name,companies.location AS comp_location FROM jobs LEFT JOIN companies ON jobs.recruiter_id=companies.recruiter_id WHERE jobs.status='Open' ORDER BY jobs.created_at DESC""").fetchall()
    analysis_result=matched_jobs=resume_source_used=None
    if request.method=="POST":
        source=request.form.get("source","profile"); resume_text=""
        if source=="upload" and "resume_file" in request.files:
            f=request.files["resume_file"]
            if f and f.filename and allowed_file(f.filename):
                sn=f"analyze_{uuid.uuid4().hex[:8]}_{secure_filename(f.filename)}"; sp=os.path.join(app.config["UPLOAD_FOLDER"],sn); f.save(sp)
                resume_text=ai_analyzer.extract_text_from_file(sp); resume_source_used=f.filename
            else: flash("Upload valid PDF/DOC/DOCX.","danger")
        elif source=="text":
            resume_text=request.form.get("resume_text","").strip(); resume_source_used="Pasted Text"
        else:
            if profile and profile["resume"]:
                fp=os.path.join(app.config["UPLOAD_FOLDER"],profile["resume"]); resume_text=ai_analyzer.extract_text_from_file(fp); resume_source_used=profile["resume"]
            else: flash("No profile resume. Upload below.","warning")
        if resume_text:
            ps=profile["skills"] if profile else ""
            analysis_result=ai_analyzer.analyze_resume_profile(resume_text,ps); matched_jobs=ai_analyzer.match_resume_with_jobs(analysis_result["skills"],resume_text,open_jobs)
            flash(f"Analysis complete! {len(analysis_result['skills'])} skills, {len(matched_jobs)} matches.","success")
    elif profile and profile["resume"]:
        fp=os.path.join(app.config["UPLOAD_FOLDER"],profile["resume"])
        if os.path.exists(fp):
            rt=ai_analyzer.extract_text_from_file(fp)
            if rt:
                ps=profile["skills"] if profile else ""
                analysis_result=ai_analyzer.analyze_resume_profile(rt,ps); matched_jobs=ai_analyzer.match_resume_with_jobs(analysis_result["skills"],rt,open_jobs); resume_source_used=profile["resume"]
    conn.close(); return render_template("resume-analyzer.html",profile=profile,analysis=analysis_result,matched_jobs=matched_jobs,resume_source=resume_source_used,total_open_jobs=len(open_jobs))

@app.route("/coding-tests")
@login_required("seeker")
def coding_tests():
    conn=get_db(); uid=session["user_id"]
    tests=conn.execute("SELECT * FROM coding_tests ORDER BY created_at DESC").fetchall()
    subs=conn.execute("SELECT test_id,score,total_questions FROM test_submissions WHERE seeker_id=?",(uid,)).fetchall()
    sub_map={s["test_id"]:s for s in subs}; conn.close()
    return render_template("coding-tests.html",tests=tests,sub_map=sub_map)

@app.route("/coding-tests/<int:test_id>",methods=["GET","POST"])
@login_required("seeker")
def take_test(test_id):
    conn=get_db(); uid=session["user_id"]
    test=conn.execute("SELECT * FROM coding_tests WHERE id=?",(test_id,)).fetchone()
    if not test: conn.close(); flash("Test not found.","danger"); return redirect(url_for("coding_tests"))
    questions=conn.execute("SELECT * FROM coding_questions WHERE test_id=?",(test_id,)).fetchall()
    existing=conn.execute("SELECT * FROM test_submissions WHERE test_id=? AND seeker_id=?",(test_id,uid)).fetchone()
    result=None
    if request.method=="POST":
        if existing: conn.close(); flash("Already submitted.","warning"); return redirect(url_for("coding_tests"))
        answers={}; score=0
        for q in questions:
            ua=request.form.get(f"q_{q['id']}","").strip().upper(); answers[str(q["id"])]=ua
            if ua==q["correct_option"].upper(): score+=1
        conn.execute("INSERT INTO test_submissions(test_id,seeker_id,score,total_questions,answers) VALUES(?,?,?,?,?)",(test_id,uid,score,len(questions),json.dumps(answers))); conn.commit()
        result={"score":score,"total":len(questions),"percentage":int((score/max(len(questions),1))*100),"answers":answers}
        flash(f"Test submitted! Score: {score}/{len(questions)} ({result['percentage']}%)","success")
        existing=conn.execute("SELECT * FROM test_submissions WHERE test_id=? AND seeker_id=?",(test_id,uid)).fetchone()
    if existing and not result:
        ans=json.loads(existing["answers"]) if existing["answers"] else {}
        result={"score":existing["score"],"total":existing["total_questions"],"percentage":int((existing["score"]/max(existing["total_questions"],1))*100),"answers":ans}
    conn.close(); return render_template("take-test.html",test=test,questions=questions,result=result)

@app.route("/mock-interview",methods=["GET","POST"])
@login_required("seeker")
def mock_interview():
    conn=get_db(); uid=session["user_id"]
    categories=["Software Engineering","Data Science","System Design","Behavioral","Frontend Development"]
    if request.method=="POST":
        action=request.form.get("action","schedule")
        if action=="schedule":
            cat=request.form.get("category","Behavioral"); sdate=request.form.get("scheduled_date",""); stime=request.form.get("scheduled_time","")
            qs=generate_mock_questions(cat)
            conn.execute("INSERT INTO mock_interviews(seeker_id,category,scheduled_date,scheduled_time,status,questions) VALUES(?,?,?,?,'Scheduled',?)",(uid,cat,sdate,stime,json.dumps(qs))); conn.commit()
            flash(f"Mock interview scheduled for {sdate} at {stime}!","success")
        elif action=="submit":
            iid=request.form.get("interview_id"); iv=conn.execute("SELECT * FROM mock_interviews WHERE id=? AND seeker_id=?",(iid,uid)).fetchone()
            if iv:
                qs=json.loads(iv["questions"] or "[]")
                ans={str(i):request.form.get(f"answer_{i}","").strip() for i in range(len(qs))}
                score=sum(1 for i,q in enumerate(qs) if len(ans.get(str(i),""))>10)*2
                pct=int((score/max(len(qs)*2,1))*100)
                fb=("Excellent! Strong understanding shown." if pct>=80 else "Good effort! Review key concepts." if pct>=60 else "Keep practicing! Focus on core topics.")
                conn.execute("UPDATE mock_interviews SET status='Completed',answers=?,score=?,feedback=? WHERE id=?",(json.dumps(ans),pct,fb,iid)); conn.commit()
                flash(f"Interview complete! Score: {pct}%","success")
    past=conn.execute("SELECT * FROM mock_interviews WHERE seeker_id=? ORDER BY created_at DESC LIMIT 10",(uid,)).fetchall()
    conn.close(); return render_template("mock-interview.html",categories=categories,past_interviews=past)

@app.route("/mock-interview/<int:interview_id>/start")
@login_required("seeker")
def start_mock_interview(interview_id):
    conn=get_db(); iv=conn.execute("SELECT * FROM mock_interviews WHERE id=? AND seeker_id=?",(interview_id,session["user_id"])).fetchone(); conn.close()
    if not iv: flash("Interview not found.","danger"); return redirect(url_for("mock_interview"))
    qs=json.loads(iv["questions"] or "[]")
    return render_template("mock-interview-session.html",interview=iv,questions=qs)

@app.route("/messages")
@login_required()
def messages():
    conn=get_db(); uid=session["user_id"]
    inbox=conn.execute("""SELECT messages.*,users.name AS sender_name,users.email AS sender_email FROM messages JOIN users ON messages.sender_id=users.id WHERE messages.receiver_id=? ORDER BY messages.sent_at DESC""",(uid,)).fetchall()
    sent=conn.execute("""SELECT messages.*,users.name AS receiver_name,users.email AS receiver_email FROM messages JOIN users ON messages.receiver_id=users.id WHERE messages.sender_id=? ORDER BY messages.sent_at DESC""",(uid,)).fetchall()
    conn.execute("UPDATE messages SET is_read=1 WHERE receiver_id=?",(uid,)); conn.commit(); conn.close()
    return render_template("messages.html",inbox=inbox,sent=sent)

@app.route("/messages/compose",methods=["GET","POST"])
@login_required()
def compose_message():
    conn=get_db()
    if request.method=="POST":
        rid=request.form.get("receiver_id","").strip(); body=request.form.get("body","").strip(); subject=request.form.get("subject","").strip()
        if not rid or not body: flash("Fill all fields.","danger")
        elif not conn.execute("SELECT id FROM users WHERE id=?",(rid,)).fetchone(): flash("Recipient not found.","danger")
        else:
            conn.execute("INSERT INTO messages(sender_id,receiver_id,subject,body) VALUES(?,?,?,?)",(session["user_id"],rid,subject,body)); conn.commit(); conn.close()
            flash("Message sent!","success"); return redirect(url_for("messages"))
    role=session.get("role")
    if role=="seeker": recipients=conn.execute("SELECT id,name,email,role FROM users WHERE role IN('recruiter','admin') ORDER BY name").fetchall()
    elif role=="recruiter": recipients=conn.execute("SELECT id,name,email,role FROM users WHERE role IN('seeker','admin') ORDER BY name").fetchall()
    else: recipients=conn.execute("SELECT id,name,email,role FROM users WHERE id!=? ORDER BY name",(session["user_id"],)).fetchall()
    conn.close(); return render_template("compose-message.html",recipients=recipients,prefill_receiver=request.args.get("to",""),prefill_subject=request.args.get("subject",""))

@app.route("/messages/<int:msg_id>")
@login_required()
def view_message(msg_id):
    conn=get_db(); uid=session["user_id"]
    msg=conn.execute("""SELECT messages.*,sender.name AS sender_name,sender.email AS sender_email,recv.name AS receiver_name,recv.email AS receiver_email FROM messages JOIN users sender ON messages.sender_id=sender.id JOIN users recv ON messages.receiver_id=recv.id WHERE messages.id=? AND (messages.sender_id=? OR messages.receiver_id=?)""",(msg_id,uid,uid)).fetchone()
    if not msg: conn.close(); flash("Message not found.","danger"); return redirect(url_for("messages"))
    conn.execute("UPDATE messages SET is_read=1 WHERE id=?",(msg_id,)); conn.commit(); conn.close()
    return render_template("view-message.html",msg=msg)

@app.route("/report-fraud",methods=["GET","POST"])
@login_required()
def report_fraud():
    conn=get_db()
    if request.method=="POST":
        job_id=request.form.get("job_id","").strip() or None; reason=request.form.get("reason","").strip(); evidence=request.form.get("evidence","").strip()
        if not reason: flash("Provide a reason.","danger")
        else:
            conn.execute("INSERT INTO fraud_reports(reporter_id,job_id,reason,evidence) VALUES(?,?,?,?)",(session["user_id"],job_id,reason,evidence)); conn.commit()
            flash("Fraud report submitted.","success")
    jobs_list=conn.execute("SELECT id,title FROM jobs WHERE status='Open' ORDER BY title").fetchall(); conn.close()
    return render_template("report-fraud.html",jobs=jobs_list)

@app.route("/resume/download/<filename>")
def download_resume(filename):
    if "user_id" not in session: flash("Please log in.","warning"); return redirect(url_for("login"))
    sn=os.path.basename(filename); fp=os.path.join(app.config["UPLOAD_FOLDER"],sn)
    if not os.path.exists(fp): flash("File not found.","warning"); return redirect(request.referrer or url_for("index"))
    return send_from_directory(app.config["UPLOAD_FOLDER"],sn,as_attachment=True)

# ---- RECRUITER ----
@app.route("/recruiter/dashboard")
@login_required("recruiter")
def recruiter_dashboard():
    conn=get_db(); rid=session["user_id"]
    company=conn.execute("SELECT * FROM companies WHERE recruiter_id=?",(rid,)).fetchone()
    jobs_list=conn.execute("""SELECT jobs.*,COUNT(applications.id) AS total_applicants,SUM(CASE WHEN applications.status='Interview' THEN 1 ELSE 0 END) AS interview_count,SUM(CASE WHEN applications.status='Selected' THEN 1 ELSE 0 END) AS selected_count FROM jobs LEFT JOIN applications ON jobs.id=applications.job_id WHERE jobs.recruiter_id=? GROUP BY jobs.id ORDER BY jobs.created_at DESC""",(rid,)).fetchall()
    total_jobs=len(jobs_list); open_jobs=sum(1 for j in jobs_list if j["status"]=="Open"); total_applicants=sum(j["total_applicants"] for j in jobs_list)
    recent=conn.execute("""SELECT applications.*,users.name AS candidate_name,users.email AS candidate_email,jobs.title AS job_title FROM applications JOIN jobs ON applications.job_id=jobs.id JOIN users ON applications.seeker_id=users.id WHERE jobs.recruiter_id=? ORDER BY applications.applied_at DESC LIMIT 6""",(rid,)).fetchall()
    unread=conn.execute("SELECT COUNT(*) FROM messages WHERE receiver_id=? AND is_read=0",(rid,)).fetchone()[0]
    conn.close()
    return render_template("recruiter-dashboard.html",company=company,jobs=jobs_list,total_jobs=total_jobs,open_jobs=open_jobs,total_applicants=total_applicants,recent_applicants=recent,unread_msgs=unread)

@app.route("/recruiter/company",methods=["GET","POST"])
@login_required("recruiter")
def recruiter_company():
    conn=get_db(); rid=session["user_id"]
    if request.method=="POST":
        cn=request.form.get("company_name","").strip()
        if not cn: flash("Company name required.","danger")
        else:
            conn.execute("UPDATE companies SET company_name=?,industry=?,description=?,website=?,location=? WHERE recruiter_id=?",(cn,request.form.get("industry","").strip(),request.form.get("description","").strip(),request.form.get("website","").strip(),request.form.get("location","").strip(),rid)); conn.commit(); flash("Company profile updated!","success")
    company=conn.execute("SELECT * FROM companies WHERE recruiter_id=?",(rid,)).fetchone(); conn.close()
    return render_template("recruiter-company.html",company=company)

@app.route("/recruiter/job/create",methods=["GET","POST"])
@login_required("recruiter")
def create_job():
    if request.method=="POST":
        title=request.form.get("title","").strip(); desc=request.form.get("description","").strip()
        if not title or not desc: flash("Title and description required.","danger"); return redirect(url_for("create_job"))
        tv=request.form.get("total_vacancy","1"); me=request.form.get("min_experience","0"); mp=request.form.get("min_percentage","0")
        is_intern=1 if request.form.get("is_internship") else 0
        conn=get_db()
        conn.execute("""INSERT INTO jobs(recruiter_id,title,description,requirements,skills,location,job_type,salary,status,total_vacancy,min_experience,required_degree,min_percentage,is_internship,internship_duration,stipend) VALUES(?,?,?,?,?,?,?,?,'Open',?,?,?,?,?,?,?)""",
                     (session["user_id"],title,desc,request.form.get("requirements","").strip(),request.form.get("skills","").strip(),request.form.get("location","").strip(),request.form.get("job_type","Full-time"),request.form.get("salary","").strip(),int(tv) if tv.isdigit() else 1,int(me) if me.isdigit() else 0,request.form.get("required_degree","").strip(),float(mp) if mp else 0,is_intern,request.form.get("internship_duration","").strip() if is_intern else "",request.form.get("stipend","").strip() if is_intern else ""))
        conn.commit(); conn.close(); flash(f"Job '{title}' published!","success"); return redirect(url_for("recruiter_dashboard"))
    return render_template("recruiter-job-form.html",job=None,mode="create")

@app.route("/recruiter/job/<int:job_id>/edit",methods=["GET","POST"])
@login_required("recruiter")
def edit_job(job_id):
    conn=get_db(); job=conn.execute("SELECT * FROM jobs WHERE id=? AND recruiter_id=?",(job_id,session["user_id"])).fetchone()
    if not job: conn.close(); flash("Job not found.","danger"); return redirect(url_for("recruiter_dashboard"))
    if request.method=="POST":
        title=request.form.get("title","").strip(); tv=request.form.get("total_vacancy","1"); me=request.form.get("min_experience","0"); mp=request.form.get("min_percentage","0"); is_intern=1 if request.form.get("is_internship") else 0
        conn.execute("""UPDATE jobs SET title=?,job_type=?,location=?,salary=?,skills=?,description=?,requirements=?,status=?,total_vacancy=?,min_experience=?,required_degree=?,min_percentage=?,is_internship=?,internship_duration=?,stipend=? WHERE id=? AND recruiter_id=?""",
                     (title,request.form.get("job_type","Full-time"),request.form.get("location","").strip(),request.form.get("salary","").strip(),request.form.get("skills","").strip(),request.form.get("description","").strip(),request.form.get("requirements","").strip(),request.form.get("status","Open"),int(tv) if tv.isdigit() else 1,int(me) if me.isdigit() else 0,request.form.get("required_degree","").strip(),float(mp) if mp else 0,is_intern,request.form.get("internship_duration","").strip(),request.form.get("stipend","").strip(),job_id,session["user_id"]))
        conn.commit(); conn.close(); flash(f"Job '{title}' updated.","success"); return redirect(url_for("recruiter_dashboard"))
    conn.close(); return render_template("recruiter-job-form.html",job=job,mode="edit")

@app.route("/recruiter/job/<int:job_id>/toggle-status",methods=["POST"])
@login_required("recruiter")
def toggle_job_status(job_id):
    conn=get_db(); job=conn.execute("SELECT * FROM jobs WHERE id=? AND recruiter_id=?",(job_id,session["user_id"])).fetchone()
    if job:
        ns="Closed" if job["status"]=="Open" else "Open"
        conn.execute("UPDATE jobs SET status=? WHERE id=?",(ns,job_id)); conn.commit(); flash(f"Job is now {ns}.","info")
    else: flash("Job not found.","danger")
    conn.close(); return redirect(url_for("recruiter_dashboard"))

@app.route("/recruiter/job/<int:job_id>/delete",methods=["POST"])
@login_required("recruiter")
def delete_job_recruiter(job_id):
    conn=get_db(); conn.execute("DELETE FROM jobs WHERE id=? AND recruiter_id=?",(job_id,session["user_id"])); conn.commit(); conn.close()
    flash("Job removed.","success"); return redirect(url_for("recruiter_dashboard"))

@app.route("/recruiter/applicants")
@login_required("recruiter")
def recruiter_applicants():
    rid=session["user_id"]; jf=request.args.get("job_id",""); sf=request.args.get("status",""); conn=get_db()
    rjobs=conn.execute("SELECT id,title FROM jobs WHERE recruiter_id=? ORDER BY title",(rid,)).fetchall()
    q="""SELECT applications.*,users.name AS candidate_name,users.email AS candidate_email,profiles.phone AS candidate_phone,profiles.skills AS candidate_skills,profiles.headline AS candidate_headline,profiles.education AS candidate_education,profiles.experience AS candidate_experience,profiles.experience_years AS candidate_exp_years,profiles.degree AS candidate_degree,profiles.degree_percentage AS candidate_pct,profiles.bio AS candidate_bio,jobs.title AS job_title FROM applications JOIN jobs ON applications.job_id=jobs.id JOIN users ON applications.seeker_id=users.id LEFT JOIN profiles ON users.id=profiles.user_id WHERE jobs.recruiter_id=?"""
    p=[rid]
    if jf: q+=" AND applications.job_id=?"; p.append(jf)
    if sf: q+=" AND applications.status=?"; p.append(sf)
    q+=" ORDER BY applications.applied_at DESC"
    appls=conn.execute(q,p).fetchall(); conn.close()
    return render_template("recruiter-applicants.html",applicants=appls,jobs=rjobs,selected_job=jf,selected_status=sf)

@app.route("/recruiter/applicant/<int:app_id>/status",methods=["POST"])
@login_required("recruiter")
def update_applicant_status(app_id):
    ns=request.form.get("status")
    if ns not in ["Applied","Shortlisted","Interview","Selected","Rejected"]: flash("Invalid status.","danger"); return redirect(url_for("recruiter_applicants"))
    conn=get_db()
    rec=conn.execute("""SELECT applications.id,users.name,jobs.title FROM applications JOIN jobs ON applications.job_id=jobs.id JOIN users ON applications.seeker_id=users.id WHERE applications.id=? AND jobs.recruiter_id=?""",(app_id,session["user_id"])).fetchone()
    if not rec: conn.close(); flash("Not found.","danger"); return redirect(url_for("recruiter_applicants"))
    conn.execute("UPDATE applications SET status=? WHERE id=?",(ns,app_id)); conn.commit(); conn.close()
    flash(f"{rec['name']}'s status: {ns}.","success"); return redirect(request.referrer or url_for("recruiter_applicants"))

@app.route("/recruiter/applicant/<int:app_id>/interview",methods=["POST"])
@login_required("recruiter")
def schedule_interview(app_id):
    conn=get_db()
    rec=conn.execute("""SELECT applications.id,users.name,jobs.title FROM applications JOIN jobs ON applications.job_id=jobs.id JOIN users ON applications.seeker_id=users.id WHERE applications.id=? AND jobs.recruiter_id=?""",(app_id,session["user_id"])).fetchone()
    if not rec: conn.close(); flash("Not found.","danger"); return redirect(url_for("recruiter_applicants"))
    id_date=request.form.get("interview_date","").strip(); id_time=request.form.get("interview_time","").strip()
    conn.execute("""UPDATE applications SET status='Interview',interview_date=?,interview_time=?,interview_mode=?,interview_link=?,interview_notes=? WHERE id=?""",(id_date,id_time,request.form.get("interview_mode","Video Call"),request.form.get("interview_link","").strip(),request.form.get("interview_notes","").strip(),app_id))
    conn.commit(); conn.close(); flash(f"Interview scheduled for {rec['name']} on {id_date}.","success"); return redirect(request.referrer or url_for("recruiter_applicants"))

# ---- ADMIN ----
@app.route("/admin/dashboard")
@login_required("admin")
def admin_dashboard():
    conn=get_db()
    metrics={"users":{"total":conn.execute("SELECT COUNT(*) FROM users").fetchone()[0],"seekers":conn.execute("SELECT COUNT(*) FROM users WHERE role='seeker'").fetchone()[0],"recruiters":conn.execute("SELECT COUNT(*) FROM users WHERE role='recruiter'").fetchone()[0],"admins":conn.execute("SELECT COUNT(*) FROM users WHERE role='admin'").fetchone()[0]},"jobs":{"total":conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0],"open":conn.execute("SELECT COUNT(*) FROM jobs WHERE status='Open'").fetchone()[0],"closed":conn.execute("SELECT COUNT(*) FROM jobs WHERE status='Closed'").fetchone()[0],"internships":conn.execute("SELECT COUNT(*) FROM jobs WHERE is_internship=1").fetchone()[0]},"applications":{"total":conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0],"applied":conn.execute("SELECT COUNT(*) FROM applications WHERE status='Applied'").fetchone()[0],"shortlisted":conn.execute("SELECT COUNT(*) FROM applications WHERE status='Shortlisted'").fetchone()[0],"interview":conn.execute("SELECT COUNT(*) FROM applications WHERE status='Interview'").fetchone()[0],"selected":conn.execute("SELECT COUNT(*) FROM applications WHERE status='Selected'").fetchone()[0],"rejected":conn.execute("SELECT COUNT(*) FROM applications WHERE status='Rejected'").fetchone()[0]},"platform":{"pending_fraud":conn.execute("SELECT COUNT(*) FROM fraud_reports WHERE status='Pending'").fetchone()[0],"total_tests":conn.execute("SELECT COUNT(*) FROM coding_tests").fetchone()[0],"total_submissions":conn.execute("SELECT COUNT(*) FROM test_submissions").fetchone()[0]}}
    recent_users=conn.execute("SELECT * FROM users ORDER BY created_at DESC LIMIT 5").fetchall()
    recent_jobs=conn.execute("""SELECT jobs.*,companies.company_name FROM jobs LEFT JOIN companies ON jobs.recruiter_id=companies.recruiter_id ORDER BY jobs.created_at DESC LIMIT 5""").fetchall()
    conn.close(); return render_template("admin-dashboard.html",metrics=metrics,recent_users=recent_users,recent_jobs=recent_jobs)

@app.route("/admin/users")
@login_required("admin")
def admin_users():
    rf=request.args.get("role",""); sq=request.args.get("q","").strip(); conn=get_db()
    q="""SELECT users.*,CASE WHEN users.role='recruiter' THEN(SELECT company_name FROM companies WHERE recruiter_id=users.id) WHEN users.role='seeker' THEN(SELECT headline FROM profiles WHERE user_id=users.id) ELSE 'System Staff' END AS detail_info,CASE WHEN users.role='recruiter' THEN(SELECT COUNT(*) FROM jobs WHERE recruiter_id=users.id) WHEN users.role='seeker' THEN(SELECT COUNT(*) FROM applications WHERE seeker_id=users.id) ELSE 0 END AS activity_count FROM users WHERE 1=1"""
    p=[]
    if rf: q+=" AND users.role=?"; p.append(rf)
    if sq: q+=" AND (users.name LIKE ? OR users.email LIKE ?)"; k=f"%{sq}%"; p.extend([k,k])
    q+=" ORDER BY users.created_at DESC"
    users_list=conn.execute(q,p).fetchall(); conn.close()
    return render_template("admin-users.html",users=users_list,selected_role=rf,search_kw=sq)

@app.route("/admin/user/<int:user_id>/delete",methods=["POST"])
@login_required("admin")
def admin_delete_user(user_id):
    if user_id==session.get("user_id"): flash("Cannot delete your own account.","danger"); return redirect(url_for("admin_users"))
    conn=get_db(); u=conn.execute("SELECT name FROM users WHERE id=?",(user_id,)).fetchone()
    if u: conn.execute("DELETE FROM users WHERE id=?",(user_id,)); conn.commit(); flash(f"User '{u['name']}' deleted.","success")
    conn.close(); return redirect(url_for("admin_users"))

@app.route("/admin/jobs")
@login_required("admin")
def admin_jobs():
    sq=request.args.get("q","").strip(); sf=request.args.get("status",""); conn=get_db()
    q="""SELECT jobs.*,companies.company_name,users.name AS recruiter_name,users.email AS recruiter_email,COUNT(applications.id) AS applicant_count FROM jobs JOIN users ON jobs.recruiter_id=users.id LEFT JOIN companies ON jobs.recruiter_id=companies.recruiter_id LEFT JOIN applications ON jobs.id=applications.job_id WHERE 1=1"""
    p=[]
    if sf: q+=" AND jobs.status=?"; p.append(sf)
    if sq: q+=" AND (jobs.title LIKE ? OR companies.company_name LIKE ? OR jobs.location LIKE ?)"; k=f"%{sq}%"; p.extend([k,k,k])
    q+=" GROUP BY jobs.id ORDER BY jobs.created_at DESC"
    all_jobs=conn.execute(q,p).fetchall(); conn.close()
    return render_template("admin-jobs.html",jobs=all_jobs,search_kw=sq,selected_status=sf)

@app.route("/admin/job/<int:job_id>/delete",methods=["POST"])
@login_required("admin")
def admin_delete_job(job_id):
    conn=get_db(); job=conn.execute("SELECT title FROM jobs WHERE id=?",(job_id,)).fetchone()
    if job: conn.execute("DELETE FROM jobs WHERE id=?",(job_id,)); conn.commit(); flash(f"Job '{job['title']}' deleted.","success")
    conn.close(); return redirect(url_for("admin_jobs"))

@app.route("/admin/fraud-reports")
@login_required("admin")
def admin_fraud_reports():
    conn=get_db()
    reports=conn.execute("""SELECT fraud_reports.*,reporter.name AS reporter_name,jobs.title AS job_title FROM fraud_reports LEFT JOIN users reporter ON fraud_reports.reporter_id=reporter.id LEFT JOIN jobs ON fraud_reports.job_id=jobs.id ORDER BY fraud_reports.created_at DESC""").fetchall()
    conn.close(); return render_template("admin-fraud-reports.html",reports=reports)

@app.route("/admin/fraud-reports/<int:rid>/update",methods=["POST"])
@login_required("admin")
def update_fraud_report(rid):
    conn=get_db()
    conn.execute("UPDATE fraud_reports SET status=?,admin_notes=? WHERE id=?",(request.form.get("status","Reviewed"),request.form.get("admin_notes","").strip(),rid))
    conn.commit(); conn.close(); flash("Report updated.","success"); return redirect(url_for("admin_fraud_reports"))


@app.route("/network")
@login_required()
def network():
    conn=get_db(); uid=session["user_id"]
    # Get following
    following=conn.execute('''SELECT users.id,users.name,users.role,profiles.headline,companies.company_name FROM follows JOIN users ON follows.followed_id=users.id LEFT JOIN profiles ON users.id=profiles.user_id LEFT JOIN companies ON users.id=companies.recruiter_id WHERE follows.follower_id=?''',(uid,)).fetchall()
    # Get followers
    followers=conn.execute('''SELECT users.id,users.name,users.role,profiles.headline,companies.company_name FROM follows JOIN users ON follows.follower_id=users.id LEFT JOIN profiles ON users.id=profiles.user_id LEFT JOIN companies ON users.id=companies.recruiter_id WHERE follows.followed_id=?''',(uid,)).fetchall()
    # Get suggestions (people not followed)
    suggestions=conn.execute('''SELECT users.id,users.name,users.role,profiles.headline,companies.company_name FROM users LEFT JOIN profiles ON users.id=profiles.user_id LEFT JOIN companies ON users.id=companies.recruiter_id WHERE users.id!=? AND users.id NOT IN (SELECT followed_id FROM follows WHERE follower_id=?) LIMIT 20''',(uid,uid)).fetchall()
    conn.close()
    return render_template("network.html", following=following, followers=followers, suggestions=suggestions)

@app.route("/follow/<int:target_id>", methods=["POST"])
@login_required()
def toggle_follow(target_id):
    uid=session["user_id"]
    if uid==target_id: flash("Cannot follow yourself.","warning"); return redirect(url_for('network'))
    conn=get_db()
    existing=conn.execute("SELECT id FROM follows WHERE follower_id=? AND followed_id=?",(uid,target_id)).fetchone()
    if existing:
        conn.execute("DELETE FROM follows WHERE id=?",(existing["id"],))
        flash("Unfollowed successfully.","success")
    else:
        conn.execute("INSERT INTO follows(follower_id,followed_id) VALUES(?,?)",(uid,target_id))
        flash("Followed successfully.","success")
    conn.commit(); conn.close()
    return redirect(url_for('network'))
if __name__=="__main__":
    init_db()
    print("CareerPulse Portal running on http://127.0.0.1:5000")
    app.run(debug=True,host="127.0.0.1",port=5000)
