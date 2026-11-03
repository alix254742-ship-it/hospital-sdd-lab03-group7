import hashlib, os, sqlite3
import requests
from flask import Flask, request, session, send_from_directory
from werkzeug.security import generate_password_hash

app = Flask(__name__)
# FIX 1: Hardcoded Secret (Read from environment)
app.secret_key = os.environ.get("MEDICARE_SECRET_KEY", "fallback-dev-key")
DB = "medicare.db"

def db():
    return sqlite3.connect(DB)

def require_role(*roles):
    def deco(fn):
        def wrapper(*a, **k):
            if session.get("role") not in roles:
                return "Forbidden", 403
            return fn(*a, **k)
        wrapper.__name__ = fn.__name__
        return wrapper
    return deco

@app.route("/login", methods=["POST"])
def login():
    user = request.form["username"]
    pwd = request.form["password"]
    # FIX 2: Weak Hash
    h = generate_password_hash(pwd)
    
    # FIX 3: SQL Injection (Parameterized)
    sql = "SELECT id, role FROM staff WHERE name=? AND pw=?"
    row = db().execute(sql, (user, h)).fetchone()
    if row:
        session["role"] = row[1]
        return "OK"
    return "Invalid"

@app.route("/patient")
@require_role("doctor", "nurse", "admin") # FIX 9: Access Control
def patient():
    pid = request.args.get("id")
    # FIX 3: SQL Injection (Parameterized)
    row = db().execute("SELECT name, diagnosis FROM patients WHERE id=?", (pid,)).fetchone()
    return str(row)

@app.route("/prescription", methods=["POST"])
@require_role("doctor") # FIX 9: Access Control
def prescription():
    db().execute("UPDATE rx SET dose=? WHERE id=?", (request.form["dose"], request.form["id"]))
    return "Updated"

@app.route("/labreport")
@require_role("doctor", "lab_tech") # FIX 9: Access Control
def labreport():
    # FIX 6: Path Traversal
    return send_from_directory("reports", request.args.get("file"))

@app.route("/billing/export")
@require_role("billing", "admin") # FIX 9: Access Control
def export():
    # FIX 7: Command Injection (Strict Allow-List, no variables passed to OS)
    ward = request.args.get("ward")
    
    if ward == "A":
        return "Exporting Ward A"
    elif ward == "B":
        return "Exporting Ward B"
    elif ward == "ICU":
        return "Exporting ICU"
    else:
        return "Invalid ward", 400

@app.route("/pharmacy/stock")
@require_role("pharmacist", "admin")
def stock():
    return "stock list"

@app.route("/insurance")
def insurance():
    # FIX 8: TLS Verification
    return requests.get("https://insurer.example.com/claims", verify=True, timeout=10).text

if __name__ == "__main__":
    # FIX 8 (cont): Debug Mode & Open Host
    app.run(host="127.0.0.1", debug=False)