# ACCESS v3 - Project Status and Development Guidelines

This document describes the current status of the ACCESS v3 project, the architectural decisions made, and directions for future development. It is intended as a guide for collaborators who wish to contribute to the project.

## Project Goal

ACCESS (Automated Cataloging and Classification Engine for Storage and Search) aims to become a powerful and flexible tool for cataloging, classifying, and searching documents. Version 3 focuses on:

1.  **Professional Code Quality:** Adoption of coding standards, linting, formatting, and static typing.
2.  **Scalability:** Ability to handle a large number of documents, from very small to very large (thousands or hundreds of thousands).
3.  **Accuracy:** Continuous improvement of tagging and search algorithms.
4.  **Modularity:** Design that allows easy replacement or evolution of key components.

## Current Repository Structure (Summary)

```
access_v3/
├── access-app/                # Main application source code
│   ├── core/                  # Business logic (database_manager.py here)
│   │   └── database_manager.py
│   ├── io/                    # I/O interaction (to be defined)
│   ├── utils/                 # Utilities (to be defined)
│   ├── cli.py                 # Entry point and CLI logic (to be defined)
│   └── __init__.py
├── data/                      # Persistent data
│   └── learned/               # Learned data (contains access_main.db)
│       └── access_main.db     # SQLite database file (currently empty or with base schema)
├── tests/                     # (Planned, to be created)
├── .github/                   # (Planned, for CI with GitHub Actions)
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml             # Project configuration and dependencies
└── repo-to-txt.sh             # Utility script to generate project tree
```

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
        *   `__init__` constructor that sets `self.db_path` and ensures the database directory exists.
        *   Planned call to `_create_tables_if_not_exists()` in the constructor.
        *   The `_create_tables_if_not_exists()` method has been defined and will contain `CREATE TABLE IF NOT EXISTS` queries for `Documents`, `Tags`, `DocumentTags`, and corresponding `CREATE INDEX IF NOT EXISTS`.
        *   Planned `_get_connection()` helper method to centralize connection logic and enable `PRAGMA foreign_keys = ON;`.
*   **SQLite Database Schema (Proposed):**
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

1.  **Complete `DatabaseManager._create_table()`:**
    *   Implement `CREATE TABLE IF NOT EXISTS` SQL queries for `Documents`, `Tags`, `DocumentTags`.
    *   Implement `CREATE INDEX IF NOT EXISTS` queries as discussed.
    *   Ensure correct use of the context manager `with self._get_connection() as conn:`.
    *   Test initialization (creation of the `.db` file and schema).
2.  **Implement Basic CRUD Methods in `DatabaseManager`:**
    *   `add_document(...)`
    *   `add_tag_if_not_exists(...)` (get-or-create)
    *   `link_document_tag(...)`
    *   `get_tag_id(...)`
    *   `get_document_id_by_stored_filename(...)`
    *   `remove_document_and_its_tags(...)`
3.  **Implement Support Methods for TF-IDF in `DatabaseManager`:**
    *   `get_total_documents_count()`
    *   `get_doc_count_for_tag(tag_id)`
    *   `get_doc_length(doc_id)`
4.  **Develop `DocumentProcessor` (Custom NLP Logic):**
    *   Functions for tokenizing, cleaning punctuation, converting to lowercase, removing stop-words (user-defined), lemmatizing (according to custom rules).
5.  **Develop `TagExtractor`:**
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
*   Keep this document updated with new decisions made.
