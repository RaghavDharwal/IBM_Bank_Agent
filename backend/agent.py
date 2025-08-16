# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# import requests
# from dotenv import load_dotenv
# import sys
# import json

# # --- Load Environment Variables ---
# # This loads the .env file for local development.
# load_dotenv()

# # --- Initialize Flask App ---
# app = Flask(__name__)
# # Enable CORS to allow your frontend to communicate with this backend.
# CORS(app)

# # --- Configuration & Authentication ---
# API_KEY = os.getenv("API_KEY")
# AGENT_ENDPOINT = os.getenv("AGENT_ENDPOINT")
# IAM_ENDPOINT = "https://iam.cloud.ibm.com/identity/token"

# # Check if essential environment variables are set
# if not API_KEY or not AGENT_ENDPOINT:
#     print("FATAL ERROR: API_KEY and AGENT_ENDPOINT must be set in the environment or a .env file.")
#     sys.exit(1)

# def get_iam_token():
#     """
#     Retrieves a temporary IAM access token from IBM Cloud using the API Key.
#     This token is required to authenticate requests to the Watsonx agent.
#     """
#     headers = {"Content-Type": "application/x-www-form-urlencoded"}
#     data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={API_KEY}"
    
#     try:
#         response = requests.post(IAM_ENDPOINT, headers=headers, data=data)
#         response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
#         return response.json().get("access_token")
#     except requests.exceptions.RequestException as e:
#         print(f"Error getting IAM token: {e}")
#         return None

# # --- API Routes ---
# # @app.route('/ask', methods=['POST'])
# # def ask_agent():
# #     """
# #     This endpoint receives a user query, authenticates with IBM,
# #     forwards the query to the agent, and returns the agent's response.
# #     """
# #     # 1. Get a fresh IAM token for this request
# #     # This ensures the token is always valid. For higher performance, you could
# #     # cache the token and refresh it only when it's about to expire.
# #     access_token = get_iam_token()
# #     if not access_token:
# #         return jsonify({"error": "Failed to authenticate with IBM Cloud. Check API Key and server logs."}), 500

# #     # 2. Get the user's query from the incoming request
# #     try:
# #         request_data = request.get_json()
# #         user_query = request_data.get("query")

# #         if not user_query:
# #             return jsonify({"error": "Query field cannot be empty."}), 400
# #     except Exception:
# #         return jsonify({"error": "Invalid request format. JSON body with 'query' key is expected."}), 400

# #     # 3. Prepare and send the request to the IBM Watsonx Agent
# #     agent_headers = {
# #         "Content-Type": "application/json",
# #         "Authorization": f"Bearer {access_token}"
# #     }
    
# #     payload = {
# #         "input": user_query
# #         # Add other parameters like 'conversation_id' if needed by your agent
# #         # "conversation_id": "some-session-id"
# #     }

# #     try:
# #         agent_response = requests.post(AGENT_ENDPOINT, headers=agent_headers, json=payload)
# #         agent_response.raise_for_status() # Raise an exception for bad status codes

# #         response_json = agent_response.json()
# #         # The key for the agent's reply might be 'output' or nested deeper.
# #         # Check your agent's response format. Example: result['output']['generic'][0]['text']
# #         reply = response_json.get("output", "No output received from agent.")
        
# #         return jsonify({"response": reply})

# #     except requests.exceptions.HTTPError as e:
# #         # This catches errors from the agent endpoint (e.g., 400, 404, 500)
# #         return jsonify({
# #             "error": "Failed to fetch response from IBM Agent.",
# #             "status_code": e.response.status_code,
# #             "details": e.response.text
# #         }), e.response.status_code
# #     except Exception as e:
# #         # This catches other errors (e.g., network issues, invalid JSON response)
# #         return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# # # --- Main Execution ---
# # if __name__ == "__main__":
# #     # The app runs on port 5000 by default.
# #     # You can change it with: app.run(debug=True, port=5001)
# #     app.run(debug=True)


# def create_detailed_prompt(form_data):
#     """Creates a detailed prompt for the AI agent from the form data."""
#     try:
#         pd = form_data.get('personalDetails', {})
#         emp = form_data.get('employment', {})
#         ld = form_data.get('loanDetails', {})

#         prompt = f"""
#         Analyze the following loan application to determine eligibility and provide a brief summary.

#         **Applicant Profile:**
#         - **Name:** {pd.get('name', 'N/A')}
#         - **Date of Birth:** {pd.get('dob', 'N/A')}
#         - **Gender:** {pd.get('gender', 'N/A')}
#         - **Marital Status:** {pd.get('maritalStatus', 'N/A')}
#         - **Nationality:** {pd.get('nationality', 'N/A')}
#         - **Contact:** {pd.get('contact', 'N/A')}
#         - **Email:** {pd.get('email', 'N/A')}

