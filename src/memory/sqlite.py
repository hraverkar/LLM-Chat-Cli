from pathlib import Path
import sqlite3

class SQLiteMemory:
    def __init__(self, db_path: str ="data/mychat.db"):
        self.db_path = Path(db_path)

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()


    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _initialize_database(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
            Create TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                role TEXT,
                content TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations (id)
            )''')
            conn.commit()

    def create_conversation(self) -> int:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO conversations DEFAULT VALUES')
            conn.commit()
            return cursor.lastrowid

    def add_message(self, conversation_id: int, role: str, content: str):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO messages (conversation_id, role, content)
                VALUES (?, ?, ?)
            ''', (conversation_id, role, content))
            conn.commit()

    def get_conversation(self, conversation_id: int) -> list[dict]:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT role, content, created_at
                FROM messages
                WHERE conversation_id = ?
                ORDER BY created_at ASC
            ''', (conversation_id,))
            rows = cursor.fetchall()
        return [{'role': row[0], 'content': row[1], 'created_at': row[2]} for row in rows]
