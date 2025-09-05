# LLM Knowledge Extractor

A web application with a FastAPI backend that analyzes unstructured text to produce a summary and structured metadata using a Large Language Model (LLM). This project is designed as a lightweight, functional prototype to demonstrate the extraction of key information from articles, blog posts, and other text sources.

## ✨ Key Features

- **Text Analysis**: Enter any unstructured text to get a summary, sentiment analysis, and key topics.
- **LLM Integration**: Seamlessly connect to a mock LLM, OpenAI's GPT, or a local Ollama instance.
- **Structured Output**: The backend uses LangChain and Pydantic to ensure the analysis is returned in a consistent, structured JSON format.
- **In-Memory Storage**: Analyzed data is stored in memory for quick retrieval and searching.
- **Responsive UI**: A simple, single-file HTML frontend built with Tailwind CSS for a clean and mobile-friendly user experience.

## 🚀 Getting Started

Follow these steps to set up and run the application on your local machine.

### Prerequisites

Ensure you have Python 3.8+ installed. We highly recommend using a virtual environment to manage dependencies.

### 1. Install Dependencies

Use the `requirements.txt` file to install all necessary Python packages. make sure you installe them in virtual environment.

```bash
pip install -r requirements.txt
```

### 2. Configure Your LLM Provider

The application supports multiple LLM providers. To use OpenAI or Ollama, you'll need to configure your environment.

#### OpenAI

If you plan to use OpenAI's GPT models, you must provide your API key. Create or open the .env file and add your key:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

Replace your_openai_api_key_here with your actual key.

#### Ollama

For a local LLM setup, ensure you have Ollama installed and a model like gemma3:1b downloaded.

```bash
ollama pull gemma3:1b
```

### 3. Run the Backend Server

Navigate to the project's root directory in your terminal and start the program.

```Python
python main.py
```

### 4. open browser

open your browser at below address

```text
127.0.0.1:8000
```

## Project Structure

- main.py: The core FastAPI application that defines the API endpoints and handles requests.
- llm_service.py: Contains the logic for interacting with different LLM providers (Mock, OpenAI, Ollama) via the LangChain library.
- index.html: The single-file frontend containing all HTML, CSS, and JavaScript.
- requirements.txt: A list of all Python dependencies required for the project.
- .env: A file to store your API keys securely.

## Trade-offs & Future Improvements

This project is a prototype with a few intentional trade-offs for rapid development:

- In-Memory Database: For a production environment, this should be replaced with a persistent database like SQLite, PostgreSQL, or MongoDB.
- LLM Keyword Extraction: The current keyword extraction is a simple frequency count. A more advanced solution could use natural language processing libraries for better results.
- Scalability: The current architecture is not designed for high-concurrency use. A more robust solution would involve asynchronous task queues and better resource management.
