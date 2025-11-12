# Financial Planning Assistant with AI Tutor

A Python desktop application that combines financial planning tools with an AI tutor, both integrated with Azure cognitive services.

## Overview

This application features a **dual-panel interface**:
- **Left Panel**: AI Tutor that explains how the financial planning app works
- **Right Panel**: Financial Planning application for budget and investment tracking

Both panels are integrated with Azure services for enhanced functionality:
- **Azure OpenAI**: Powers the AI tutor with intelligent responses
- **Azure Speech Services (TTS)**: Converts AI responses to speech
- **Azure Speech Services (STT)**: Converts user voice input to text
- **Azure Translator**: Provides multi-language support

## Features

### AI Tutor (Left Panel)
- 🤖 Interactive chat interface with Azure OpenAI
- 📚 Built-in tutorial topics covering:
  - Getting started with the app
  - Understanding budget categories
  - Investment types and strategies
  - Financial projections and calculations
  - App architecture and code structure
- 💡 Quick tips for financial planning
- 🔊 Text-to-Speech support for responses
- 🎤 Speech-to-Text for voice questions (planned)
- 🌐 Multi-language translation support
- 💬 Context-aware conversations with memory

### Financial Planning App (Right Panel)
- 💰 Budget tracking with multiple expense categories
- 📊 Investment planning across multiple asset types:
  - Stocks (with real-time data from Alpha Vantage)
  - Bonds
  - Real Estate
  - Cryptocurrency
  - Fixed Deposits
- 📈 Net worth projections over time
- 📉 Interactive charts and visualizations with Plotly
- 🤖 Multi-LLM AI suggestions (Gemini, DeepSeek)
- 💬 Botpress chatbot integration
- 🎯 Savings target tracking

## Installation

### Prerequisites
- Python 3.8 or higher
- Azure account with the following services (optional but recommended):
  - Azure OpenAI Service
  - Azure Speech Services
  - Azure Translator Service

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/adnbal/financialplanning.git
   cd financialplanning
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Azure Services:**
   
   Option A: Using configuration file (recommended)
   ```bash
   cp config.json.template config.json
   # Edit config.json with your Azure credentials
   ```

   Option B: Using environment variables
   ```bash
   export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
   export AZURE_OPENAI_API_KEY="your-api-key"
   export AZURE_OPENAI_DEPLOYMENT="gpt-4"
   export AZURE_SPEECH_KEY="your-speech-key"
   export AZURE_SPEECH_REGION="your-region"
   export AZURE_TRANSLATOR_KEY="your-translator-key"
   export AZURE_TRANSLATOR_REGION="your-region"
   ```

4. **Configure Streamlit Secrets (for financial app):**
   
   Create `.streamlit/secrets.toml`:
   ```toml
   [botpress]
   chat_api_id = "your-botpress-api-id"
   token = "your-botpress-token"

   [gemini]
   api_key = "your-gemini-api-key"

   [openrouter]
   api_key = "your-openrouter-api-key"

   [alpha_vantage]
   api_key = "your-alpha-vantage-api-key"
   ```

## Usage

### Starting the Application

**Launch the dual-panel desktop app:**
```bash
python main_app.py
```

This will open the main application window with:
- AI Tutor on the left
- Financial app launcher on the right

### Using the AI Tutor

1. **Ask Questions**: Type your question in the input field and press Enter or click "Ask"
2. **Load Tutorials**: Select a topic from the dropdown and click "Load Tutorial"
3. **Quick Tips**: Click "Quick Tips" to get instant financial advice
4. **Clear Chat**: Reset the conversation with "Clear Chat"
5. **Text-to-Speech**: Click "🔊 Speak Last" to hear the last AI response

Example questions:
- "How do I calculate my net worth?"
- "What's the difference between stocks and bonds?"
- "How does the investment projection work?"
- "Explain the code structure of the app"

### Using the Financial Planning App

1. **Launch the App**: Click "🚀 Launch Financial App" in the right panel
2. **Wait for Browser**: The app will open automatically in your browser
3. **Enter Your Data**: Fill in your income, expenses, and investments in the sidebar
4. **View Projections**: Adjust the time period and see your financial growth
5. **Get AI Advice**: Use the AI suggestion buttons for personalized recommendations
6. **Chat with Bot**: Ask questions to the Botpress financial assistant

### Stopping the Application

- Click "⏹ Stop App" to stop the financial planning app
- Close the main window to exit the desktop application

