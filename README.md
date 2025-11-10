# Financial Planning & Python AI Tutor

A comprehensive financial planning application with an integrated Python AI Tutor to help developers learn and troubleshoot Python issues.

## Features

### 💸 Budget & Investment Planner
- Monthly budget tracking with income and expenses
- Investment portfolio management (stocks, bonds, crypto, real estate, fixed deposits)
- Real-time market data integration via Alpha Vantage API
- Net worth projections over customizable time periods
- Interactive charts and visualizations
- Multi-LLM AI financial suggestions (Gemini, DeepSeek)
- Botpress chatbot integration for financial advice

### 🐍 Python AI Tutor
An intelligent tutoring system that helps developers with:
- **Virtual environment issues** - Setup, activation, and troubleshooting
- **Import errors** - Module not found, installation issues
- **Path problems** - File paths, directory navigation, Windows/Mac/Linux compatibility
- **General Python questions** - Concepts, best practices, debugging

The tutor is available in two modes:
1. **Streamlit Web Interface** - Interactive chat with AI-powered responses
2. **Command Line Interface** - Quick help without requiring API keys

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/adnbal/financialplanning.git
cd financialplanning
```

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate the virtual environment:
   - **Windows**: `.venv\Scripts\activate`
   - **Mac/Linux**: `source .venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Configure API keys (for Streamlit apps):
Create a `.streamlit/secrets.toml` file with:
```toml
[gemini]
api_key = "your-gemini-api-key"

[openrouter]
api_key = "your-openrouter-api-key"

[alpha_vantage]
api_key = "your-alpha-vantage-api-key"

[botpress]
chat_api_id = "your-botpress-bot-id"
token = "your-botpress-token"
```

## Usage

### Budget & Investment Planner

Run the Streamlit app:
```bash
streamlit run budget_invest_app.py
```

### Python AI Tutor - Web Interface

Run the tutor Streamlit app:
```bash
streamlit run ai_tutor.py
```

Features:
- Interactive chat interface
- AI-powered responses (Gemini or DeepSeek)
- Quick access to common topics
- Code examples and best practices
- Chat history

### Python AI Tutor - CLI

For quick help without API keys:

```bash
# Ask a specific question
python python_tutor_cli.py "Why am I getting a path error with .venv?"

# Interactive mode
python python_tutor_cli.py
```

Example questions:
- "The system cannot find the path specified (.venv)"
- "How do I create a virtual environment?"
- "Why can't Python find my module?"
- "How do I fix import errors?"

## Common Issues & Solutions

### Virtual Environment Path Error

**Problem**: `The system cannot find the path specified` when accessing `.venv`

**Solutions**:
1. Check if `.venv` directory exists: `dir` (Windows) or `ls -la` (Mac/Linux)
2. Create a new virtual environment: `python -m venv .venv`
3. Use quotes for paths with spaces: `cd "path with spaces"`
4. Activate: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux)

**Prevention**:
- Avoid spaces in directory names
- Use underscores: `Demo_1_before_Delete` instead of `Demo 1 - before Delte`
- Keep virtual environments in project root

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'package'`

**Solutions**:
1. Install the package: `pip install package-name`
2. Verify virtual environment is activated (look for `(.venv)` in prompt)
3. Check installation: `pip list`
4. Update pip: `python -m pip install --upgrade pip`

## Project Structure

```
financialplanning/
├── budget_invest_app.py      # Main financial planning Streamlit app
├── ai_tutor.py               # Python AI Tutor web interface
├── python_tutor_cli.py       # Python AI Tutor CLI
├── botpress_client.py        # Botpress integration client
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## API Services

### Required APIs
- **Google Gemini** - AI responses for financial advice and tutoring
- **OpenRouter (DeepSeek)** - Alternative AI model for diverse responses
- **Alpha Vantage** - Real-time stock market data
- **Botpress** - Conversational AI chatbot

### Getting API Keys
- **Gemini**: [Google AI Studio](https://makersuite.google.com/app/apikey)
- **OpenRouter**: [OpenRouter Dashboard](https://openrouter.ai/keys)
- **Alpha Vantage**: [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
- **Botpress**: [Botpress Cloud](https://botpress.com/)

## Development

### Running Tests
```bash
# Test CLI tutor
python python_tutor_cli.py "test question"

# Test Streamlit apps (requires API keys)
streamlit run ai_tutor.py
streamlit run budget_invest_app.py
```

### Contributing
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## Best Practices

### Virtual Environments
- Always use virtual environments for Python projects
- Activate before installing packages
- Use `requirements.txt` to track dependencies
- Add `.venv` to `.gitignore`

### Path Handling
- Use `pathlib.Path` for cross-platform compatibility
- Use forward slashes or raw strings
- Avoid spaces in directory names

### Dependencies
- Keep `requirements.txt` updated: `pip freeze > requirements.txt`
- Use specific versions for reproducibility
- Update regularly for security patches

## Troubleshooting

### Streamlit Not Starting
```bash
# Reinstall streamlit
pip install --upgrade streamlit

# Check installation
streamlit --version

# Clear cache
streamlit cache clear
```

### API Key Errors
- Verify `.streamlit/secrets.toml` exists and has correct format
- Check API keys are valid and not expired
- Ensure proper indentation in TOML file

### Import Errors
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version compatibility

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Use the Python AI Tutor for Python-related questions
- Check existing documentation and examples

---

**Happy coding and planning! 💸🐍**
