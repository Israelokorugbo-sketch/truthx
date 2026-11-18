from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os, json, threading, subprocess, sys
from datetime import datetime
from functools import wraps

# Fix imports for both direct and package run
try:
    from database import Base, engine, SessionLocal
    from models import User, Trade, Job, AppBuild
    from auth import create_token, verify_token, gen_api_key
except ImportError:
    from backend.database import Base, engine, SessionLocal
    from backend.models import User, Trade, Job, AppBuild
    from backend.auth import create_token, verify_token, gen_api_key

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND = os.path.join(ROOT, "frontend")
Base.metadata.create_all(bind=engine)

def get_db():
    return SessionLocal()

@app.route("/")
def root():
    idx = os.path.join(FRONTEND, "index.html")
    if os.path.exists(idx):
        return send_from_directory(FRONTEND, "index.html")
    return jsonify({"status": "Sovereign Builder HEAVY-DUTY", "mode": "production"})

@app.route("/api")
def api_info():
    return jsonify({"status": "HEAVY-DUTY API", "features": ["postgres-ready", "redis-ready", "jwt", "jobs"]})

@app.route("/health")
def health():
    db = get_db()
    try:
        users = db.query(User).count()
        jobs = db.query(Job).count()
        return jsonify({"ok": True, "users": users, "jobs": jobs})
    finally:
        db.close()

@app.route("/register", methods=["POST"])
def register():
    data = request.json or {}
    db = get_db()
    try:
        email = data.get("email")
        existing = db.query(User).filter(User.email == email).first() if email else None
        if existing:
            token = create_token(existing.id)
            return jsonify({"ok": True, "user_id": existing.id, "token": token})
        user = User(name=data.get("name",""), email=email, country=data.get("country","NG"), api_key=gen_api_key())
        db.add(user)
        db.commit()
        db.refresh(user)
        token = create_token(user.id)
        return jsonify({"ok": True, "user_id": user.id, "token": token})
    finally:
        db.close()

@app.route("/jobs", methods=["GET"])
def list_jobs():
    db = get_db()
    try:
        jobs = db.query(Job).order_by(Job.id.desc()).limit(50).all()
        return jsonify([{"id": j.id, "machine": j.machine, "status": j.status} for j in jobs])
    finally:
        db.close()

@app.route("/jobs/<int:job_id>")
def get_job(job_id):
    db = get_db()
    try:
        j = db.query(Job).filter(Job.id == job_id).first()
        if not j: return jsonify({"error": "not found"}), 404
        return jsonify({"id": j.id, "machine": j.machine, "status": j.status, "stdout": j.stdout, "stderr": j.stderr})
    finally:
        db.close()

@app.route("/run/<machine>", methods=["POST"])
def run_machine(machine):
    db = get_db()
    try:
        job = Job(machine=machine, status="queued")
        db.add(job)
        db.commit()
        db.refresh(job)
        job_id = job.id
    finally:
        db.close()

    def run_thread():
        db2 = SessionLocal()
        j = db2.query(Job).filter(Job.id == job_id).first()
        j.status = "running"
        db2.commit()
        script = os.path.join(ROOT, f"{machine}.py")
        try:
            result = subprocess.run([sys.executable, script], capture_output=True, text=True, timeout=600, cwd=ROOT)
            j.stdout = result.stdout[-10000:]
            j.stderr = result.stderr[-5000:]
            j.status = "done" if result.returncode==0 else "failed"
        except Exception as e:
            j.stderr = str(e)
            j.status = "failed"
        from datetime import datetime
        j.finished_at = datetime.utcnow()
        db2.commit()
        db2.close()

    threading.Thread(target=run_thread, daemon=True).start()
    return jsonify({"ok": True, "job_id": job_id, "check": f"/jobs/{job_id}"})

@app.route("/<path:path>")
def serve_frontend(path):
    full = os.path.join(FRONTEND, path)
    if os.path.exists(full):
        return send_from_directory(FRONTEND, path)
    idx = os.path.join(FRONTEND, "index.html")
    if os.path.exists(idx):
        return send_from_directory(FRONTEND, "index.html")
    return jsonify({"error":"not found"}), 404
