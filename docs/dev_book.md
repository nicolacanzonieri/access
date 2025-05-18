# ACCESS v3: Development Book

**Key Files and Decisions:**

*   **`pyproject.toml`**:
    *   Adopted as the central file for project configuration (metadata, dependencies) and development tools.
    *   **Development Dependencies (`[project.optional-dependencies].dev`):**
        *   `black` (formatter)
        *   `flake8` (linter)
        *   `isort` (import sorter)
        *   `mypy` (type checker)
        *   `pre-commit` (for automatic git hooks)
        *   `pytest` (for future tests)
    *   **Tool Configuration:** Includes `[tool.black]`, `[tool.isort]`, `[tool.flake8]`, `[tool.mypy]` sections with basic settings (e.g., `line-length = 88`).
*   **Code Quality Automation (Planned):**
    *   **Pre-commit Hooks:** Will be configured via `.pre-commit-config.yaml` to automatically run `black`, `isort`, `flake8`, `mypy` before each commit.
    *   **GitHub Actions (CI):** Will be configured in `.github/workflows/` for automatic checks on push/pull requests.
*   **Source Code in `access-app/`**:
    *   The main application code resides in this package for better organization and importability.

## Key Architectural Components (Decisions Made)

### 1. Tag Data Persistence

*   **Technology Choice:** **SQLite**.
    *   **Motivation:** Integrated into Python (no heavy external dependencies for the end user), file-based, transactional, supports indexes for good performance on targeted queries. Suitable for the initial scalability required.
    *   **Discarded Alternative (for now):** Monolithic JSON file (not scalable).
    *   **Possible Future Alternative:** Text search engines (e.g., Whoosh) if search complexity grows significantly.
*   **Dedicated Manager:** An `access-app.core.database_manager.DatabaseManager` class.
    *   **Responsibility:** Encapsulate all interaction with SQLite (connections, SQL execution, schema creation). Provide a clean API to the rest of the application.
    *   **Current State of `database_manager.py`:**
        *   Definition of the database path (`DEFAULT_DB_PATH` pointing to `data/learned/access_main.db`).
        *   `__init__` constructor that sets `self.db_path`, ensures the database directory exists, and calls `_create_table()`.
        *   `_create_table()` method implemented with `CREATE TABLE IF NOT EXISTS` queries for `Documents`, `Tags`, `DocumentTags`, and corresponding `CREATE INDEX IF NOT EXISTS`.
        *   `_get_connection()` helper method implemented to centralize connection logic and enable `PRAGMA foreign_keys = ON;`.
        *   Helper methods `_check_filename_in_db()`, `_check_tag_in_db()`, and `_generate_unique_filename()` implemented.
        *   CRUD Method `add_document()` implemented, including logic for generating a unique `stored_filename` with collision detection.
        *   CRUD Method `get_or_create_tag()` implemented (get-or-create pattern for tags).
*   **SQLite Database Schema (Implemented):**
    *   **`Documents`**: `doc_id` (PK), `original_filename`, `stored_filename` (UNIQUE), `import_date`, `doc_length`.
    *   **`Tags`**: `tag_id` (PK), `tag_text` (UNIQUE).
    *   **`DocumentTags`**: `doc_id` (FK), `tag_id` (FK), `tf_idf_score` (REAL). `PRIMARY KEY (doc_id, tag_id)`. `ON DELETE CASCADE` for foreign keys.

### 2. Document Processing (NLP Algorithm)

*   **Technology Choice (Current):** Custom internally developed algorithm (external NLP libraries like spaCy or NLTK will *not* be used *in this phase*).
    *   **Motivation:** Maintain full control over the algorithm, reduce initial external dependencies, learning opportunity.
    *   **Flexibility:** The system will be designed so that this component (`DocumentProcessor`) can be replaced in the future if necessary.
*   **Planned Components (to be defined/developed):**
    *   `DocumentProcessor`: Responsible for tokenization, cleaning, lowercasing, stop-word removal (user-defined), lemmatization (according to custom logic).
    *   `TagExtractor`: Responsible for calculating term frequency (TF) for a document.

### 3. Tag Weight Calculation

