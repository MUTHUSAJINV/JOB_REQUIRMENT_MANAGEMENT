import os, re
path = r'c:\Users\SAJIN\OneDrive\Desktop\job\app.py'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add table to init_db
init_db_patch = """    conn.execute('''CREATE TABLE IF NOT EXISTS follows(id INTEGER PRIMARY KEY AUTOINCREMENT,follower_id INTEGER NOT NULL,followed_id INTEGER NOT NULL,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(follower_id)REFERENCES users(id)ON DELETE CASCADE,FOREIGN KEY(followed_id)REFERENCES users(id)ON DELETE CASCADE,UNIQUE(follower_id,followed_id))''')
    conn.execute('''CREATE TABLE IF NOT EXISTS resume_builder"""
content = content.replace('    conn.execute("""CREATE TABLE IF NOT EXISTS resume_builder', init_db_patch)

# 2. Add Network Routes at the bottom of the file (before app.run if it existed, but it doesn't, so just append)
routes_addition = """
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
"""
if "/network" not in content:
    content += routes_addition

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("app.py updated with Network logic")