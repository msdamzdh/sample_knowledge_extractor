LLM Knowledge Extractor
This is a small prototype application for the "LLM Knowledge Extractor" assignment. It consists of a simple web UI and a FastAPI backend that analyzes unstructured text to produce a summary and structured metadata.

Setup and Run Instructions
Prerequisites: Ensure you have Python 3.8+ installed.

Install Dependencies:
First, install the necessary Python packages. I recommend using a virtual environment.

pip install fastapi uvicorn "uvicorn[standard]"

Run the Backend:
Open your terminal, navigate to the directory containing main.py, and run the following command:

uvicorn main:app --reload

This will start the FastAPI server on http://127.0.0.1:8000. The --reload flag is for development, as it automatically reloads the server on code changes.

Open the Frontend:
Simply open the index.html file in your web browser. It will automatically connect to the running FastAPI backend.

Design Choices
FastAPI for the Backend: I chose FastAPI because it is a modern, high-performance, and developer-friendly framework for building APIs in Python. Its automatic Pydantic data validation and interactive API documentation (Swagger UI) make it ideal for quickly building robust endpoints for a prototype.

Single-File HTML/JS/CSS Frontend: The entire user interface is contained within a single index.html file. This approach simplifies the setup for a small prototype, as it requires no build process. I used Tailwind CSS via a CDN to create a clean, responsive, and aesthetically pleasing UI with minimal effort.

Mock LLM: Instead of integrating with a real LLM API like OpenAI or Claude, I implemented a simple MockLLM class. This choice was made to meet the timebox constraint and eliminate the need for API keys or external dependencies, ensuring the prototype is fully functional out-of-the-box.

In-Memory Database: The analyses_db is a simple Python list that persists data for the duration of the server's uptime. This was a pragmatic choice to avoid the setup time required for a real database like SQLite or Postgres, which would have involved separate database files, connection management, and ORM configuration.

Trade-offs
Due to the timebox, I made the following trade-offs:

Mocked Services: The LLM and database are mocked or in-memory. In a production environment, these would be replaced with real, persistent solutions (e.g., an LLM provider and a SQL database).

Naive Keyword Extraction: The keyword extraction logic is a simple word frequency counter. A more robust solution would use a library like nltk or spaCy for proper part-of-speech tagging and lemmatization.

Limited Error Handling: While basic error handling is in place for empty input and LLM failures, a more complete system would include more granular error codes, logging, and user-friendly error messages for various failure scenarios.

No Tests: The project does not include tests (unit or integration). For a production system, a test suite would be essential to ensure reliability and maintainability.