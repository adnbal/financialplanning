#!/usr/bin/env python3
"""
Python AI Tutor - Command Line Interface
A simple CLI tool to help with Python questions and troubleshooting.
"""

import sys
import os
from typing import Optional


class SimplePythonTutor:
    """
    A simple Python tutor that provides guidance without requiring API keys.
    Useful for basic troubleshooting and explanations.
    """
    
    def __init__(self):
        self.knowledge_base = self._build_knowledge_base()
    
    def _build_knowledge_base(self):
        """Build a knowledge base of common Python issues and solutions."""
        return {
            "venv_path_error": {
                "triggers": ["venv", "cannot find the path", "path specified", ".venv"],
                "title": "Virtual Environment Path Error",
                "explanation": """
This error typically occurs when:
1. The virtual environment (.venv) directory doesn't exist at the specified path
2. The path contains spaces or special characters that aren't properly escaped
3. You're in the wrong directory
4. The virtual environment was deleted or moved
""",
                "solutions": [
                    "Check if the .venv directory exists:\n  - On Windows: dir /a\n  - On Mac/Linux: ls -la",
                    "Verify you're in the correct directory:\n  - cd to your project folder first",
                    "Create a new virtual environment:\n  - python -m venv .venv\n  - Or: python3 -m venv .venv",
                    "If path has spaces, use quotes:\n  - cd \"E:\\Apps\\SU\\Demo 1 - before Delte\"",
                    "Activate the virtual environment:\n  - Windows: .venv\\Scripts\\activate\n  - Mac/Linux: source .venv/bin/activate",
                    "If directory name has typo (like 'Delte'), consider renaming:\n  - Remove spaces and fix typos for easier access"
                ],
                "prevention": [
                    "Avoid spaces in directory names",
                    "Use underscores instead: Demo_1_before_Delete",
                    "Keep virtual environments in project root",
                    "Add .venv to .gitignore to avoid version control issues"
                ]
            },
            "import_error": {
                "triggers": ["import", "modulenotfounderror", "no module named"],
                "title": "Import Error / Module Not Found",
                "explanation": """
This error means Python cannot find the module you're trying to import.
Common causes:
1. Package not installed
2. Wrong virtual environment activated
3. Typo in package/module name
4. Package name differs from import name
""",
                "solutions": [
                    "Install the package:\n  pip install package-name",
                    "Check if in correct venv:\n  - which python (Mac/Linux)\n  - where python (Windows)",
                    "Verify installation:\n  pip list | grep package-name",
                    "Update pip:\n  python -m pip install --upgrade pip",
                    "Check Python path:\n  python -c \"import sys; print(sys.path)\""
                ]
            },
            "general_venv": {
                "triggers": ["virtual environment", "venv", "virtualenv"],
                "title": "Virtual Environment Basics",
                "explanation": """
A virtual environment is an isolated Python environment that allows you to:
- Install packages without affecting your system Python
- Manage different project dependencies separately
- Avoid version conflicts between projects
""",
                "solutions": [
                    "Create virtual environment:\n  python -m venv .venv",
                    "Activate it:\n  - Windows: .venv\\Scripts\\activate\n  - Mac/Linux: source .venv/bin/activate",
                    "Verify it's active:\n  - Your prompt should show (.venv)",
                    "Install packages:\n  pip install package-name",
                    "Deactivate when done:\n  deactivate",
                    "Save dependencies:\n  pip freeze > requirements.txt",
                    "Install from requirements:\n  pip install -r requirements.txt"
                ]
            },
            "path_issues": {
                "triggers": ["path", "directory", "cannot find"],
                "title": "File Path Issues",
                "explanation": """
Path errors occur when Python (or Windows) cannot locate a file or directory.
Common issues:
1. Spaces in path names
2. Incorrect slashes (\\  vs /)
3. Relative vs absolute paths
4. Typos in directory names
""",
                "solutions": [
                    "Use quotes for paths with spaces:\n  cd \"path with spaces\"",
                    "Use raw strings in Python:\n  path = r\"C:\\Users\\Name\\folder\"",
                    "Use pathlib (recommended):\n  from pathlib import Path\n  path = Path(\"E:/Apps/SU/Demo 1\")",
                    "Check current directory:\n  - Windows: cd\n  - Mac/Linux: pwd",
                    "List directory contents:\n  - Windows: dir\n  - Mac/Linux: ls",
                    "Use forward slashes (works on all platforms):\n  path = \"E:/Apps/SU/Demo 1/.venv\""
                ]
            }
        }
    
    def analyze_question(self, question: str) -> Optional[dict]:
        """Analyze user question and return relevant knowledge."""
        question_lower = question.lower()
        
        # Find matching knowledge base entry
        for key, knowledge in self.knowledge_base.items():
            triggers = knowledge.get("triggers", [])
            if any(trigger in question_lower for trigger in triggers):
                return knowledge
        
        return None
    
    def provide_help(self, question: str):
        """Provide help based on the user's question."""
        print("\n" + "="*70)
        print("🐍 PYTHON AI TUTOR")
        print("="*70)
        
        knowledge = self.analyze_question(question)
        
        if knowledge:
            print(f"\n📖 {knowledge['title']}")
            print("-"*70)
            print(knowledge['explanation'])
            
            print("\n✅ SOLUTIONS:")
            for i, solution in enumerate(knowledge['solutions'], 1):
                print(f"\n{i}. {solution}")
            
            if 'prevention' in knowledge:
                print("\n🛡️ PREVENTION / BEST PRACTICES:")
                for tip in knowledge['prevention']:
                    print(f"  • {tip}")
        else:
            print("\n💡 GENERAL PYTHON HELP")
            print("-"*70)
            print("I can help with:")
            print("  • Virtual environment issues (.venv)")
            print("  • Import errors and missing modules")
            print("  • Path and directory problems")
            print("  • Python installation and setup")
            print("\nPlease describe your issue in more detail.")
        
        print("\n" + "="*70)
    
    def interactive_mode(self):
        """Run in interactive mode."""
        print("\n🐍 Python AI Tutor - Interactive Mode")
        print("Type your question or 'quit' to exit\n")
        
        while True:
            question = input("You: ").strip()
            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye! Happy coding!")
                break
            if not question:
                continue
            
            self.provide_help(question)
            print()


def main():
    """Main entry point for CLI."""
    tutor = SimplePythonTutor()
    
    # Check if question provided as command line argument
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        tutor.provide_help(question)
    else:
        tutor.interactive_mode()


if __name__ == "__main__":
    main()
