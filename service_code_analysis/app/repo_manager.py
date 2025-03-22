import os
import uuid
import subprocess
from threading import Lock

jobs = {}
jobs_lock = Lock()

def create_job(repo_url: str) -> str:
    job_id = str(uuid.uuid4())
    repo_path = os.path.join("repos", job_id)
    os.makedirs(repo_path, exist_ok=True)
    jobs[job_id] = {"repo_url": repo_url, "repo_path": repo_path, "status": "pending"}
    return job_id

def download_repo(job_id: str):
    job = jobs.get(job_id)
    if not job:
        return
    repo_url = job["repo_url"]
    repo_path = job["repo_path"]
    try:
        subprocess.run(["git", "clone", repo_url, repo_path], check=True)
        print('status = completed')
        job["status"] = "completed"
    except Exception as e:
        print('status = failed', str(e))
        job["status"] = "failed"
        job["error"] = str(e)
