import streamlit as st
import google.generativeai as genai
import requests
from typing import List


class PythonAITutor:
    """
    AI-powered Python tutor that helps users understand Python concepts,
    troubleshoot errors, and learn best practices.
    """

    def __init__(self, gemini_api_key: str, openrouter_api_key: str):
        """Initialize the AI tutor with API keys for different AI services."""
        self.gemini_api_key = gemini_api_key
        self.openrouter_api_key = openrouter_api_key
        genai.configure(api_key=gemini_api_key)

    def identify_error_type(self, user_input: str) -> str:
        """Identify the type of Python issue from user input."""
        user_input_lower = user_input.lower()

        if "cannot find the path" in user_input_lower or "path specified" in user_input_lower:
            return "path_error"
        elif ".venv" in user_input_lower or "virtual environment" in user_input_lower or "virtualenv" in user_input_lower:
            return "venv_error"
        elif "import" in user_input_lower and "error" in user_input_lower:
            return "import_error"
        elif "syntax" in user_input_lower and "error" in user_input_lower:
            return "syntax_error"
        elif "indentation" in user_input_lower:
            return "indentation_error"
        elif "why" in user_input_lower and len(user_input.split()) <= 3:
            return "general_question"
        else:
            return "general"

    def get_context_specific_prompt(self, user_input: str, error_type: str) -> str:
        """Generate a context-specific prompt based on the error type."""
        base_context = """You are a helpful Python AI tutor. Your goal is to:
1. Explain Python concepts clearly and concisely
2. Help troubleshoot errors with actionable solutions
3. Provide best practices and recommendations
4. Use simple language suitable for all skill levels
"""

        if error_type == "path_error":
            return f"""{base_context}

The user is experiencing a file path error. Here's their issue:
{user_input}

Please:
1. Explain why this path error occurs
2. Identify potential causes (spaces in path, incorrect directory, etc.)
3. Provide step-by-step solutions to fix the issue
4. Suggest best practices for handling paths in Python
5. Include example commands if relevant

Be especially helpful with Windows path issues, backslashes, and directory navigation."""

        elif error_type == "venv_error":
            return f"""{base_context}

The user is having issues with Python virtual environments. Here's their issue:
{user_input}

Please:
1. Explain what virtual environments are and why they're important
2. Diagnose the specific issue they're facing
3. Provide clear steps to create/activate/fix their virtual environment
4. Include platform-specific instructions (Windows/Mac/Linux) as relevant
5. Suggest troubleshooting steps if the venv doesn't exist or is corrupted

Include actual commands they can run."""

        elif error_type == "import_error":
            return f"""{base_context}

The user is experiencing an import error. Here's their issue:
{user_input}

Please:
1. Explain why the import is failing
2. Check if it's a missing package, incorrect name, or path issue
3. Provide installation commands (pip install)
4. Explain the difference between package names and import names if relevant
5. Suggest how to verify the installation"""

        elif error_type == "general_question":
            return f"""{base_context}

The user has a general question or wants an explanation. Here's what they asked:
{user_input}

Please:
1. Provide a clear, comprehensive explanation
2. Include relevant context and background
3. Give examples if applicable
4. Suggest related concepts they might want to learn
5. Keep it educational and encouraging"""

        else:
            return f"""{base_context}

User question:
{user_input}

Please provide a helpful, clear, and educational response."""

    def get_response_with_gemini(self, user_input: str) -> str:
        """Get AI response using Google Gemini."""
        try:
            error_type = self.identify_error_type(user_input)
            prompt = self.get_context_specific_prompt(user_input, error_type)

            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error getting Gemini response: {e}"

    def get_response_with_deepseek(self, user_input: str) -> str:
        """Get AI response using DeepSeek via OpenRouter."""
        try:
            error_type = self.identify_error_type(user_input)
            prompt = self.get_context_specific_prompt(user_input, error_type)

            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "deepseek/deepseek-r1:free",
                "messages": [{"role": "user", "content": prompt}]
            }
            res = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )
            res.raise_for_status()
            return res.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error getting DeepSeek response: {e}"

    def get_common_solutions(self, error_type: str) -> List[str]:
        """Provide quick common solutions for known error types."""
        solutions = {
            "path_error": [
                "Check if the directory exists using: os.path.exists(path)",
                "Use raw strings for Windows paths: r'C:\\path\\to\\folder'",
                "Use os.path.join() for cross-platform path handling",
                "Remove spaces from directory names or use quotes",
                "Verify you're in the correct working directory: os.getcwd()"
            ],
            "venv_error": [
                "Create a new virtual environment: python -m venv .venv",
                "Activate on Windows: .venv\\Scripts\\activate",
                "Activate on Mac/Linux: source .venv/bin/activate",
                "Check if venv module is installed: python -m venv --help",
                "Try recreating the venv if it's corrupted"
            ],
            "import_error": [
                "Install the package: pip install package-name",
                "Check if you're in the right virtual environment",
                "Verify the package name: pip search package-name",
                "Update pip: python -m pip install --upgrade pip",
                "Check Python path: import sys; print(sys.path)"
            ]
        }
        return solutions.get(error_type, [])


