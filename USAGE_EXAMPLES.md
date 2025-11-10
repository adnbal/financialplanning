# Python AI Tutor - Usage Examples

This document provides practical examples of using the Python AI Tutor.

## CLI Mode Examples

### Example 1: Virtual Environment Path Error (User's Issue)

**Question:**
```bash
python python_tutor_cli.py "The system cannot find the path specified .venv"
```

**Response:**
```
📖 Virtual Environment Path Error

This error typically occurs when:
1. The virtual environment (.venv) directory doesn't exist at the specified path
2. The path contains spaces or special characters that aren't properly escaped
3. You're in the wrong directory
4. The virtual environment was deleted or moved

✅ SOLUTIONS:

1. Check if the .venv directory exists:
   - On Windows: dir /a
   - On Mac/Linux: ls -la

2. Verify you're in the correct directory:
   - cd to your project folder first

3. Create a new virtual environment:
   - python -m venv .venv
   - Or: python3 -m venv .venv

4. If path has spaces, use quotes:
   - cd "E:\Apps\SU\Demo 1 - before Delte"

5. Activate the virtual environment:
   - Windows: .venv\Scripts\activate
   - Mac/Linux: source .venv/bin/activate
```

### Example 2: Import Error

**Question:**
```bash
python python_tutor_cli.py "ModuleNotFoundError: No module named 'requests'"
```

**Response:**
```
📖 Import Error / Module Not Found

This error means Python cannot find the module you're trying to import.
Common causes:
1. Package not installed
2. Wrong virtual environment activated
3. Typo in package/module name
4. Package name differs from import name

✅ SOLUTIONS:

1. Install the package:
   pip install package-name

2. Check if in correct venv:
   - which python (Mac/Linux)
   - where python (Windows)

3. Verify installation:
   pip list | grep package-name
```

### Example 3: Virtual Environment Setup

**Question:**
```bash
python python_tutor_cli.py "How do I create a virtual environment?"
```

**Response:**
```
📖 Virtual Environment Basics

A virtual environment is an isolated Python environment that allows you to:
- Install packages without affecting your system Python
- Manage different project dependencies separately
- Avoid version conflicts between projects

✅ SOLUTIONS:

1. Create virtual environment:
   python -m venv .venv

2. Activate it:
   - Windows: .venv\Scripts\activate
   - Mac/Linux: source .venv/bin/activate

3. Verify it's active:
   - Your prompt should show (.venv)

4. Install packages:
   pip install package-name
```

### Example 4: Interactive Mode

```bash
python python_tutor_cli.py
```

Then type your questions interactively:
```
You: why am I getting path errors?
[Tutor provides help]

You: how do I fix import errors?
[Tutor provides help]

You: quit
👋 Goodbye! Happy coding!
```

## Web Interface Examples

### Starting the Web Interface

```bash
streamlit run ai_tutor.py
```

This opens a web browser with:
- Interactive chat interface
- Message history
- Quick access topics
- AI-powered responses (requires API keys)

### Quick Help Topics

The sidebar provides quick access to common topics:
- Virtual Environment Issues
- Import Errors
- Path Problems
- Getting Started
- Package Installation

### Example Chat Session

**User:** "I'm getting an error: The system cannot find the path specified when trying to access .venv"

**Tutor (Quick Solutions):**
- Check if the .venv directory exists: `dir /a` (Windows)
- Create a new virtual environment: `python -m venv .venv`
- Use quotes for paths with spaces
- Activate: `.venv\Scripts\activate`

**User clicks "Ask Gemini"**

**AI Response:** [Detailed explanation with context-specific advice]

## Common Use Cases

### Use Case 1: First-Time Python Setup

```bash
# Question 1: Setup
python python_tutor_cli.py "How do I set up Python for a new project?"

# Question 2: Virtual Environment
python python_tutor_cli.py "How do I create a virtual environment?"

# Question 3: Install Packages
python python_tutor_cli.py "How do I install packages?"
```

### Use Case 2: Troubleshooting Existing Project

```bash
# Check your specific error
python python_tutor_cli.py "The system cannot find the path specified .venv"

# Follow the solutions provided
# Then verify
dir .venv  # Windows
python -m venv .venv  # Create if missing
.venv\Scripts\activate  # Activate
```

### Use Case 3: Learning Best Practices

Use the web interface to:
1. Navigate to "Quick Help Topics"
2. Select "Getting Started"
3. Read comprehensive guides
4. Ask follow-up questions in chat

## Tips for Best Results

### CLI Mode
- Be specific about your error message
- Include relevant context (error text, what you were trying to do)
- Use quotes for multi-word questions
- Try interactive mode for multiple questions

### Web Mode
- Use Quick Help Topics for common issues
- Click "Ask Gemini" or "Ask DeepSeek" for AI-powered responses
- Review Quick Solutions first for instant help
- Keep chat history for reference

### When to Use Each Mode

**Use CLI when:**
- You need quick help without setting up API keys
- Working in terminal already
- Want instant, pattern-based solutions
- Troubleshooting common errors

**Use Web Interface when:**
- Need detailed, context-aware AI explanations
- Want to explore multiple topics
- Prefer visual interface
- Need conversation history

## Real-World Scenarios

### Scenario: User on Windows with Path Error

**Problem:** User has directory "E:\Apps\SU\Demo 1 - before Delte\.venv" and gets path error

**Solution Steps:**
```bash
# 1. Check current directory
cd

# 2. Navigate with quotes
cd "E:\Apps\SU\Demo 1 - before Delte"

# 3. Check if .venv exists
dir /a

# 4. If missing, create it
python -m venv .venv

# 5. Activate
.venv\Scripts\activate

# 6. Verify activation (should see (.venv) in prompt)
where python
```

### Scenario: Module Not Found After Installation

**Problem:** Installed package but still getting ModuleNotFoundError

**Solution Steps:**
```bash
# 1. Check which Python is active
where python  # Windows
which python  # Mac/Linux

# 2. Verify virtual environment is activated
# Should see (.venv) in prompt

# 3. Check if package is installed
pip list | grep package-name

# 4. Install if missing
pip install package-name

# 5. Verify import
python -c "import package_name; print('Success!')"
```

## Integration with Your Workflow

### In Your Project README

Add this to help your team:
```markdown
## Troubleshooting

Having Python setup issues? Use our AI Tutor:

\`\`\`bash
# Quick help
python python_tutor_cli.py "your question"

# Interactive mode
python python_tutor_cli.py

# Web interface
streamlit run ai_tutor.py
\`\`\`
```

### As a Git Hook

You can add helpful reminders:
```bash
# .git/hooks/post-checkout
echo "💡 Need help with Python? Run: python python_tutor_cli.py"
```

## Next Steps

1. Try the CLI with your own questions
2. Explore the web interface
3. Bookmark this file for quick reference
4. Share with your team

---

**Need more help?** Run `python python_tutor_cli.py` and ask away!
