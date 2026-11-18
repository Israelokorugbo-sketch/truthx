import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery("sovereign", broker=REDIS_URL, backend=REDIS_URL)
celery_app.conf.update(
    task_track_started=True,
    task_time_limit=600,
    worker_concurrency=4,
)

@celery_app.task(bind=True)
def run_machine_task(self, job_id, machine, root_dir):
    import subprocess, sys
    from datetime import datetime
    from .database import SessionLocal
    from .models import Job
    import os

    db = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()
    if job:
        job.status = "running"
        db.commit()

    script = os.path.join(root_dir, f"{machine}.py")
    try:
        result = subprocess.run([sys.executable, script], capture_output=True, text=True, timeout=600, cwd=root_dir)
        stdout = result.stdout[-10000:]
        stderr = result.stderr[-5000:]
        status = "done" if result.returncode == 0 else "failed"
    except Exception as e:
        stdout = ""
        stderr = str(e)
        status = "failed"

    if job:
        job.stdout = stdout
        job.stderr = stderr
        job.status = status
        job.finished_at = datetime.utcnow()
        db.commit()
    db.close()
    return {"status": status, "stdout": stdout}