def run_tutor_app():
    """Main Streamlit app for the Python AI Tutor."""
    st.set_page_config(page_title="🐍 Python AI Tutor", page_icon="🐍", layout="wide")

    st.title("🐍 Python AI Tutor")
    st.markdown("""
    Welcome to your personal Python AI Tutor! I can help you with:
    - 🔍 Understanding Python errors and warnings
    - 💡 Learning Python concepts and best practices
    - 🛠️ Troubleshooting virtual environments and setup issues
    - 📚 Explaining code and providing examples
    """)

    # Check for API keys in secrets
    try:
        gemini_api_key = st.secrets["gemini"]["api_key"]
        openrouter_api_key = st.secrets["openrouter"]["api_key"]
    except Exception:
        st.error("⚠️ API keys not found in secrets. Please configure them to use the tutor.")
        st.stop()

    # Initialize tutor
    tutor = PythonAITutor(gemini_api_key, openrouter_api_key)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Common scenarios quick access
    st.sidebar.header("📋 Quick Help Topics")
    quick_topics = {
        "Virtual Environment Issues": "I'm getting an error: The system cannot find the path specified when trying to access .venv",
        "Import Errors": "Why am I getting 'ModuleNotFoundError' when importing a package?",
        "Path Problems": "How do I fix path errors in Windows with spaces in directory names?",
        "Getting Started": "How do I create and activate a Python virtual environment?",
        "Package Installation": "How do I install Python packages and manage dependencies?"
    }

    selected_topic = st.sidebar.selectbox("Choose a topic:", ["Custom Question"] + list(quick_topics.keys()))

    # User input
    if selected_topic != "Custom Question":
        user_input = quick_topics[selected_topic]
        st.info(f"Selected topic: {selected_topic}")
    else:
        user_input = st.chat_input("Ask me anything about Python!")

    # Process user input
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Identify error type and show quick solutions
        error_type = tutor.identify_error_type(user_input)
        quick_solutions = tutor.get_common_solutions(error_type)

        if quick_solutions:
            with st.expander("💡 Quick Solutions", expanded=True):
                for solution in quick_solutions:
                    st.markdown(f"- {solution}")

        # AI selection
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🤖 Ask Gemini", use_container_width=True):
                with st.spinner("Gemini is thinking..."):
                    response = tutor.get_response_with_gemini(user_input)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    with st.chat_message("assistant"):
                        st.markdown(response)

        with col2:
            if st.button("🧠 Ask DeepSeek", use_container_width=True):
                with st.spinner("DeepSeek is thinking..."):
                    response = tutor.get_response_with_deepseek(user_input)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    with st.chat_message("assistant"):
                        st.markdown(response)

    # Add clear chat button
    if st.sidebar.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    # Additional resources
    st.sidebar.markdown("---")
    st.sidebar.header("📚 Resources")
    st.sidebar.markdown("""
    - [Python Official Docs](https://docs.python.org/)
    - [Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)
    - [pip Documentation](https://pip.pypa.io/)
    """)


if __name__ == "__main__":
    run_tutor_app()
