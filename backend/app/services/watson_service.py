# backend/app/services/watson_service.py file 

import requests
from flask import current_app

# We need to import the helper functions from our new utils folder
from ..utils.helpers import calculate_age_from_dob
# The rule-based function is our fallback if the AI isn't available
from ..utils.helpers import rule_based_eligibility_assessment


def get_iam_token():
    """
    Retrieves a temporary IAM access token from IBM Cloud using the API Key.
    This token is required to authenticate requests to the Watsonx agent.
    """
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    # Use current_app.config to get the API Key from our central config file
    api_key = current_app.config['API_KEY']
    iam_endpoint = current_app.config['IAM_ENDPOINT']
    
    data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={api_key}"
    
    try:
        response = requests.post(iam_endpoint, headers=headers, data=data)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"Error getting IAM token: {e}")
        return None

def parse_watson_eligibility_response(watson_response):
    """Parse Watson AI response into structured format"""
    try:
        lines = watson_response.strip().split('\n')
        eligibility_data = {
            'status': 'PENDING_REVIEW',
            'reason': 'Assessment completed',
            'documents': 'Identity Proof, Income Proof, Address Proof',
            'recommendations': 'Standard documentation required'
        }
        
        for line in lines:
            if line.startswith('ELIGIBILITY:'):
                eligibility_data['status'] = line.replace('ELIGIBILITY:', '').strip()
            elif line.startswith('REASON:'):
                eligibility_data['reason'] = line.replace('REASON:', '').strip()
            elif line.startswith('DOCUMENTS:'):
                eligibility_data['documents'] = line.replace('DOCUMENTS:', '').strip()
            elif line.startswith('RECOMMENDATIONS:'):
                eligibility_data['recommendations'] = line.replace('RECOMMENDATIONS:', '').strip()
        
        return eligibility_data
    except Exception as e:
        print(f"Error parsing Watson response: {e}")
        return {
            'status': 'PENDING_REVIEW',
            'reason': 'Automated assessment completed',
            'documents': 'Identity Proof, Income Proof, Address Proof',
            'recommendations': 'Please submit required documents'
        }

def assess_loan_eligibility_with_watson(loan_data):
    """Use Watson AI to assess loan eligibility based on comprehensive data"""
    try:
        # Prepare eligibility assessment prompt for Watson AI
        eligibility_prompt = f"""
        As a banking loan officer AI, assess the loan eligibility for the following applicant and provide detailed analysis:

        APPLICANT DETAILS:
        - Full Name: {loan_data.get('full-name', 'N/A')}
        - Age: {calculate_age_from_dob(loan_data.get('date-of-birth', ''))} years
        - Gender: {loan_data.get('gender', 'N/A')}
        - Marital Status: {loan_data.get('marital-status', 'N/A')}
        - Nationality: {loan_data.get('nationality', 'N/A')}
        - Employment Type: {loan_data.get('employment-type', 'N/A')}
        - Employer/Business: {loan_data.get('employer-name', 'N/A')}
        - Annual Income: ₹{loan_data.get('annual-income', 'N/A')}
        - Existing Loans/EMIs: {loan_data.get('existing-loans', 'None')}
        - CIBIL Score: {loan_data.get('cibil-score', 'N/A')}

        LOAN REQUEST:
        - Loan Type: {loan_data.get('loan-type', 'N/A')}
        - Loan Amount: ₹{loan_data.get('loan-amount', 'N/A')}
        - Loan Tenure: {loan_data.get('loan-tenure', 'N/A')} years
        - Purpose: {loan_data.get('loan-purpose', 'N/A')}
        - Preferred EMI: ₹{loan_data.get('preferred-emi', 'N/A')}

        Please provide:
        1. ELIGIBILITY STATUS: APPROVED/CONDITIONALLY_APPROVED/REJECTED
        2. DETAILED REASON: Explain the decision factors
        3. REQUIRED DOCUMENTS: List specific documents needed if eligible
        4. RECOMMENDATIONS: Suggest improvements if rejected or conditions if conditional

        Format your response as:
        ELIGIBILITY: [status]
        REASON: [detailed explanation]
        DOCUMENTS: [comma-separated list]
        RECOMMENDATIONS: [specific advice]
        """
        
        # Check if IBM credentials are configured in our central config
        if current_app.config['API_KEY'] and current_app.config['AGENT_ENDPOINT']:
            access_token = get_iam_token()
            if access_token:
                agent_headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}"
                }
                
                payload = {
                    "messages": [
                        {"role": "user", "content": eligibility_prompt}
                    ]
                }

                try:
                    agent_response = requests.post(current_app.config['AGENT_ENDPOINT'], headers=agent_headers, json=payload)
                    agent_response.raise_for_status()
                    response_json = agent_response.json()
                    
                    choices = response_json.get("choices", [])
                    if choices:
                        message = choices[0].get("message", {})
                        watson_response = message.get("content", "")
                        return parse_watson_eligibility_response(watson_response)
                
                except Exception as e:
                    print(f"Watson AI request failed: {e}")
                    # Fall back to rule-based assessment
                    return rule_based_eligibility_assessment(loan_data)
        
        # Fallback to rule-based assessment when Watson is not available or configured
        return rule_based_eligibility_assessment(loan_data)
        
    except Exception as e:
        print(f"Eligibility assessment error: {e}")
        return rule_based_eligibility_assessment(loan_data)