import os, sys
# Fix Termux path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "backend"))

from main import app
from waitress import serve

port = int(os.getenv("PORT", 8000))
print(f"HEAVY-DUTY Sovereign Builder starting on 0.0.0.0:{port}")
print(f"DB: {os.getenv('DATABASE_URL','sqlite local')[:60]}")
serve(app, host="0.0.0.0", port=port, threads=32, connection_limit=200)