#         **Financial Information:**
#         - **Employment Type:** {emp.get('type', 'N/A')}
#         - **Employer/Business Name:** {emp.get('employer', 'N/A')}
#         - **Annual Income (INR):** {emp.get('income', 'N/A')}
#         - **Existing Loans/EMIs:** {emp.get('existingLoans', 'N/A')}
#         - **CIBIL Score:** {ld.get('cibilScore', 'N/A')}

#         **Loan Requirements:**
#         - **Loan Types Requested:** {', '.join(ld.get('types', []))}
#         - **Loan Amount Required (INR):** {ld.get('amount', 'N/A')}
#         - **Loan Tenure:** {ld.get('tenure', 'N/A')} years
#         - **Purpose of Loan:** {ld.get('purpose', 'N/A')}
#         - **Preferred Monthly EMI (INR):** {ld.get('preferredEMI', 'N/A')}

#         Based on these details, please provide a concise analysis of the applicant's eligibility.
#         Start your response with a clear eligibility decision (e.g., "Potentially Eligible", "Likely Ineligible", "More Information Required").
#         Then, briefly explain the key factors supporting your decision.
#         """
#         return prompt
#     except Exception as e:
#         print(f"Error creating prompt: {e}")
#         return "Please analyze this loan application."



# @app.route('/ask', methods=['POST'])
# def ask_agent():
#     """
#     This endpoint receives a user query, authenticates with IBM,
#     forwards the query to the agent, and returns the agent's response.
#     """
#     # 1. Get a fresh IAM token for this request
#     access_token = get_iam_token()
#     if not access_token:
#         return jsonify({"error": "Failed to authenticate with IBM Cloud. Check API Key and server logs."}), 500

#     # 2. Get the user's query from the incoming request
#     # try:
#     #     request_data = request.get_json()
#     #     user_query = request_data.get("query")

#     #     if not user_query:
#     #         return jsonify({"error": "Query field cannot be empty."}), 400
#     # except Exception:
#     #     return jsonify({"error": "Invalid request format. JSON body with 'query' key is expected."}), 400


#     try:
#         form_data = request.get_json()
#         if not form_data:
#             return jsonify({"error": "Invalid request format. No JSON data received."}), 400
#     except Exception:
#         return jsonify({"error": "Invalid request format. Could not parse JSON."}), 400

#     # Create the detailed prompt for the AI
#     user_query = create_detailed_prompt(form_data)




#     # 3. Prepare and send the request to the IBM Watsonx Agent
#     agent_headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {access_token}"
#     }
    
#     # --- THIS IS THE CORRECTED PAYLOAD STRUCTURE ---
#     # Watsonx agents typically expect a "messages" array.
#     payload = {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": user_query
#             }
#         ]
#     }

#     try:
#         agent_response = requests.post(AGENT_ENDPOINT, headers=agent_headers, json=payload)
#         agent_response.raise_for_status() # Raise an exception for bad status codes

#         response_json = agent_response.json()
#         # The key for the agent's reply might be 'output' or nested deeper.
#         # Check your agent's response format. Example: result['output']['generic'][0]['text']

#         # --- DEBUGGING STEP: Print the full response from the agent to the terminal ---
#         # print("------ Full Agent Response ------")
#         # print(json.dumps(response_json, indent=2))
#         # print("---------------------------------")



#         # For the new message format, the response is often in a similar messages structure.
#         # Let's assume the response is in response_json['messages'][1]['content']
#         # reply = "Could not parse agent response." # Default message
#         # if response_json.get("messages") and len(response_json["messages"]) > 1:
#         #     reply = response_json["messages"][1].get("content", reply)



#         # --- FINAL FIX: Correctly parse the agent's response structure ---
#         reply = "Could not parse agent response." # Default message
#         # Use .get() for safe access to prevent errors if the structure is unexpected
#         choices = response_json.get("choices", [])
#         if choices:
#             message = choices[0].get("message", {})
#             reply = message.get("content", reply)

#         # Simple logic to determine eligibility from the agent's text
#         is_eligible = "eligible" in reply.lower() or "potentially" in reply.lower()


#         # return jsonify({"response": reply})
        
#         return jsonify({"response": reply, "is_eligible": is_eligible})    


#     except requests.exceptions.HTTPError as e:
#         # This catches errors from the agent endpoint (e.g., 400, 404, 500)
#         return jsonify({
#             "error": "Failed to fetch response from IBM Agent.",
#             "status_code": e.response.status_code,
#             "details": e.response.text
#         }), e.response.status_code
#     except Exception as e:
#         # This catches other errors (e.g., network issues, invalid JSON response)
#         return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# # --- Main Execution ---
# if __name__ == "__main__":
#     # The app runs on port 5000 by default.
#     # You can change it with: app.run(debug=True, port=5001)
#     app.run(debug=True)