*   **Algorithm Choice (Initial):** **TF-IDF (Term Frequency-Inverse Document Frequency)**.
    *   **Motivation:** Well-understood standard, relatively simple to implement on top of SQLite, improves relevance compared to just term frequency.
    *   **Implementation:**
        *   TF calculated by `TagExtractor`.
        *   IDF calculable via queries on `Documents` and `DocumentTags` (managed by `DatabaseManager`).
        *   The final TF-IDF score will be stored in `DocumentTags.tf_idf_score`.
*   **Planned Component (to be defined/developed):**
    *   `ScoringEngine`: Could contain logic for calculating TF-IDF and, in the future, other scoring models.

### 4. Tag Expansion

*   **Status:** To be discussed and defined in a later phase. The database infrastructure (`Tags` table) is ready to support tags that may derive from expansions.

### 5. Search (`search`)

*   **Initial Strategy:**
    1.  The user prompt will be processed by the `DocumentProcessor` (same pipeline as documents during the `learn` phase).
    2.  For each tag in the prompt, the `DatabaseManager` will be queried to get documents containing that tag and their corresponding TF-IDF scores.
    3.  TF-IDF scores will be aggregated for each document.
    4.  Penalties will be applied for excluded keywords.
    5.  Results will be ordered by score.
*   **Flexibility:** Search logic will be orchestrated (e.g., in `tag_engine_logic.py` or a `SearchOrchestrator`) using services from `DatabaseManager` and `ScoringEngine`.

## Immediate Next Steps (Contributor Guide)

1.  **Complete `DatabaseManager` CRUD Methods (CREATE):**
    *   **Done:** `add_document(original_filename: str, doc_length: int) -> Optional[int]`
    *   **Done:** `get_or_create_tag(tag: str) -> Optional[int]` (implements get-or-create pattern).
    *   **To Do:** `link_document_tag(doc_id: int, tag_id: int, tf_idf_score: Optional[float] = None) -> bool`.
2.  **Implement Basic CRUD Methods (READ) in `DatabaseManager`:**
    *   `get_tag_id_by_text(tag_text: str) -> Optional[int]` (Note: `get_or_create_tag` can serve part of this, but a dedicated GET might be cleaner for some use cases).
    *   `get_document_id_by_stored_filename(stored_filename: str) -> Optional[int]`
    *   (Consider other GET methods that might be needed, e.g., `get_document_by_id`, `get_tag_by_id`, `get_tags_for_document`, `get_documents_for_tag`).
3.  **Implement Basic CRUD Methods (DELETE) in `DatabaseManager`:**
    *   `remove_document(doc_id: int) -> bool` (or by `stored_filename`). This will also remove associated tags via `ON DELETE CASCADE`.
    *   (Consider `unlink_document_tag(doc_id: int, tag_id: int) -> bool` or `remove_tag_globally(tag_id: int) -> bool`).
4.  **Implement Support Methods for TF-IDF in `DatabaseManager`:**
    *   `get_total_documents_count() -> int`
    *   `get_doc_count_for_tag(tag_id: int) -> int`
    *   `get_doc_length(doc_id: int) -> Optional[int]`
    *   `update_tf_idf_score(doc_id: int, tag_id: int, score: float) -> bool` (This is an UPDATE method).
5.  **Develop `DocumentProcessor` (Custom NLP Logic):**
    *   Functions for tokenizing, cleaning punctuation, converting to lowercase, removing stop-words (user-defined), lemmatizing (according to custom rules).
6.  **Develop `TagExtractor`:**
    *   Takes the output of `DocumentProcessor` and calculates term frequencies (TF) for the document.

## Areas to Be Defined/Developed Later

*   Complete logic for `learn()` and `search()` using the new components.
*   Implementation of the `ScoringEngine` (initially with TF-IDF).
*   Strategies for tag expansion.
*   Completion of modules in `access-app/io/` and `access-app/utils/`.
*   Implementation of unit and integration tests in `tests/`.
*   Setup of pre-commit hooks and GitHub Actions CI.
*   Handling of very large documents (streaming/chunking if necessary).
*   Handling of different file types (PDF, DOCX, etc.).

## Contributing

*   Ensure you have the development tools installed (see `pyproject.toml` `[project.optional-dependencies].dev` section).
*   Follow the code style enforced by `black` and `flake8` (will be automated with pre-commit).
*   Write tests for new features.
*   Keep this document (`dev_book.md`) updated with new decisions made.
