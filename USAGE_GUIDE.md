# Usage Guide - Financial Planning Assistant

## Quick Start Guide

### For Testing Without Azure (Demo Mode)

If you want to test the application without setting up Azure services:

1. **Run the application:**
   ```bash
   python3 main_app.py
   ```

2. **What works in Demo Mode:**
   - ✓ The dual-panel interface will load
   - ✓ Tutorial topics and quick tips work
   - ✓ Financial app launcher works
   - ✗ AI chat requires Azure OpenAI (shows error message)
   - ✗ Text-to-Speech requires Azure Speech Services
   - ✗ Speech-to-Text requires Azure Speech Services
   - ✗ Translation requires Azure Translator

### For Full Functionality (With Azure)

1. **Set up Azure services** (see Azure Setup section below)

2. **Configure the application:**
   ```bash
   cp config.json.template config.json
   # Edit config.json with your credentials
   ```

3. **Run the application:**
   ```bash
   python3 main_app.py
   # or use the launcher:
   ./run.sh
   ```

## Using the AI Tutor (Left Panel)

### Tutorial Topics

The AI Tutor includes pre-written tutorials on various topics:

1. **Select a topic** from the dropdown menu
2. **Click "Load Tutorial"** to display the content
3. **Topics available:**
   - Getting Started with the App
   - Understanding Budget Categories
   - Investment Types Explained
   - How Projections Work
   - Reading the Charts and Graphs
   - Tax Calculations
   - Setting Financial Goals
   - Monthly Net Worth Calculation
   - Using AI Suggestions Effectively
   - App Architecture and Code Structure
   - Python and Streamlit Basics
   - Integrating External APIs

### Chat with AI Tutor (Requires Azure OpenAI)

1. **Type your question** in the input field at the bottom
2. **Press Enter** or click "Ask" button
3. **Wait for response** - AI will think and reply
4. **Follow-up questions** are welcome - context is maintained

**Example questions:**
```
- How do I calculate my monthly savings?
- What's the difference between stocks and bonds?
- Explain how the compound interest calculation works
- Show me how to interpret the net worth chart
- How is this app built with Python and Streamlit?
- What APIs does the app use?
```

### Quick Tips

Click the **"Quick Tips"** button to get instant financial planning advice without using Azure API calls.

### Text-to-Speech (Requires Azure Speech)

1. **Ask a question** and get a response
2. **Click "🔊 Speak Last"** button
3. **Audio will be generated** and played automatically
4. Works on Windows, macOS, and Linux

### Clearing the Chat

Click **"Clear Chat"** to:
- Reset the conversation
- Clear the chat history
- Start fresh with the AI Tutor

## Using the Financial Planning App (Right Panel)

### Launching the App

1. **Click "🚀 Launch Financial App"** button
2. **Wait a few seconds** for Streamlit to start
3. **Browser will open automatically** at http://localhost:8501
4. **Status indicator** shows "Running on port 8501"

### If Launch Fails

Check these common issues:

**Streamlit not installed:**
```bash
pip install streamlit
```

**Port 8501 already in use:**
```bash
# Find and kill the process using port 8501
lsof -ti:8501 | xargs kill -9
```

**Missing secrets file:**
Create `.streamlit/secrets.toml` with your API keys (see Configuration section)

### Using the Financial App

Once launched in your browser:

1. **Enter Income Information:**
   - Monthly income (before tax)
   - Tax rate percentage

2. **Add Your Expenses:**
   - Housing/Rent
   - Food/Groceries
   - Transportation
   - Utilities
   - Entertainment
   - Other expenses

3. **Plan Your Investments:**
   - Stocks
   - Bonds
   - Real Estate
   - Cryptocurrency
   - Fixed Deposits

4. **Set Your Goals:**
   - Projection period (months)
   - Savings target amount

5. **Analyze Results:**
   - View net cash flow
   - See net worth projection chart
   - Check expense breakdown pie chart
   - Review investment allocation

6. **Get AI Suggestions:**
   - Click "Generate Gemini Suggestion"
   - Or "Generate DeepSeek Suggestion"
   - Get personalized financial advice

7. **Chat with Financial Assistant:**
   - Type questions in the Botpress chat
   - Get instant answers about your finances

### Stopping the Financial App

1. **Click "⏹ Stop App"** in the desktop application
2. **Or close the browser tab** (app keeps running in background)
3. **Or press Ctrl+C** in terminal if running standalone

## Configuration

### Azure OpenAI Setup

1. **Create Azure OpenAI resource:**
   - Go to Azure Portal
   - Create "Azure OpenAI" resource
   - Deploy a model (gpt-4 or gpt-35-turbo)

2. **Get credentials:**
   - Endpoint: `https://YOUR-RESOURCE-NAME.openai.azure.com/`
   - API Key: Found in "Keys and Endpoint" section
   - Deployment name: Name you gave the model

3. **Add to config.json:**
   ```json
   {
     "azure_openai": {
       "endpoint": "https://your-resource.openai.azure.com/",
       "api_key": "your-32-character-key",
       "deployment": "gpt-4"
     }
   }
   ```

### Azure Speech Services Setup

1. **Create Speech resource:**
   - Azure Portal → Create "Speech Services"
   - Choose a region (e.g., eastus, westus2)

