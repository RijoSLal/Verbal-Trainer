import sqlite3

DB_PATH = "database/user_data.db"

def init_db():
    """Initializes the SQLite database and creates tables if they don't exist."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    module_type TEXT NOT NULL,
                    user_input TEXT DEFAULT '',
                    ai_feedback TEXT DEFAULT '',
                    score REAL DEFAULT 0,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
        print("✅ Database initialized successfully.")
    except Exception as e:
        print(f"⚠️ Database Initialization Error: {e}")

def save_user_response(session_id, module, user_input, feedback, score):
    """Saves the user's training session and AI feedback to the database."""
    try:
        if not session_id or not module:
            print("⚠️ Error: Missing required fields (session_id, module)")
            return

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user_progress (session_id, module_type, user_input, ai_feedback, score)
                VALUES (?, ?, ?, ?, ?)
            """, (session_id, module, user_input or "N/A", feedback or "No feedback", score or 0))
            conn.commit()
        print(f"✅ Data saved for session: {session_id} | Module: {module}")
    except Exception as e:
        print(f"⚠️ Database Save Error: {e}")

def get_user_progress(session_id):
    """Retrieves all past training sessions for a given user session."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT module_type, user_input, ai_feedback, score, timestamp
                FROM user_progress WHERE session_id = ?
                ORDER BY timestamp DESC
            """, (session_id,))
            progress = cursor.fetchall()

        if not progress:
            print(f"⚠️ No progress data found for session: {session_id}")
            return []

        print(f"✅ Retrieved {len(progress)} records for session: {session_id}")
        return progress
    except Exception as e:
        print(f"⚠️ Database Query Error: {e}")
        return []
