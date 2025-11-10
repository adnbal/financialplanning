#!/usr/bin/env python3
"""
Test script for Python AI Tutor functionality.
"""

import sys
from python_tutor_cli import SimplePythonTutor


def test_venv_error():
    """Test virtual environment error detection."""
    tutor = SimplePythonTutor()
    question = "The system cannot find the path specified .venv"
    knowledge = tutor.analyze_question(question)
    assert knowledge is not None, "Should detect venv error"
    assert knowledge['title'] == "Virtual Environment Path Error"
    print("✓ test_venv_error passed")


def test_import_error():
    """Test import error detection."""
    tutor = SimplePythonTutor()
    question = "ModuleNotFoundError: No module named 'requests'"
    knowledge = tutor.analyze_question(question)
    assert knowledge is not None, "Should detect import error"
    assert knowledge['title'] == "Import Error / Module Not Found"
    print("✓ test_import_error passed")


def test_general_venv_question():
    """Test general virtual environment question."""
    tutor = SimplePythonTutor()
    question = "How do I create a virtual environment?"
    knowledge = tutor.analyze_question(question)
    assert knowledge is not None, "Should detect venv question"
    assert knowledge['title'] == "Virtual Environment Basics"
    print("✓ test_general_venv_question passed")


def test_path_issues():
    """Test path issue detection."""
    tutor = SimplePythonTutor()
    question = "How do I handle file paths with spaces in Python?"
    knowledge = tutor.analyze_question(question)
    assert knowledge is not None, "Should detect path issue"
    assert knowledge['title'] == "File Path Issues"
    print("✓ test_path_issues passed")


def test_unknown_question():
    """Test handling of unknown questions."""
    tutor = SimplePythonTutor()
    question = "What is machine learning?"
    knowledge = tutor.analyze_question(question)
    # Should return None for unrecognized questions
    assert knowledge is None, "Should not match any pattern"
    print("✓ test_unknown_question passed")


def test_knowledge_base_structure():
    """Test that knowledge base is properly structured."""
    tutor = SimplePythonTutor()
    kb = tutor.knowledge_base

    # Check all entries have required fields
    for key, knowledge in kb.items():
        assert 'triggers' in knowledge, f"{key} missing triggers"
        assert 'title' in knowledge, f"{key} missing title"
        assert 'explanation' in knowledge, f"{key} missing explanation"
        assert 'solutions' in knowledge, f"{key} missing solutions"
        assert len(knowledge['solutions']) > 0, f"{key} has no solutions"

    print("✓ test_knowledge_base_structure passed")


def run_all_tests():
    """Run all tests."""
    tests = [
        test_venv_error,
        test_import_error,
        test_general_venv_question,
        test_path_issues,
        test_unknown_question,
        test_knowledge_base_structure
    ]

    print("Running Python AI Tutor tests...\n")
    failed = 0

    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Tests completed: {len(tests) - failed}/{len(tests)} passed")

    if failed > 0:
        print(f"❌ {failed} test(s) failed")
        sys.exit(1)
    else:
        print("✅ All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    run_all_tests()
