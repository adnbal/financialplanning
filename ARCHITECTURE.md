# Architecture Documentation

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Financial Planning Assistant                      │
│                         Desktop Application                          │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │       main_app.py         │
                    │   (Tkinter Desktop UI)    │
                    └─────────────┬─────────────┘
                                  │
            ┌─────────────────────┴─────────────────────┐
            │                                           │
    ┌───────▼────────┐                      ┌──────────▼─────────┐
    │   LEFT PANEL   │                      │   RIGHT PANEL      │
    │   AI TUTOR     │                      │  FINANCIAL APP     │
    └───────┬────────┘                      └──────────┬─────────┘
            │                                           │
            │                                           │
    ┌───────▼────────┐                      ┌──────────▼─────────┐
    │  ai_tutor.py   │                      │ budget_invest_app.py│
    │                │                      │   (Streamlit)      │
    │ • Chat         │                      │                    │
    │ • Tutorials    │                      │ • Budget Track     │
    │ • Quick Tips   │                      │ • Investment Plan  │
    │ • TTS/STT      │                      │ • Net Worth Calc   │
    │ • Translation  │                      │ • AI Suggestions   │
    └───────┬────────┘                      └──────────┬─────────┘
            │                                           │
            │                                           │
    ┌───────▼────────────────────────────────┐         │
    │    azure_services.py                   │         │
    │    (Azure Services Manager)            │         │
    └───────┬────────────────────────────────┘         │
            │                                           │
            ├───────────┬───────────┬──────────┐       │
            │           │           │          │       │
    ┌───────▼──┐  ┌─────▼────┐  ┌──▼─────┐ ┌─▼────┐  │
    │  Azure   │  │  Azure   │  │ Azure  │ │Azure │  │
    │ OpenAI   │  │   TTS    │  │  STT   │ │Trans │  │
    │  (Chat)  │  │ (Speech) │  │(Speech)│ │lator │  │
    └──────────┘  └──────────┘  └────────┘ └──────┘  │
                                                       │
                    External APIs Used by              │
                    Financial App                      │
                    ┌──────────────────────────────────┘
                    │
        ┌───────────┼───────────┬────────────┬──────────────┐
        │           │           │            │              │
    ┌───▼───┐  ┌────▼────┐ ┌───▼─────┐ ┌────▼─────┐  ┌────▼────┐
    │Gemini │  │DeepSeek │ │Botpress │ │  Alpha   │  │ Others  │
    │  API  │  │   API   │ │   API   │ │ Vantage  │  │   ...   │
    └───────┘  └─────────┘ └─────────┘ └──────────┘  └─────────┘
```

## Component Details

### 1. Main Application Layer (`main_app.py`)

**Purpose**: Desktop UI and application orchestration

**Responsibilities**:
- Create and manage Tkinter window
- Handle user interactions
- Coordinate between panels
- Manage Streamlit subprocess
- Display status information

**Key Classes**:
- `DualPanelApp`: Main application controller

**Technologies**:
- Tkinter for GUI
- Threading for async operations
- subprocess for Streamlit launcher

---

### 2. AI Tutor Component (`ai_tutor.py`)

**Purpose**: Educational assistant and conversation manager

**Responsibilities**:
- Manage chat conversations
- Provide tutorial content
- Handle Azure service calls
- Maintain conversation context

**Key Classes**:
- `AITutor`: Main tutor logic

**Features**:
- 12 built-in tutorials
- 8 quick tips
- Context-aware conversations
- Multi-modal interaction (text, voice)

---

### 3. Azure Services Layer (`azure_services.py`)

**Purpose**: Unified Azure services integration

**Responsibilities**:
- Initialize Azure clients
- Handle API requests
- Manage credentials
- Error handling

**Key Classes**:
- `AzureOpenAIClient`: Chat completion
- `AzureTTSClient`: Text-to-Speech
- `AzureSTTClient`: Speech-to-Text
- `AzureTranslatorClient`: Translation
- `AzureServicesManager`: Unified manager

---

### 4. Financial Planning App (`budget_invest_app.py`)

**Purpose**: Budget and investment tracking

**Responsibilities**:
- Calculate budgets
- Project investments
- Visualize data
- Provide AI suggestions

**Technologies**:
- Streamlit for UI
- Pandas for data
- Plotly for charts
- Multiple AI APIs

---

## Data Flow Diagrams

### User Question Flow (AI Tutor)

```
User Types Question
       │
       ▼
