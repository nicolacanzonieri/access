import os
import sqlite3
from typing import Optional

PROJECT_ROOT_DIR: str = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
DEFAULT_DB_PATH: str = os.path.join(
    PROJECT_ROOT_DIR, "data", "learned", "access_main.db"
)


class DatabaseManager:
    db_path: str

    def __init__(self, db_path: Optional[str] = None):
        # Use given db_path if not None, otherwise use the default one
        self.db_path = db_path if db_path is not None else DEFAULT_DB_PATH

        # Check database folder
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            try:
                os.makedirs(db_dir, exist_ok=True)
            except OSError as error:
                print(f"Error while creating database directory:\n{error}")

        # Initialize SQLite tables
        self._create_table()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _create_table(self):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()

                # Documents Table
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS Documents (
                        doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        original_filename TEXT NOT NULL,
                        stored_filename TEXT NOT NULL UNIQUE,
                        import_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        doc_length INTEGER
                    )
                """
                )

                # Tags Table
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS Tags (
                        tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tag_text TEXT NOT NULL UNIQUE
                    )
                """
                )

                # DocumentTags Table
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS DocumentTags (
                        doc_id INTEGER NOT NULL,
                        tag_id INTEGER NOT NULL,
                        tf_idf_score REAL,
                        PRIMARY KEY (doc_id, tag_id),
                        FOREIGN KEY (doc_id) REFERENCES Documents(doc_id) ON DELETE CASCADE,
                        FOREIGN KEY (tag_id) REFERENCES Tags(tag_id) ON DELETE CASCADE
                    )
                """
                )

                # Indices
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_doc_id_on_documenttags ON DocumentTags (doc_id);"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_tag_id_on_documenttags ON DocumentTags (tag_id);"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_tag_text_on_tags ON Tags (tag_text);"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_stored_filename_on_documents ON Documents (stored_filename);"
                )

        except sqlite3.Error as e:
            print(f"SQLite error during table creation: {e}")
            # Consider whether propagating the exception is appropriate here
            # if table creation is a critical failure for the application.
            raise


if __name__ == "__main__":
    print(f"Default database path: {DEFAULT_DB_PATH}")
    if os.path.exists(DEFAULT_DB_PATH):
        os.remove(DEFAULT_DB_PATH)

    db_manager = DatabaseManager()
    print(
        f"DatabaseManager initialized. The database file is located at: {db_manager.db_path}"
    )
