import os
import logging
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# Initialize clients (Lazy initialization for testing without keys first)
def get_openai_client():
    return AzureOpenAI(
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY", ""),
        api_version="2023-05-15"
    )

def get_search_client():
    return SearchClient(
        endpoint=os.environ.get("AZURE_SEARCH_ENDPOINT", ""),
        index_name=os.environ.get("AZURE_SEARCH_INDEX_NAME", ""),
        credential=AzureKeyCredential(os.environ.get("AZURE_SEARCH_API_KEY", ""))
    )

def retrieve_context(query):
    # This retrieves context from Azure AI Search
    try:
        if not os.environ.get("AZURE_SEARCH_ENDPOINT") or os.environ.get("AZURE_SEARCH_ENDPOINT") == "your_search_endpoint":
            return ["(No Azure Search configured. This is a fallback mock context for testing local dev.)"]
        
        search_client = get_search_client()
        # Mocking vector query, in reality you pass generate_embedding(query)
        # However, hybrid search often uses simply text search if vectors aren't available
        results = search_client.search(
            search_text=query,
            top=3
        )
        context = [doc['content'] for doc in results if 'content' in doc]
        return context
    except Exception as e:
        logging.warning(f"Failed to retrieve context: {e}")
        return ["(Error retrieving context or search not configured properly.)"]

def process_chat_request(messages):
    """
    RAG pattern implementation:
    1. Extract the latest user query.
    2. Retrieve relevant context from Azure AI Search.
    3. Construct a system prompt with the context.
    4. Call Azure OpenAI to generate a response.
    """
    if not messages:
        return "No messages provided."
    
    latest_user_message = next((msg['content'] for msg in reversed(messages) if msg['role'] == 'user'), "")
    
    # 1. Retrieve Context
    context_docs = retrieve_context(latest_user_message)
    context_text = "\n\n".join(context_docs)
    
    # 2. Augment prompt
    system_prompt = {
        "role": "system",
        "content": f"You are a helpful AI assistant. Use the following context to answer the user's question. If the answer is not in the context, do your best to answer based on your knowledge, but indicate that you could not find specific references.\n\nContext:\n{context_text}"
    }
    
    augmented_messages = [system_prompt] + messages
    
    # 3. Call Azure OpenAI
    try:
        if not os.environ.get("AZURE_OPENAI_ENDPOINT") or os.environ.get("AZURE_OPENAI_ENDPOINT") == "your_openai_endpoint":
             # Fallback if OpenAI is not configured
             return f"[Mock Response] Based on the context ({context_text}), here is your answer to: {latest_user_message}"

        client = get_openai_client()
        deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo")
        
        response = client.chat.completions.create(
            model=deployment_name,
            messages=augmented_messages,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logging.error(f"OpenAI error: {e}")
        return f"An error occurred while generating a response from OpenAI: {str(e)}"
