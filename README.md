# ACCESS - Automated Cataloging and Classification Engine for Storage and Search

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
<!-- Add other badges as the project evolves, e.g., build status, code coverage, PyPI version -->

> [!IMPORTANT]
> The project is still uncomplete and need some works before final release

ACCESS (Automated Cataloging and Classification Engine for Storage and Search) is a Python-based application designed to provide a powerful and flexible solution for cataloging, classifying, and searching documents. This project aims to streamline document management through intelligent tagging and efficient retrieval mechanisms.

## Project Goal

The primary goal of ACCESS is to offer a robust tool that can:
1.  **Automate Document Organization:** Automatically process and categorize documents based on their content.
2.  **Enable Efficient Search:** Allow users to quickly find relevant documents using a tag-based search system.
3.  **Ensure Scalability:** Handle a growing number of documents, from small personal collections to larger archives.
4.  **Maintain High Code Quality:** Adhere to professional coding standards, including linting, formatting, static typing, and testing.
5.  **Be Modular and Extensible:** Design components that can be easily evolved or replaced.

## Features (Current & Planned)

*   **SQLite-based Data Persistence:** Secure and efficient storage of document metadata and tags using SQLite.
*   **Automatic Tagging (Work in Progress):**
    *   Custom NLP pipeline for document processing (tokenization, cleaning, lemmatization).
    *   TF-IDF based scoring for tag relevance.
*   **Tag-Based Search (Planned):** Powerful search 여성anisms based on document tags and their scores.
*   **Command-Line Interface (CLI) (Planned):** Initial interface for interacting with the system.
*   **Unique Document Storage:** Internal mechanism to ensure uniquely stored filenames using UUIDs.
*   **Robust Database Management:** Dedicated `DatabaseManager` class to handle all database interactions, schema creation, and CRUD operations.

## Architectural Overview

ACCESS is built with a modular architecture to promote maintainability and future enhancements. Key components include:

*   **`access-app/core`:** Contains the core business logic.
    *   `database_manager.py`: Manages all interactions with the SQLite database, including schema definition, document and tag storage, and retrieval.
    *   *(Planned)* `DocumentProcessor`: Handles the NLP tasks like tokenization, stop-word removal, and lemmatization.
    *   *(Planned)* `TagExtractor`: Calculates term frequencies from processed documents.
    *   *(Planned)* `ScoringEngine`: Implements TF-IDF and potentially other scoring algorithms.
*   **`access-app/io`:** (To be defined) Intended for input/output interactions, such as file handling.
*   **`access-app/utils`:** (To be defined) For utility functions and helper classes.
*   **`access-app/cli.py`:** (To be defined) The main entry point for the command-line interface.
*   **`data/learned/access_main.db`:** The SQLite database file where all learned information and metadata are stored.

### Database Schema

The core data is organized into three main tables:

1.  **`Documents`**: Stores metadata about each document.
    *   `doc_id` (INTEGER, PK, Autoincrement)
    *   `original_filename` (TEXT, NOT NULL)
    *   `stored_filename` (TEXT, NOT NULL, UNIQUE) - Internally generated unique filename.
    *   `import_date` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
    *   `doc_length` (INTEGER) - e.g., number of words or characters.
2.  **`Tags`**: Stores unique tags identified in the documents.
    *   `tag_id` (INTEGER, PK, Autoincrement)
    *   `tag_text` (TEXT, NOT NULL, UNIQUE)
3.  **`DocumentTags`**: A linking table associating documents with tags and their relevance scores.
    *   `doc_id` (INTEGER, NOT NULL, FK to Documents)
    *   `tag_id` (INTEGER, NOT NULL, FK to Tags)
    *   `tf_idf_score` (REAL) - The TF-IDF score for the tag in relation to the document.
    *   PRIMARY KEY (`doc_id`, `tag_id`)
    *   Foreign keys have `ON DELETE CASCADE` to maintain data integrity.

Appropriate indexes are created on these tables to ensure efficient querying.

## Getting Started (Development)

Currently, ACCESS is in active development. To set up a development environment:

1.  **Prerequisites:**
    *   Python 3.8 or higher.
2.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd access_v3 # Or your repository's root directory name
    ```
3.  **Set up a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
4.  **Install Dependencies:**
    The project uses `pyproject.toml` for project metadata. Core dependencies are minimal (built-in `sqlite3`). Development dependencies can be installed via:
    ```bash
    pip install -e .[dev]
    ```
    This installs the package in editable mode (`-e .`) and the development tools specified in `[project.optional-dependencies].dev` of `pyproject.toml` (like `black`, `flake8`, `mypy`, `pytest`).

5.  **Initialize the Database (Automatic):**
    Running any part of the application that instantiates the `DatabaseManager` (e.g., future CLI commands or scripts) will automatically create the `data/learned/access_main.db` file and its schema if they don't exist.

## Development Guidelines & Contributing

We welcome contributions to ACCESS! Please follow these guidelines:

*   **Code Style:**
    *   The project uses `black` for code formatting, `isort` for import sorting, and `flake8` for linting.
    *   (Planned) Pre-commit hooks will be set up to automate these checks.
*   **Type Hinting:**
    *   `mypy` is used for static type checking. Please include type hints in your code.
*   **Branching:**
    *   Create a new branch for each feature or bug fix (e.g., `feature/new-search-algorithm` or `fix/database-query-error`).
*   **Commits:**
    *   Write clear and concise commit messages.
*   **Testing (Planned):**
    *   `pytest` will be used for unit and integration tests. Please write tests for new functionalities.
*   **Documentation:**
    *   Keep inline comments and docstrings up-to-date.
    *   Update the `docs/dev_book.md` file with significant architectural decisions or changes to the development plan.
*   **Pull Requests:**
    *   Ensure your code passes all linting and type checks before submitting a pull request.
    *   (Planned) GitHub Actions will be set up for CI to automate checks on PRs.

Refer to the `docs/dev_book.md` for a more detailed overview of the current development status, architectural choices, and a roadmap for immediate next steps.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Future Directions

*   Implementation of the full `learn` and `search` commands.
*   Development of the `DocumentProcessor`, `TagExtractor`, and `ScoringEngine` components.
*   Strategies for tag expansion and synonyms.
*   Support for various file types (PDF, DOCX, etc.).
*   Potential GUI development.
*   Enhanced scalability for very large document sets.
