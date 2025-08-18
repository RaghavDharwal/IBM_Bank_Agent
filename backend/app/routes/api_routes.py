# backend/app/routes/api_routes.py

from flask import Blueprint, request, jsonify, session, current_app
import requests

# Import functions from our new service and utility modules
from ..services.watson_service import get_iam_token
from ..utils.csv_handler import save_chat_log

# Create a Blueprint. This is like a mini-app for our API routes.
api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/ask', methods=['POST'])
def ask_agent():
    """
    This endpoint receives a user query, authenticates with IBM,
    forwards the query to the agent, and returns the agent's response.
    """
    
    # Check if IBM credentials are provided in the config
    ibm_enabled = current_app.config['API_KEY'] and current_app.config['AGENT_ENDPOINT']

    if not ibm_enabled:
        request_data = request.get_json()
        user_query = request_data.get("query", "")
        
        # Provide a mock response for testing
        mock_response = f"Thank you for your message: '{user_query}'. This is a demo response as IBM Watson is not configured."
        
        save_chat_log(user_query, mock_response, session.get('session_id'))
        return jsonify({"response": mock_response})
    
    # 1. Get a fresh IAM token for this request
    access_token = get_iam_token()
    if not access_token:
        error_response = "Failed to authenticate with IBM Cloud. Check API Key and server logs."
        save_chat_log(request.get_json().get('query', ''), error_response)
        return jsonify({"error": error_response}), 500

    # 2. Get the user's query from the incoming request
    try:
        request_data = request.get_json()
        user_query = request_data.get("query")

        if not user_query:
            return jsonify({"error": "Query field cannot be empty."}), 400
    except Exception:
        return jsonify({"error": "Invalid request format. JSON body with 'query' key is expected."}), 400

    # 3. Prepare and send the request to the IBM Watsonx Agent
    agent_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    payload = {
        "messages": [
            {"role": "user", "content": user_query}
        ]
    }

    try:
        agent_endpoint = current_app.config['AGENT_ENDPOINT']
        agent_response = requests.post(agent_endpoint, headers=agent_headers, json=payload)
        agent_response.raise_for_status()

        response_json = agent_response.json()
        
        # Correctly parse the agent's response structure
        reply = "Could not parse agent response."
        choices = response_json.get("choices", [])
        if choices:
            message = choices[0].get("message", {})
            reply = message.get("content", reply)

        # Save the chat interaction to CSV
        save_chat_log(user_query, reply, session.get('session_id'))
        
        return jsonify({"response": reply})

    except requests.exceptions.HTTPError as e:
        error_response = f"Failed to fetch response from IBM Agent. Status: {e.response.status_code}"
        save_chat_log(user_query, error_response)
        return jsonify({
            "error": "Failed to fetch response from IBM Agent.",
            "status_code": e.response.status_code,
            "details": e.response.text
        }), e.response.status_code
    except Exception as e:
        error_response = f"An unexpected error occurred: {str(e)}"
        save_chat_log(user_query, error_response)
        return jsonify({"error": error_response}), 500