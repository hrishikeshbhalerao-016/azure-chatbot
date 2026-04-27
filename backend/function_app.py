import azure.functions as func
import logging
import json
from orchestrator import process_chat_request

app = func.FunctionApp()

@app.route(route="chat", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def chat_handler(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing chat request.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
             "Invalid JSON.",
             status_code=400
        )

    messages = req_body.get('messages')
    
    if not messages:
        return func.HttpResponse(
             "Please provide a messages list in the request body.",
             status_code=400
        )

    try:
        # Call the orchestrator
        response_content = process_chat_request(messages)
        
        return func.HttpResponse(
            body=json.dumps({"response": response_content}),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error processing context: {e}")
        return func.HttpResponse(
             f"An error occurred: {str(e)}",
             status_code=500
        )
