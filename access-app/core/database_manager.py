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
            is_filename_taken = self._check_filename_in_db(generated_filename)
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

    def get_document_id_by_stored_filename(self, stored_filename: str) -> Optional[int]:
        """
        Retrieves the ID of a document given its filename inside the database.

        Args:
            stored_filename: The filename of the document inside the database

        Returns:
            The integer document_id if found, or None if the document does not exist
            or a database error occurs.
        """
        sql_select = "SELECT doc_id FROM Documents WHERE stored_filename = ?;"
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql_select, (stored_filename,))
                row = cursor.fetchone()
                if row:
                    return row[0]  # Returns the ID of the existing document
                else:
                    print(f"INFO: Document '{stored_filename}' not found")
                    return None
        except sqlite3.Error as e:
            print(
                f"ERROR: SQLite error while trying to retrieve doc_id for stored_filename '{stored_filename}':\n{e}"
            )
            return None

    def get_document_by_id(self, doc_id: int) -> Optional[dict]:
        """
        Retrieves all details of a document given its ID.

        Args:
            doc_id: The ID of the document to retrieve.

        Returns:
            A dictionary containing the document's details (column_name: value)
            if found, or None if the document does not exist or a database
            error occurs.
        """
        sql_select = "SELECT doc_id, original_filename, stored_filename, import_date, doc_length FROM Documents WHERE doc_id = ?;"
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql_select, (doc_id,))
                row = cursor.fetchone()
                if row:
                    column_names = [
                        description[0] for description in cursor.description
                    ]
                    document_details: dict = dict(zip(column_names, row))
                    return document_details
                else:
                    print(f"INFO: Document with id '{doc_id}' not found")
                    return None
        except sqlite3.Error as e:
            print(
                f"ERROR: SQLite error while trying to retrieve document for doc_id '{doc_id}':\n{e}"
            )
            return None

    def get_or_create_tag(self, tag: str) -> Optional[int]:
        """
        Create a new tag to the Tags table if it doesn't already exist.
        If the tag exists, its tag_id is returned. (Get-or-create pattern)

        Args:
            tag: The text of the tag.

        Returns:
            The tag_id of the tag (newly created or existing), or None on error.
        """
        sql_insert = """
            INSERT INTO Tags (tag_text)
            VALUES (?);
        """
        sql_select_id = "SELECT tag_id FROM Tags WHERE tag_text = ?;"

        is_tag_in_db = self._check_tag_in_db(tag)

        if is_tag_in_db:
            try:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(sql_select_id, (tag,))
                    row = cursor.fetchone()
                    if row:
                        return row[0]  # Returns the ID of the existing tag
                    else:
                        # This case is strange: _check_tag_in_db reported that it exists,
                        # but now we can't find it. It could be a race condition
                        # very rare or a logical error.
                        print(
                            f"ERROR: Tag '{tag}' reported as existing but not found when fetching ID."
                        )
                        return None
            except sqlite3.Error as e:
                print(
                    f"ERROR: SQLite error while fetching ID for existing tag '{tag}':\n{e}"
                )
                return None
        elif not is_tag_in_db:
            try:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(sql_insert, (tag,))
                    conn.commit()
                    return cursor.lastrowid
            except sqlite3.Error as e:
                print(f"ERROR: SQLite error while adding tag '{tag}':\n{e}")
                return None
        elif is_tag_in_db is None:
            return None

    def get_tag_id_by_text(self, tag_text: str) -> Optional[int]:
        """
        Retrieves the ID of a tag given its text.

        Args:
            tag_text: The text of the tag to look up.

        Returns:
            The integer tag_id if found, or None if the tag does not exist
            or a database error occurs.
        """
        sql_select = "SELECT tag_id FROM Tags WHERE tag_text = ?;"
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql_select, (tag_text,))
                row = cursor.fetchone()
                if row:
                    return row[0]  # Returns the ID of the existing tag
                else:
                    print(f"INFO: Tag '{tag_text}' not found")
                    return None
        except sqlite3.Error as e:
            print(
                f"ERROR: SQLite error while trying to retrieve tag_id for tag '{tag_text}':\n{e}"
            )
            return None

    def link_document_tag(
        self,
        doc_id: int,
        tag_id: int,
        score: Optional[float] = None,  # Consistency with column name
    ) -> bool:
        """
        Links a document to a tag in the DocumentTags table.
        If the link already exists, the operation is still considered successful
        (as the link is present). An optional score can be provided.

        Args:
            doc_id: The ID of the document.
            tag_id: The ID of the tag.
            score: Optional score for the document-tag association.

        Returns:
            True if the link was successfully created or already existed without error,
            False if a foreign key constraint was violated or another SQLite error occurred.
        """
        # If the pair (doc_id, tag_id) already exists, IGNORE prevents the error.
        # If doc_id or tag_id do not exist in the referenced tables, IntegrityError will be raised (FK violation).
        sql = """
            INSERT OR IGNORE INTO DocumentTags (doc_id, tag_id, score)
            VALUES (?, ?, ?);
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (doc_id, tag_id, score))
                conn.commit()
                # If rowcount is 0 and there are no errors, it means the link already existed.
                if cursor.rowcount > 0:
                    print(
                        f"INFO: Link created between doc_id {doc_id} and tag_id {tag_id}."
                    )
                else:
                    print(
                        f"INFO: Link between doc_id {doc_id} and tag_id {tag_id} already existed or no change made."
                    )
                return True
        except sqlite3.IntegrityError as e:
            # With INSERT OR IGNORE, this error is most likely due to a FOREIGN KEY violation.
            print(
                f"ERROR: Failed to link doc_id {doc_id} with tag_id {tag_id}. "
                f"This is likely due to a non-existent doc_id or tag_id (Foreign Key violation): {e}"
            )
            return False
        except sqlite3.Error as e:
            print(
                f"ERROR: SQLite error linking doc_id {doc_id} with tag_id {tag_id}: {e}"
            )
            return False

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
                        score REAL,
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

    def _check_filename_in_db(self, filename: str) -> Optional[bool]:
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

    def _check_tag_in_db(self, tag: str) -> Optional[bool]:
        """
        Checks if a given tag already exists in the Tags table.

        Args:
            tag: The stored filename to check.

        Returns:
            True if the tag exists, False if it doesn't, and None if
            a database error occurred.
        """
        sql_select = """
            SELECT 1 FROM Tags WHERE tag_text = ? LIMIT 1;"
        """

        # Check if the given filename is inside the database
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    sql_select,
                    (tag,),
                )
                return (
                    cursor.fetchone()
                    is not None  # True if filename exists in the database
                )
        except sqlite3.Error as e:
            print(
                f"ERROR: An error occurred while looking for a tag in the database:\n{e}"
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


if __name__ == "__main__":
    print(f"Default database path: {DEFAULT_DB_PATH}")
    if os.path.exists(DEFAULT_DB_PATH):
        os.remove(DEFAULT_DB_PATH)

    db_manager = DatabaseManager()
    print(
        f"DatabaseManager initialized. The database file is located at: {db_manager.db_path}"
    )
