import os
import sqlite3
import uuid
from typing import Optional

PROJECT_ROOT_DIR: str = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
DEFAULT_DB_PATH: str = os.path.join(
    PROJECT_ROOT_DIR, "data", "learned", "access_main.db"
)


class DatabaseManager:
    """
    Manages the SQLite database for storing document and tag information.
    Handles database connection, table creation, and basic document operations.
    """

    db_path: str

    def __init__(self, db_path: Optional[str] = None) -> None:
        """
        Initializes the DatabaseManager.

        Args:
            db_path: Optional path to the SQLite database file.
                     If None, the default path is used.
        """
        # Use given db_path if not None, otherwise use the default one
        self.db_path = db_path if db_path is not None else DEFAULT_DB_PATH

        # Check database folder
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            try:
                os.makedirs(db_dir, exist_ok=True)
            except OSError as e:
                print(
                    f"ERROR: An error occurred while creating database directory:\n{e}"
                )

        # Initialize SQLite tables
        self._create_table()

    def _get_connection(self) -> sqlite3.Connection:
        """
        Establishes and returns a connection to the SQLite database.
        Ensures foreign key support is enabled.

        Returns:
            A sqlite3.Connection object.
        """
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _create_table(self) -> None:
        """
        Creates the necessary tables (Documents, Tags, DocumentTags)
        in the database if they do not already exist. Also creates relevant indices.
        """
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
            print(f"ERROR: SQLite error during table creation:\n{e}")
            raise

    def _check_db_filename(self, filename: str) -> Optional[bool]:
        """
        Checks if a given stored filename already exists in the Documents table.

        Args:
            filename: The stored filename to check.

        Returns:
            True if the filename exists, False if it doesn't, and None if
            a database error occurred.
        """
        sql_select = """
            SELECT 1 FROM Documents WHERE stored_filename = ? LIMIT 1;"
        """

        # Check if the given filename is inside the database
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    sql_select,
                    (filename,),
                )
                return (
                    cursor.fetchone()
                    is not None  # True if filename exists in the database
                )
        except sqlite3.Error as e:
            print(
                f"ERROR: An error occurred while looking for a taken filename in the database:\n{e}"
            )
            return None

    def _generate_unique_filename(self, filename: str) -> str:
        """
        Generates a unique filename using UUID, preserving the original file extension.

        Args:
            filename: The original filename to extract the extension from.

        Returns:
            A unique string intended for use as a stored filename.
        """
        _, ext = os.path.splitext(filename)  # Get the extension of the given file
        return str(uuid.uuid4().hex) + ext  # Return a unique filename

    def add_document(self, original_filename: str, doc_length: int) -> Optional[int]:
        """
        Adds a new document to the Documents table.
        A unique stored_filename (UUID + extension) is generated internally.

        Args:
            original_filename: The original name of the document file.
            doc_length: The length of the document.

        Returns:
            The doc_id of the newly added document, or None if the document
            could not be added.
        """
        sql_insert = """
            INSERT INTO Documents (original_filename, stored_filename, doc_length)
            VALUES (?, ?, ?);
        """

        # Generate a unique filename for the document in the database. This filename
        # is generated at maximum 5 times before giving up
        stored_filename: str = ""
        max_attempts = 5
        for attempt in range(max_attempts):
            generated_filename = self._generate_unique_filename(original_filename)
            is_filename_taken = self._check_db_filename(generated_filename)
            if is_filename_taken is not None and not is_filename_taken:
                stored_filename = generated_filename
                break
            elif attempt == max_attempts - 1:
                print("ERROR: generated 5 not unique filenames for the document!")
                return None

        # Insert the document in the database
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    sql_insert,
                    (original_filename, stored_filename, doc_length),
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(
                f"ERROR: Cannot add document. 'stored_filename' ({stored_filename}) already exists:\n{e}"
            )
            return None
        except sqlite3.Error as e:
            print(
                f"ERROR: SQLite error while adding document '{original_filename}':\n{e}"
            )
            return None


if __name__ == "__main__":
    print(f"Default database path: {DEFAULT_DB_PATH}")
    if os.path.exists(DEFAULT_DB_PATH):
        os.remove(DEFAULT_DB_PATH)

    db_manager = DatabaseManager()
    print(
        f"DatabaseManager initialized. The database file is located at: {db_manager.db_path}"
    )
