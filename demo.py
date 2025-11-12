#!/usr/bin/env python3
"""
Demo script showing the application capabilities
This demonstrates the app without requiring Azure credentials
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from azure_services import AzureServicesManager
from ai_tutor import AITutor


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_section(title):
    """Print a section title"""
    print(f"\n{'─' * 70}")
    print(f"  {title}")
    print('─' * 70)


def demo_azure_services():
    """Demonstrate Azure Services Manager"""
    print_header("🔧 Azure Services Manager Demo")
    
    print("Initializing Azure Services Manager...")
    manager = AzureServicesManager()
    
    # Initialize with empty config (demo mode)
    manager.initialize_from_config({})
    
    print("✓ Manager initialized (demo mode - no services)")
    print("\nServices Status:")
    print(f"  • Chat (Azure OpenAI):  {'✓' if manager.chat_client else '✗'} {'Configured' if manager.chat_client else 'Not configured'}")
    print(f"  • TTS (Text-to-Speech): {'✓' if manager.tts_client else '✗'} {'Configured' if manager.tts_client else 'Not configured'}")
    print(f"  • STT (Speech-to-Text): {'✓' if manager.stt_client else '✗'} {'Configured' if manager.stt_client else 'Not configured'}")
    print(f"  • Translator:           {'✓' if manager.translator_client else '✗'} {'Configured' if manager.translator_client else 'Not configured'}")
    
    print("\n💡 To enable services, add credentials to config.json")


def demo_ai_tutor():
    """Demonstrate AI Tutor capabilities"""
    print_header("🤖 AI Tutor Demo")
    
    # Initialize
    manager = AzureServicesManager()
    manager.initialize_from_config({})
    tutor = AITutor(manager)
    
    print("✓ AI Tutor initialized\n")
    
    # Show tutorial topics
    print_section("📚 Available Tutorial Topics")
    topics = tutor.get_tutorial_topics()
    for i, topic in enumerate(topics, 1):
        print(f"  {i:2d}. {topic}")
    
    # Show quick tips
    print_section("💡 Quick Financial Planning Tips")
    tips = tutor.get_quick_tips()
    for tip in tips:
        print(f"  {tip}")
    
    # Show sample tutorial content
    print_section("📖 Sample Tutorial: Getting Started with the App")
    content = tutor.get_tutorial_content("Getting Started with the App")
    print(content)
    
    # Show another tutorial
    print_section("📖 Sample Tutorial: Investment Types Explained")
    content = tutor.get_tutorial_content("Investment Types Explained")
    print(content)


def demo_chat_capability():
    """Demonstrate chat capabilities (would require Azure)"""
    print_header("💬 Chat Capability Demo")
    
    print("The AI Tutor can answer questions like:\n")
    
    sample_questions = [
        "How do I calculate my net worth?",
        "What's the difference between stocks and bonds?",
        "How does compound interest work in the app?",
        "Explain the financial projection calculations",
        "What technologies are used to build this app?",
        "How do I integrate Azure services?",
        "What's the best investment strategy for beginners?",
        "How often should I review my budget?"
    ]
    
    for i, question in enumerate(sample_questions, 1):
        print(f"  {i}. {question}")
    
    print("\n⚠️  Note: Live chat requires Azure OpenAI configuration")
    print("   Configure your credentials in config.json to enable this feature")


def demo_features_summary():
    """Show summary of all features"""
    print_header("✨ Application Features Summary")
    
    print("LEFT PANEL - AI Tutor:")
    print("  ✓ Interactive chat with Azure OpenAI")
    print("  ✓ 12 built-in tutorial topics")
    print("  ✓ Quick financial planning tips")
    print("  ✓ Context-aware conversations")
    print("  ✓ Text-to-Speech for responses (with Azure Speech)")
    print("  ✓ Speech-to-Text for questions (with Azure Speech)")
    print("  ✓ Multi-language translation (with Azure Translator)")
    
    print("\nRIGHT PANEL - Financial Planning App:")
    print("  ✓ Budget tracking (income, expenses)")
    print("  ✓ Investment planning (5 asset types)")
    print("  ✓ Net worth projections")
    print("  ✓ Interactive charts and visualizations")
    print("  ✓ AI suggestions (Gemini, DeepSeek)")
    print("  ✓ Real-time market data (Alpha Vantage)")
    print("  ✓ Botpress chatbot integration")
    
    print("\nINTEGRATION:")
    print("  ✓ Dual-panel desktop interface")
    print("  ✓ Streamlit app launcher")
    print("  ✓ Unified Azure services")
    print("  ✓ Cross-platform (Windows, macOS, Linux)")


def main():
    """Main demo function"""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║                                                                   ║")
    print("║       Financial Planning Assistant - Application Demo            ║")
    print("║                                                                   ║")
    print("║    AI Tutor (Left) + Financial Planning App (Right)              ║")
    print("║                                                                   ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    
    # Run demonstrations
    demo_azure_services()
    demo_ai_tutor()
    demo_chat_capability()
    demo_features_summary()
    
    # Final instructions
    print_header("🚀 Ready to Launch!")
    
    print("To run the full application:")
    print("\n  1. Configure Azure services (optional but recommended):")
    print("     cp config.json.template config.json")
    print("     # Edit config.json with your credentials")
    print("\n  2. Install dependencies:")
    print("     pip install -r requirements.txt")
    print("\n  3. Launch the application:")
    print("     python3 main_app.py")
    print("     # or use: ./run.sh")
    print("\n  4. Click 'Launch Financial App' in the right panel")
    print("\n  5. Start exploring and learning!")
    
    print("\n📖 For detailed instructions, see:")
    print("   • README.md - Complete documentation")
    print("   • USAGE_GUIDE.md - Step-by-step usage guide")
    
    print("\n" + "=" * 70)
    print()


if __name__ == "__main__":
    main()
