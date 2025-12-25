import sqlite3
from contextlib import contextmanager
from app.core.config import settings

def init_db():
    with sqlite3.connect(settings.DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    prompt TEXT NOT NULL,
                    status TEXT NOT NULL,
                    seed INTEGER NOT NULL,
                    height INTEGER NOT NULL,
                    width INTEGER NOT NULL,
                    num_inference_steps INTEGER NOT NULL,
                    file_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        yield conn
    finally:
        conn.close()
                     