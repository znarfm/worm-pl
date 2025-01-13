import streamlit as st
from code_editor import code_editor
import pandas as pd

# Page config
st.set_page_config(page_title="Worm Code Tokenizer", page_icon="🪱", layout="wide")

# Header
st.title("*Worm* Code Tokenizer / Lexical Analyzer")

# Create two columns
left_col, right_col = st.columns(2, border=True)

with left_col:
    st.subheader("Code Input")
    # Store uploaded content in session state to persist between rerenders
    if "code_content" not in st.session_state:
        st.session_state.code_content = 'print("Hello, World!")'

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload a worm code file",
        type=["worm"],
        accept_multiple_files=False,
        help="Only .worm files are allowed",
    )

    if uploaded_file is not None:
        st.session_state.code_content = uploaded_file.getvalue().decode("utf-8")

    custom_btns = [
        {
            "name": "Copy",
            "feather": "Copy",
            "commands": ["copyAll"],
            "style": {"top": "0.46rem", "right": "0.4rem"},
        },
        {
            "name": "Tokenize",
            "hasText": True,
            "feather": "Check",
            "alwaysOn": True,
            "commands": ["submit"],
            "style": {"bottom": "0.46rem", "right": "0.4rem"},
        },
    ]
    # Text area for code input - now using session state
    response_dict = code_editor(
        code=st.session_state.code_content,
        height=[10, 20],
        lang="python",
        theme="dark",
        focus=True,
        buttons=custom_btns,
    )

    # Tokenize handler
    if response_dict.get("text", not None):
        st.write(response_dict)
        # Simple tokenization (you can enhance this based on your needs)
        tokens = response_dict.get("text").split()

        # Create a dataframe with tokens
        df = pd.DataFrame(
            {
                "Token": tokens,
                "Type": [
                    "keyword"
                    if token
                    in [
                        "def",
                        "class",
                        "import",
                        "for",
                        "while",
                        "if",
                        "else",
                        "return",
                    ]
                    else "identifier"
                    for token in tokens
                ],
            }
        )

        # Display results in right column
        with right_col:
            st.subheader("Tokenization Results")
            st.dataframe(df)
    else:
        with right_col:
            st.subheader("Tokenization Results")
            st.error("Please enter some code or upload a file first.")
