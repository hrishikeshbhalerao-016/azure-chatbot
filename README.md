# Azure AI Chatbot

A full-stack RAG (Retrieval-Augmented Generation) chatbot application leveraging Streamlit for the frontend, Azure Functions for orchestration, and Azure AI Search + Azure OpenAI for conversational intelligence.

## Architecture
- **Frontend**: Streamlit application with chat interface, chat history, and loading indicators.
- **Backend**: Python Azure Functions instance providing an API endpoint (`/api/chat`).
- **Orchestration**:
  1. Captures user query from frontend.
  2. Queries Vector store / Azure AI Search for relevant context (Hybrid/Semantic search context retrieval).
  3. Augments an Azure OpenAI payload with fetched context (RAG pattern).
  4. Returns the LLM response to the frontend.

## Prerequisites
- Python 3.9+
- Azure Functions Core Tools (`func`)
- An Azure Subscription with Azure OpenAI and Azure AI Search configured.

## Setup Instructions

### 1. Setup Backend
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a Virtual Environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Mac/Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Update `local.settings.json` with your real Azure keys:
   - `AZURE_OPENAI_ENDPOINT`
   - `AZURE_OPENAI_API_KEY`
   - `AZURE_OPENAI_DEPLOYMENT_NAME`
   - `AZURE_SEARCH_ENDPOINT`
   - `AZURE_SEARCH_API_KEY`
   - `AZURE_SEARCH_INDEX_NAME`
5. Run the function app:
   ```bash
   func start
   ```

### 2. Setup Frontend
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Create and activate a Virtual Environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Update `.env` if the backend is not running on `http://localhost:7071/api/chat`.
5. Run Streamlit:
   ```bash
   streamlit run app.py
   ```

## Testing Locally
Even if you do not have your Azure keys right away, you can run the app. The backend orchestrator handles missing keys gracefully by returning mock responses so you can see the end-to-end integration flow.
