"""
AI Tutor Module
Provides an interactive AI tutor to explain the financial planning application
"""

from typing import Optional, List
from azure_services import AzureServicesManager


class AITutor:
    """AI Tutor that explains the financial planning application"""
    
    def __init__(self, azure_manager: AzureServicesManager):
        self.azure_manager = azure_manager
        self.conversation_history: List[dict] = []
        self.system_prompt = self._get_system_prompt()
        
        # Initialize conversation with system prompt
        self.conversation_history.append({
            "role": "system",
            "content": self.system_prompt
        })
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the AI tutor"""
        return """You are an AI tutor specialized in explaining financial planning applications and Python programming.

Your role is to help users understand how the financial planning application works, including:
1. The purpose and functionality of each component
2. How the budget calculation works
3. How investment projections are calculated
4. How to interpret the visualizations and charts
5. Best practices for financial planning
6. How the application is built using Python, Streamlit, and other technologies

When explaining code, be clear, concise, and educational. Use examples and analogies when helpful.
Break down complex concepts into simple, understandable parts.
Be encouraging and supportive of the user's learning journey.

You can also answer questions about:
- Python programming concepts used in the app
- Streamlit framework basics
- Financial planning principles
- Data visualization with Plotly
- API integration patterns
- Best practices for building financial applications

Always be patient, friendly, and aim to enhance the user's understanding."""
    
    def ask(self, question: str) -> str:
        """Ask the AI tutor a question"""
        if not self.azure_manager.chat_client:
            return "Azure OpenAI service is not configured. Please set up Azure credentials."
        
        # Add user question to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": question
        })
        
        # Get response from Azure OpenAI
        response = self.azure_manager.chat_client.chat_completion(
            messages=self.conversation_history,
            temperature=0.7
        )
        
        # Add assistant response to conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        # Keep conversation history manageable (last 10 exchanges)
        if len(self.conversation_history) > 21:  # system + 10 exchanges (20 messages)
            self.conversation_history = [self.conversation_history[0]] + self.conversation_history[-20:]
        
        return response
    
    def speak_response(self, text: str) -> Optional[bytes]:
        """Convert text response to speech"""
        if not self.azure_manager.tts_client:
            return None
        
        return self.azure_manager.tts_client.synthesize_speech(text)
    
    def listen_to_question(self, audio_data: bytes) -> str:
        """Convert speech to text for user question"""
        if not self.azure_manager.stt_client:
            return ""
        
        return self.azure_manager.stt_client.recognize_from_audio(audio_data)
    
    def translate_response(self, text: str, target_language: str) -> str:
        """Translate response to target language"""
        if not self.azure_manager.translator_client:
            return text
        
        return self.azure_manager.translator_client.translate_text(text, target_language)
    
    def get_quick_tips(self) -> List[str]:
        """Get quick tips about the financial planning app"""
        return [
            "💡 Start by entering your monthly income and tax rate",
            "💡 Break down all your monthly expenses accurately",
            "💡 Diversify your investments across different asset classes",
            "💡 Aim to save at least 20% of your after-tax income",
            "💡 Review and adjust your budget regularly",
            "💡 Use the projection slider to see long-term growth",
            "💡 Monitor your net worth growth over time",
            "💡 Consider talking to a financial advisor for personalized advice"
        ]
    
    def get_tutorial_topics(self) -> List[str]:
        """Get list of tutorial topics available"""
        return [
            "Getting Started with the App",
            "Understanding Budget Categories",
            "Investment Types Explained",
            "How Projections Work",
            "Reading the Charts and Graphs",
            "Tax Calculations",
            "Setting Financial Goals",
            "Monthly Net Worth Calculation",
            "Using AI Suggestions Effectively",
            "App Architecture and Code Structure",
            "Python and Streamlit Basics",
            "Integrating External APIs"
        ]
    
    def get_tutorial_content(self, topic: str) -> str:
        """Get detailed tutorial content for a specific topic"""
        tutorials = {
            "Getting Started with the App": """
**Getting Started with the Financial Planning App**

1. **Set Your Income**: Enter your gross monthly income in the sidebar
2. **Configure Tax Rate**: Adjust the tax rate slider to match your bracket
3. **Enter Expenses**: Fill in all your monthly expense categories:
   - Housing/Rent
   - Food/Groceries
   - Transportation
   - Utilities
   - Entertainment
   - Other expenses
4. **Plan Investments**: Allocate monthly investment amounts across:
   - Stocks
   - Bonds
   - Real Estate
   - Cryptocurrency
   - Fixed Deposits
5. **Set Goals**: Choose your projection period and savings target
6. **Analyze**: Review the charts and get AI suggestions

The app will automatically calculate your net cash flow and project your net worth over time!
""",
            "Understanding Budget Categories": """
**Budget Categories Explained**

**Income**: Your gross monthly salary or revenue before taxes

**Expenses**:
- **Housing**: Rent, mortgage, property maintenance
- **Food**: Groceries, dining out, meal delivery
- **Transport**: Car payments, gas, public transit, ride-sharing
- **Utilities**: Electricity, water, internet, phone bills
- **Entertainment**: Subscriptions, hobbies, outings
- **Others**: Insurance, healthcare, personal care, miscellaneous

**Investments**: Money you allocate to grow wealth over time

**Net Cash Flow**: Income - Taxes - Expenses - Investments
This is what you have left over each month for savings or emergency funds.
""",
            "Investment Types Explained": """
**Investment Types in the App**

**Stocks**: 
- Ownership shares in companies
- Higher potential returns but more volatile
- App uses SPY (S&P 500) as benchmark

**Bonds**:
- Fixed-income securities (loans to governments/corporations)
- Lower risk, steady returns
- App uses AGG as benchmark

**Real Estate**:
- Property investments, REITs
- Moderate risk, inflation hedge

**Cryptocurrency**:
- Digital assets like Bitcoin, Ethereum
- High risk, high potential returns

**Fixed Deposits**:
- Bank savings with guaranteed returns
- Lowest risk, lowest returns

Diversification across these types helps manage risk!
""",
            "How Projections Work": """
**Understanding Financial Projections**

The app projects your net worth using compound growth:

1. **Monthly Contribution**: Your investment amount each month
2. **Return Rate**: Expected monthly return for each asset class
   - Fetched from real market data (Alpha Vantage API)
   - Uses historical averages as fallback

3. **Future Value Formula**:
   ```
   FV = PMT × [(1 + r)^n - 1] / r
   ```
   Where:
   - PMT = monthly investment
   - r = monthly return rate
   - n = number of months

4. **Net Worth**: Sum of all investment values plus cash balance

The projection helps you see if you'll reach your savings target!
"""
        }
        
        return tutorials.get(topic, "Tutorial content not available for this topic.")
    
    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation_history = [{
            "role": "system",
            "content": self.system_prompt
        }]
