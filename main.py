import streamlit as st
from streamlit_ace import st_ace
import pandas as pd

from lexer import Lexer

# Page config
st.set_page_config(page_title="Worm Code Tokenizer", page_icon="🪱", layout="wide")

# Header
st.title("*Worm* Code Tokenizer / Lexical Analyzer")

# Create two columns
left_col, right_col = st.columns(2, border=False)

with left_col:
    st.subheader("Code Input")
    # Store uploaded content in session state to persist between rerenders
    if "code_content" not in st.session_state:
        st.session_state.code_content = 'print("Hello, Worm!");'

    with st.expander("Presets", expanded=True):
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload a worm code file",
            type=["worm"],
            accept_multiple_files=False,
            help="Only .worm files are allowed",
        )
        
        if uploaded_file is not None:
            st.session_state.code_content = uploaded_file.getvalue().decode("utf-8")

        
        preset_buttons_columns = st.columns(6)
        with preset_buttons_columns[0]:
            if st.button("Hello"):
                st.session_state.code_content = 'print("Hello, Worm!");'
        with preset_buttons_columns[1]:
            if st.button("Math"):
                st.session_state.code_content = 'result = 2 + 3 * 4;'
        with preset_buttons_columns[2]:
            if st.button("Vars"):
                st.session_state.code_content = 'let x = 42;\nlet y = x + 8;'
        with preset_buttons_columns[3]:
            if st.button("Loop"):
                st.session_state.code_content = 'for i in range(5) {\n    print(i);\n}'
        with preset_buttons_columns[4]:
            if st.button("Func"):
                st.session_state.code_content = 'def add(a, b) {\n    return a + b;\n}'
        with preset_buttons_columns[5]:
            if st.button("Clear"):
                st.session_state.code_content = ''

    # Text area for code input
    code_input = st_ace(
        value=st.session_state.code_content,
        min_lines=10,
        language="python",
        theme="dracula",
        show_gutter=True,
        auto_update=False,
        font_size=20,
    )

    # Tokenize handler
    if code_input:
        # Create lexer instance and tokenize
        lexer = Lexer(code_input, include_comments=True)
        tokens = lexer.tokenize()

        # Convert tokens to DataFrame
        df = pd.DataFrame(
            [
                {
                    "Line": token.line,
                    "Column": token.column,
                    "Type": token.type,
                    "Value": token.value,
                }
                for token in tokens
            ]
        )

        # Display results in right column
        with right_col:
            st.subheader("Tokenization Results")
            if not df.empty:
                st.dataframe(
                    df,
                    column_config={
                        "Line": st.column_config.NumberColumn("Line #"),
                        "Column": st.column_config.NumberColumn("Col #"),
                        "Type": st.column_config.TextColumn("Token", width="medium"),
                        "Value": st.column_config.TextColumn("Lexeme", width="medium"),
                    },
                    hide_index=True,
                    use_container_width=True,
                )
            else:
                st.info("No tokens found in the input code.")

    else:
        with right_col:
            st.subheader("Tokenization Results")
            st.error("Please enter some code or upload a file first.")