2. **Get credentials:**
   - Key: Found in "Keys and Endpoint"
   - Region: The region you selected

3. **Add to config.json:**
   ```json
   {
     "azure_speech": {
       "key": "your-speech-key",
       "region": "eastus"
     }
   }
   ```

### Azure Translator Setup

1. **Create Translator resource:**
   - Azure Portal → Create "Translator"
   - Choose a region

2. **Get credentials:**
   - Key: Found in "Keys and Endpoint"
   - Region: The region you selected

3. **Add to config.json:**
   ```json
   {
     "azure_translator": {
       "key": "your-translator-key",
       "region": "eastus"
     }
   }
   ```

### Streamlit Secrets Setup

Create `.streamlit/secrets.toml`:

```toml
# Botpress Configuration
[botpress]
chat_api_id = "your-botpress-bot-id"
token = "bp_pat_xxxxxxxxxxxxx"

# Google Gemini
[gemini]
api_key = "AIzaSy-xxxxxxxxxxxxx"

# OpenRouter (for DeepSeek)
[openrouter]
api_key = "sk-or-xxxxxxxxxxxxx"

# Alpha Vantage (Stock Data)
[alpha_vantage]
api_key = "your-alphavantage-key"
```

**Getting these API keys:**

- **Botpress**: Sign up at https://botpress.com/
- **Gemini**: Get free key at https://makersuite.google.com/
- **OpenRouter**: Sign up at https://openrouter.ai/
- **Alpha Vantage**: Free key at https://www.alphavantage.co/

## Keyboard Shortcuts

### In AI Tutor Chat
- **Enter**: Send message
- **Ctrl+A**: Select all text in input

### In Main Window
- **Alt+F4** (Windows/Linux) or **Cmd+Q** (Mac): Close application

## Troubleshooting

### "Azure OpenAI service is not configured"

**Solution:**
1. Check config.json exists and has valid credentials
2. Verify endpoint URL format: `https://NAME.openai.azure.com/`
3. Ensure API key is correct (32 characters)
4. Check deployment name matches your Azure deployment

### "Failed to launch app: budget_invest_app.py not found"

**Solution:**
1. Ensure you're in the correct directory
2. Verify budget_invest_app.py exists
3. Check file permissions

### Text-to-Speech Not Working

**Solutions:**
1. Verify Azure Speech key and region in config.json
2. Check internet connectivity
3. Ensure audio device is working
4. Check if audio file is created in /tmp/

### Financial App Shows Errors

**Solutions:**
1. Check `.streamlit/secrets.toml` exists
2. Verify all API keys are valid
3. Check API rate limits (Alpha Vantage: 5 calls/minute)
4. Restart Streamlit app

### Port 8501 Already in Use

**Solution:**
```bash
# Kill existing Streamlit process
pkill -f streamlit
# Or find and kill specific process
lsof -ti:8501 | xargs kill -9
```

## Tips for Best Experience

### Financial Planning Tips

1. **Be Accurate**: Enter exact figures for best projections
2. **Regular Updates**: Review and update monthly
3. **Diversify**: Spread investments across asset types
4. **Emergency Fund**: Keep 3-6 months of expenses in savings
5. **Track Progress**: Compare actual vs. projected regularly

### AI Tutor Tips

1. **Be Specific**: Ask detailed questions for better answers
2. **Context**: The AI remembers conversation history
3. **Follow-up**: Ask clarifying questions if needed
4. **Tutorials First**: Check built-in tutorials before asking
5. **Experiment**: Try different question styles

### Performance Tips

1. **Close Unused Apps**: Free up system resources
2. **Stable Internet**: Required for Azure services and APIs
3. **API Limits**: Be aware of rate limits (especially Alpha Vantage)
4. **Clear Cache**: Restart app if it becomes slow

## Advanced Usage

### Running Streamlit App Standalone

```bash
streamlit run budget_invest_app.py
```

### Using Environment Variables Instead of config.json

```bash
export AZURE_OPENAI_ENDPOINT="https://your.openai.azure.com/"
export AZURE_OPENAI_API_KEY="your-key"
export AZURE_OPENAI_DEPLOYMENT="gpt-4"
export AZURE_SPEECH_KEY="your-speech-key"
export AZURE_SPEECH_REGION="eastus"
export AZURE_TRANSLATOR_KEY="your-translator-key"
export AZURE_TRANSLATOR_REGION="eastus"

python3 main_app.py
```

### Customizing Tutorial Content

Edit `ai_tutor.py` and modify the `get_tutorial_content()` method to add your own tutorials.

### Changing UI Colors and Fonts

Edit `main_app.py` and modify the font configurations in `setup_left_panel()` and `setup_right_panel()`.

## Getting Help

1. **Check README.md**: Comprehensive documentation
2. **Read this guide**: Most common issues covered
3. **Azure Docs**: https://docs.microsoft.com/azure/
4. **Streamlit Docs**: https://docs.streamlit.io/
5. **GitHub Issues**: Report bugs or ask questions

## Next Steps

1. ✓ Launch the application
2. ✓ Explore tutorial topics
3. ✓ Launch financial planning app
4. ✓ Enter your financial data
5. ✓ Ask AI Tutor questions
6. ✓ Get personalized financial advice
7. ✓ Track your progress over time

**Happy Financial Planning! 💰**