## Architecture

### Project Structure
```
financialplanning/
├── main_app.py              # Main dual-panel desktop application
├── ai_tutor.py              # AI Tutor logic and tutorial content
├── azure_services.py        # Azure service integrations
├── budget_invest_app.py     # Financial planning Streamlit app
├── botpress_client.py       # Botpress API client
├── requirements.txt         # Python dependencies
├── config.json.template     # Azure configuration template
└── README.md               # This file
```

### Technology Stack

**Desktop Application:**
- Tkinter: GUI framework
- Threading: Async operations
- subprocess: Streamlit app launcher

**AI & Azure Services:**
- Azure OpenAI: Chat completion API
- Azure Speech Services: TTS and STT
- Azure Translator: Multi-language support

**Financial Planning App:**
- Streamlit: Web framework
- Pandas: Data manipulation
- Plotly: Interactive visualizations
- Alpha Vantage API: Real-time market data
- Gemini & DeepSeek: AI suggestions
- Botpress: Chatbot integration

## How It Works

### AI Tutor Flow
1. User types or speaks a question
2. Question is sent to Azure OpenAI with context
3. AI generates educational response
4. Response displayed in chat and optionally spoken via TTS
5. Conversation context maintained for follow-up questions

### Financial Planning Flow
1. User enters financial data in Streamlit sidebar
2. App calculates net cash flow and projections
3. Real-time market data fetched from Alpha Vantage
4. Interactive charts display financial growth
5. AI models provide personalized advice
6. Botpress chatbot answers specific questions

### Integration Between Panels
- AI Tutor explains how the financial app works
- Users can ask about specific features or calculations
- Both panels share Azure service connections
- Seamless learning and application experience

## Configuration Details

### Azure OpenAI
- **Required for**: AI Tutor chat functionality
- **Model**: GPT-4 or GPT-3.5-turbo
- **Setup**: Create Azure OpenAI resource, deploy model, get endpoint and key

### Azure Speech Services
- **Required for**: Text-to-Speech and Speech-to-Text
- **Setup**: Create Speech resource, get key and region
- **Voices**: Uses en-US-JennyNeural by default (configurable)

### Azure Translator
- **Required for**: Multi-language support
- **Setup**: Create Translator resource, get key and region
- **Languages**: Supports 100+ languages

### Other APIs
- **Alpha Vantage**: Free tier allows 5 requests/minute
- **Gemini**: Google's AI model for financial advice
- **OpenRouter**: Access to DeepSeek and other models
- **Botpress**: Conversational AI platform

## Troubleshooting

### Common Issues

**1. "Azure OpenAI service is not configured"**
- Check your config.json or environment variables
- Ensure endpoint URL is correct (includes https://)
- Verify API key is valid

**2. "Streamlit Not Installed"**
- Run: `pip install streamlit`
- Check with: `streamlit --version`

**3. Financial app won't launch**
- Ensure budget_invest_app.py exists
- Check Streamlit secrets are configured
- Verify port 8501 is not in use

**4. TTS/STT not working**
- Verify Azure Speech credentials
- Check region is correct
- Ensure internet connectivity

**5. API rate limits**
- Alpha Vantage: Free tier is limited to 5 calls/minute
- Consider upgrading or caching results

## Development

### Adding New Tutorial Topics

Edit `ai_tutor.py` and add to `get_tutorial_content()`:
```python
tutorials = {
    "Your New Topic": """
    Tutorial content here...
    """
}
```

### Customizing the UI

Edit `main_app.py`:
- Modify `setup_left_panel()` for tutor interface
- Modify `setup_right_panel()` for app launcher
- Adjust colors, fonts, and layout in respective methods

### Adding Azure Services

Edit `azure_services.py`:
1. Create new client class
2. Add to `AzureServicesManager`
3. Initialize in `initialize_from_config()`

## Security Notes

- Never commit `config.json` or `.streamlit/secrets.toml` to version control
- Use environment variables in production
- Keep API keys secure and rotate regularly
- Follow Azure security best practices

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is provided as-is for educational and personal use.

## Support

For issues and questions:
- Open an issue on GitHub
- Check Azure documentation for service-specific problems
- Review Streamlit docs for app-related questions

## Acknowledgments

- Azure Cognitive Services for AI capabilities
- Streamlit for the web framework
- Alpha Vantage for market data
- Plotly for visualizations
- All open-source contributors

---

**Made with ❤️ for better financial planning and learning**
