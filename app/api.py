from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import get_connection
from app.app_logic import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/applications")
def get_applications():
    conn = get_connection()
    cur = conn.cursor()
    init_db(cur)

    cur.execute("SELECT id, company, role, stage FROM applications ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()

    return [{"id": r[0], "company": r[1], "role": r[2], "stage": r[3]} for r in rows]

@app.get("/summary")
def get_summary():
    conn = get_connection()
    cur = conn.cursor()
    init_db(cur)

    cur.execute("""
        SELECT stage, COUNT(*) AS count
        FROM applications
        GROUP BY stage
        ORDER BY count DESC
    """)
    rows = cur.fetchall()
    conn.close()

    return [{"stage": r[0], "count": r[1]} for r in rows]
