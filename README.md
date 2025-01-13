# Worm Programming Language Tokenizer

A web-based tokenizer/lexical analyzer for the Worm programming language built with Streamlit.

## Features

- Interactive code editor with syntax highlighting
- File upload support for `.worm` files
- Real-time tokenization of code
- Token visualization using tables
- Dark theme code editor

## Setup

This project uses `pyproject.toml` for dependency management. You can use any of these package managers:

- **uv** (Recommended):

  ```bash
  uv venv
  uv sync
  ```

- **pip**:

  ```bash
  python -m venv venv
  pip install -r requirements.txt
  ```

- **poetry**:

  ```bash
  poetry install
  ```

## Running the Application

First, activate your virtual environment:

- **On Windows**:

  ```bash
  .\venv\Scripts\activate
  ```

- **On macOS/Linux**:

  ```bash
  source venv/bin/activate
  ```

Then run the application:

```bash
streamlit run main.py
```

## Development

The application is built with:

- Streamlit for the web interface
- streamlit-code-editor for the code editing component
- Pandas for data manipulation and display

## Project Structure

```
worm-pl/
├── main.py          # Main application file
├── lexer.py         # Main lexer logic
├── pyproject.toml   # Project dependencies and metadata
└── README.md        # This file
```