┌──────────────┐
│ main_app.py  │ ─────► Display in chat
│ (Input)      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ ai_tutor.py  │ ─────► Add to conversation history
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ azure_services.py│ ─────► AzureOpenAIClient
│ (Chat API Call)  │
└──────┬───────────┘
       │
       ▼
┌──────────────┐
│ Azure OpenAI │ ─────► GPT-4 processes
└──────┬───────┘
       │
       ▼
Response Generated
       │
       ▼
┌──────────────┐
│ ai_tutor.py  │ ─────► Add response to history
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ main_app.py  │ ─────► Display response
│ (Output)     │
└──────────────┘
```

### Text-to-Speech Flow

```
User Clicks "Speak Last"
       │
       ▼
┌──────────────┐
│ main_app.py  │ ─────► Get last response text
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ ai_tutor.py  │ ─────► speak_response(text)
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ azure_services.py│ ─────► AzureTTSClient
│ (TTS API Call)   │
└──────┬───────────┘
       │
       ▼
┌──────────────┐
│ Azure Speech │ ─────► Synthesize audio
└──────┬───────┘
       │
       ▼
Audio File (MP3)
       │
       ▼
┌──────────────┐
│ main_app.py  │ ─────► Play audio file
│ (OS specific)│
└──────────────┘
```

### Financial App Launch Flow

```
User Clicks "Launch"
       │
       ▼
┌──────────────┐
│ main_app.py  │ ─────► Check if already running
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ subprocess.Popen │ ─────► Launch Streamlit
└──────┬───────────┘
       │
       ▼
┌─────────────────┐
│ Streamlit Server│ ─────► Start on port 8501
└──────┬──────────┘
       │
       ▼
┌──────────────┐
│ webbrowser   │ ─────► Open browser tab
│ .open()      │
└──────────────┘
```

---

## Configuration Flow

### Config Loading Priority

```
1. Check for config.json file
       │
       ├─ Found ────► Load and parse JSON
       │              │
       │              ▼
       │         Initialize Azure clients
       │
       └─ Not Found ──► Check environment variables
                        │
                        ├─ Found ────► Use env vars
                        │              │
                        │              ▼
                        │         Initialize Azure clients
                        │
                        └─ Not Found ──► Run in demo mode
                                        (limited functionality)
```

### Configuration Sources

**Option 1: config.json**
```json
{
  "azure_openai": {...},
  "azure_speech": {...},
  "azure_translator": {...}
}
```

**Option 2: Environment Variables**
```bash
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_API_KEY=...
AZURE_SPEECH_KEY=...
...
```

---

## Module Dependencies

```
main_app.py
    ├── tkinter (built-in)
    ├── threading (built-in)
    ├── subprocess (built-in)
    ├── webbrowser (built-in)
    ├── azure_services.py
    └── ai_tutor.py
            └── azure_services.py

ai_tutor.py
    └── azure_services.py

azure_services.py
    ├── requests (external)
    ├── azure-cognitiveservices-speech (external)
    └── azure-ai-translation-text (external)

budget_invest_app.py
    ├── streamlit (external)
    ├── pandas (external)
    ├── plotly (external)
    ├── requests (external)
    └── google-generativeai (external)
```

---

## State Management

### Application State

```
DualPanelApp (main_app.py)
│
├── Azure Manager State
│   ├── chat_client (initialized or None)
│   ├── tts_client (initialized or None)
│   ├── stt_client (initialized or None)
│   └── translator_client (initialized or None)
│
├── AI Tutor State
│   ├── conversation_history (list of messages)
│   ├── last_response (string)
│   └── system_prompt (string)
│
└── Streamlit Process State
    ├── streamlit_process (Popen object or None)
    └── streamlit_port (8501)
```

### Session State (Streamlit App)

```
Streamlit Session State
│
├── conversation_id (Botpress)
├── User inputs (income, expenses, etc.)
└── Cached API responses
```

---

## Error Handling Strategy

### Levels of Error Handling

1. **API Level** (azure_services.py)
   - Catch HTTP errors
   - Return error messages or None
   - Log errors to console

2. **Business Logic Level** (ai_tutor.py)
   - Check for None responses
   - Provide fallback messages
   - Graceful degradation

3. **UI Level** (main_app.py)
   - Show user-friendly messages
   - Update status indicators
   - Disable unavailable features

### Error Propagation

```
Azure API Error
    │
    ▼
azure_services.py catches exception
    │
    ▼
Returns error string or None
    │
    ▼
ai_tutor.py checks for None
    │
    ▼
Returns fallback message
    │
    ▼
