import os
import requests
import logging

def send_chat_request(messages):
    api_url = os.environ.get("BACKEND_API_URL", "http://localhost:7071/api/chat")
    try:
        response = requests.post(
            api_url,
            json={"messages": messages},
            timeout=60 # 60 seconds timeout because LLMs can be slow
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "No response content received.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error calling backend API: {e}")
        return f"Error communicating with backend: {e}"