main_app.py displays to user
```

---

## Security Architecture

### Security Layers

```
┌─────────────────────────────────────────┐
│         User Interface Layer            │
│  (No sensitive data displayed)          │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      Application Logic Layer            │
│  (Credentials loaded, never logged)     │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│     Configuration Layer                 │
│  (config.json in .gitignore)           │
│  (Environment variables)                │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│       Network Layer                     │
│  (HTTPS only, timeout limits)          │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│       Azure Services                    │
│  (Managed by Microsoft)                │
└─────────────────────────────────────────┘
```

### Credential Flow

```
Credentials (stored securely)
    │
    ├─ config.json (local file, .gitignore)
    │       │
    │       └─► Loaded at startup
    │
    └─ Environment Variables
            │
            └─► Loaded at startup
                    │
                    ▼
            Used to initialize clients
                    │
                    ▼
            Stored in memory only
                    │
                    ▼
            Used for API calls
                    │
                    ▼
            Never logged or displayed
```

---

## Performance Considerations

### Async Operations

```
User Action
    │
    ├─ UI Thread ────────► Stays responsive
    │
    └─ Worker Thread ────► Makes API call
            │
            └─► Returns result
                    │
                    └─► Updates UI
```

### Resource Usage

- **Memory**: ~50-100 MB (Python + Tkinter + Streamlit)
- **Network**: On-demand API calls only
- **CPU**: Low (mostly idle, spikes on API calls)
- **Disk**: Minimal (config files, temporary audio)

---

## Deployment Architecture

### Local Deployment (Current)

```
┌─────────────────────────────────────┐
│      User's Computer                │
│                                     │
│  ┌─────────────────────────────┐   │
│  │   Python Application        │   │
│  │   (main_app.py)            │   │
│  │                            │   │
│  │   ┌───────────────────┐   │   │
│  │   │  Streamlit Server │   │   │
│  │   │  (port 8501)      │   │   │
│  │   └───────────────────┘   │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
           │
           │ HTTPS
           ▼
    ┌─────────────┐
    │   Azure     │
    │  Services   │
    └─────────────┘
```

### Potential Cloud Deployment

```
┌─────────────────────────────────────┐
│      Cloud Platform                 │
│      (Azure, AWS, etc.)            │
│                                     │
│  ┌─────────────────────────────┐   │
│  │   Web Server                │   │
│  │   (Streamlit Cloud)        │   │
│  │                            │   │
│  │   ┌───────────────────┐   │   │
│  │   │  Backend API      │   │   │
│  │   │  (FastAPI)        │   │   │
│  │   └───────────────────┘   │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
           │
           │ HTTPS
           ▼
    ┌─────────────┐
    │   Azure     │
    │  Services   │
    └─────────────┘
```

---

## Scalability Considerations

### Current Scale
- Single user application
- Local processing
- Cloud API calls

### Potential Enhancements for Multi-User
1. Database for user data
2. Session management
3. Load balancing
4. Caching layer
5. Message queue
6. Microservices architecture

---

## Technology Stack Summary

### Frontend
- **Tkinter**: Desktop UI
- **Streamlit**: Web UI for financial app

### Backend
- **Python 3.8+**: Core language
- **Requests**: HTTP client

### AI/ML Services
- **Azure OpenAI**: Chat
- **Azure Speech**: TTS/STT
- **Azure Translator**: Translation
- **Google Gemini**: Financial advice
- **DeepSeek**: Financial advice
- **Botpress**: Chatbot

### Data/Visualization
- **Pandas**: Data processing
- **Plotly**: Interactive charts

### External APIs
- **Alpha Vantage**: Stock data
- **Various AI APIs**: Financial suggestions

---

## Extension Points

### Easy to Extend

1. **Add New Tutorial Topics**
   - Edit `ai_tutor.py`
   - Add to `get_tutorial_content()`

2. **Add New Azure Service**
   - Create client class in `azure_services.py`
   - Add to `AzureServicesManager`

3. **Add New UI Features**
   - Modify `main_app.py`
   - Add buttons/panels as needed

4. **Add New Financial Features**
   - Modify `budget_invest_app.py`
   - Streamlit makes it easy

---

## Monitoring and Logging

### Current Logging
- Console output for errors
- Status updates in UI
- No persistent logs

### Recommended for Production
- Structured logging (JSON)
- Log aggregation service
- Error tracking (Sentry)
- Usage analytics
- Performance monitoring

---

## Conclusion

This architecture provides:
✅ Clean separation of concerns
✅ Modular design
✅ Easy to understand
✅ Easy to extend
✅ Secure by design
✅ Well-documented

The dual-panel approach allows users to learn and use simultaneously, creating an excellent educational experience.

---

*Architecture documented on November 12, 2025*
