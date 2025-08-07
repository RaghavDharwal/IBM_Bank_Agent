from flask import Flask, request, jsonify, session, redirect, url_for, render_template_string
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv
import sys
import json
import csv
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import send_from_directory
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import ssl
# --- Load Environment Variables ---
# This loads the .env file for local development.
load_dotenv()

# --- Helper Functions ---
def format_currency(amount, currency_symbol="₹"):
    """Safely format currency amounts, handling non-numeric values"""
    if amount is None or amount == '' or str(amount).lower() in ['n/a', 'na', 'none']:
        return 'N/A'
    
    try:
        # Convert to string and remove any currency symbols or spaces
        amount_str = str(amount).replace(currency_symbol, '').replace(',', '').strip()
        
        # Check if it's a valid number
        if amount_str.replace('.', '').isdigit():
            amount_num = float(amount_str)
            return f"{currency_symbol}{int(amount_num):,}"
        else:
            return 'N/A'
    except (ValueError, TypeError):
        return 'N/A'

# --- Initialize Flask App ---
app = Flask(__name__)
# Enable CORS to allow your frontend to communicate with this backend.
CORS(app)
app.secret_key = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")

# --- CSV File Paths ---
CSV_DIR = "data"
STAFF_CSV = os.path.join(CSV_DIR, "staff.csv")
LOAN_APPLICATIONS_CSV = os.path.join(CSV_DIR, "loan_applications.csv")
COMPREHENSIVE_LOANS_CSV = os.path.join(CSV_DIR, "comprehensive_loans.csv")
USERS_CSV = os.path.join(CSV_DIR, "users.csv")
CHAT_LOGS_CSV = os.path.join(CSV_DIR, "chat_logs.csv")

# Create data directory if it doesn't exist
os.makedirs(CSV_DIR, exist_ok=True)

# --- Configuration & Authentication ---
API_KEY = os.getenv("API_KEY")
AGENT_ENDPOINT = os.getenv("AGENT_ENDPOINT")
IAM_ENDPOINT = "https://iam.cloud.ibm.com/identity/token"

# --- SMTP Email Configuration ---
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USERNAME)
FROM_NAME = os.getenv("FROM_NAME", "AI Banking Portal")

# Check if email configuration is available
EMAIL_ENABLED = bool(SMTP_USERNAME and SMTP_PASSWORD)
if not EMAIL_ENABLED:
    print("WARNING: SMTP credentials not configured. Email notifications will be logged only.")
    print("Set SMTP_USERNAME and SMTP_PASSWORD in .env file for actual email sending.")

# Check if essential environment variables are set (warn but don't exit for UI testing)
IBM_ENABLED = bool(API_KEY and AGENT_ENDPOINT)
if not IBM_ENABLED:
    print("WARNING: API_KEY and AGENT_ENDPOINT not set. IBM Watson features will be disabled.")
    print("Only UI testing and CSV functionality will work.")

def get_iam_token():
    """
    Retrieves a temporary IAM access token from IBM Cloud using the API Key.
    This token is required to authenticate requests to the Watsonx agent.
    """
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={API_KEY}"
    
    try:
        response = requests.post(IAM_ENDPOINT, headers=headers, data=data)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"Error getting IAM token: {e}")
        return None

# --- CSV Helper Functions ---
def initialize_csv_files():
    """Initialize CSV files with headers if they don't exist"""
    
    # Initialize staff.csv
    if not os.path.exists(STAFF_CSV):
        with open(STAFF_CSV, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'username', 'password_hash', 'email', 'role', 'created_at'])
            # Add default admin user
            admin_id = str(uuid.uuid4())
            admin_password_hash = generate_password_hash('admin123')
            writer.writerow([admin_id, 'admin', admin_password_hash, 'singhishant37@gmail.com', 'admin', datetime.now().isoformat()])
    
    # Initialize users.csv
    if not os.path.exists(USERS_CSV):
        with open(USERS_CSV, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'name', 'email', 'phone', 'password_hash', 'created_at'])
    
    # Initialize loan_applications.csv (simple form)
    if not os.path.exists(LOAN_APPLICATIONS_CSV):
        with open(LOAN_APPLICATIONS_CSV, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'application_id', 'first_name', 'last_name', 'email', 'phone', 
                'loan_type', 'loan_amount', 'annual_income', 'employment_status', 
                'purpose', 'status', 'created_at'
            ])
    
    # Initialize comprehensive_loans.csv (detailed form)
    if not os.path.exists(COMPREHENSIVE_LOANS_CSV):
        with open(COMPREHENSIVE_LOANS_CSV, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'application_id', 'user_email', 'full_name', 'date_of_birth', 'gender', 
                'marital_status', 'nationality', 'contact_number', 'employment_type', 
                'employer_name', 'annual_income', 'existing_loans', 'loan_type', 
                'loan_amount', 'loan_tenure', 'loan_purpose', 'preferred_emi', 
                'cibil_score', 'status', 'eligibility_status', 'eligibility_reason',
                'required_documents', 'uploaded_documents', 'admin_notes', 
                'verification_status', 'created_at', 'updated_at'
            ])
    
    # Initialize document_uploads.csv
    documents_csv = os.path.join(CSV_DIR, "document_uploads.csv")
    if not os.path.exists(documents_csv):
        with open(documents_csv, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'id', 'application_id', 'user_email', 'document_type', 
                'file_name', 'file_path', 'upload_status', 'verified', 
                'admin_comments', 'uploaded_at'
            ])
    
    # Initialize user_alerts.csv
    alerts_csv = os.path.join(CSV_DIR, "user_alerts.csv")
    if not os.path.exists(alerts_csv):
        with open(alerts_csv, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'id', 'user_email', 'application_id', 'alert_type', 
                'title', 'message', 'priority', 'read', 'created_at'
            ])
    
    # Initialize chat_logs.csv
    if not os.path.exists(CHAT_LOGS_CSV):
        with open(CHAT_LOGS_CSV, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'user_message', 'bot_response', 'timestamp', 'session_id'])

def verify_staff_credentials(username, password):
    """Verify staff login credentials"""
    try:
        with open(STAFF_CSV, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username:
                    if check_password_hash(row['password_hash'], password):
                        return {'success': True, 'user': row}
                    else:
                        return {'success': False, 'error': 'Invalid password'}
            return {'success': False, 'error': 'User not found'}
    except FileNotFoundError:
        return {'success': False, 'error': 'Staff database not found'}

def save_loan_application(loan_data):
    """Save loan application to CSV"""
    try:
        application_id = str(uuid.uuid4())[:8].upper()
        
        with open(LOAN_APPLICATIONS_CSV, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                application_id,
                loan_data.get('firstName', ''),
                loan_data.get('lastName', ''),
                loan_data.get('email', ''),
                loan_data.get('phone', ''),
                loan_data.get('loanType', ''),
                loan_data.get('loanAmount', ''),
                loan_data.get('annualIncome', ''),
                loan_data.get('employmentStatus', ''),
                loan_data.get('purpose', ''),
                'pending',
                datetime.now().isoformat()
            ])
        
        return {'success': True, 'application_id': application_id}
    except Exception as e:
        print(f"Error saving loan application: {e}")
        return {'success': False, 'error': str(e)}

def save_chat_log(user_message, bot_response, session_id=None):
    """Save chat interaction to CSV"""
    try:
        chat_id = str(uuid.uuid4())
        session_id = session_id or str(uuid.uuid4())
        
        with open(CHAT_LOGS_CSV, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                chat_id,
                user_message,
                bot_response,
                datetime.now().isoformat(),
                session_id
            ])
    except Exception as e:
        print(f"Error saving chat log: {e}")

def get_all_loan_applications():
    """Retrieve all loan applications from both old and new CSV files"""
    try:
        applications = []
        
        # Read old format loan applications
        try:
            with open(LOAN_APPLICATIONS_CSV, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Add source indicator
                    row['source'] = 'basic'
                    applications.append(row)
        except FileNotFoundError:
            pass
        
        # Read comprehensive loan applications (new format)
        try:
            with open(COMPREHENSIVE_LOANS_CSV, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Add source indicator and normalize field names for compatibility
                    row['source'] = 'comprehensive'
                    # Map comprehensive fields to admin dashboard expected fields
                    if 'full_name' in row and row['full_name']:
                        # Split full name if available
                        name_parts = row['full_name'].split(' ', 1)
                        row['first_name'] = name_parts[0] if len(name_parts) > 0 else ''
                        row['last_name'] = name_parts[1] if len(name_parts) > 1 else ''
                    else:
                        row['first_name'] = row.get('first_name', '')
                        row['last_name'] = row.get('last_name', '')
                    
                    # Map email field
                    row['email'] = row.get('user_email', row.get('email', ''))
                    
                    # Ensure other required fields exist
                    row['phone'] = row.get('contact_number', row.get('phone', ''))
                    
                    applications.append(row)
        except FileNotFoundError:
            pass
        
        # Sort by creation date (newest first)
        applications.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return applications
    except Exception as e:
        print(f"Error reading loan applications: {e}")
        return []

def get_chat_logs(limit=100):
    """Retrieve recent chat logs"""
    try:
        logs = []
        with open(CHAT_LOGS_CSV, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                logs.append(row)
        return logs[-limit:]  # Return last N logs
    except FileNotFoundError:
        return []

def register_user(user_data):
    """Register a new user"""
    try:
        # Check if user already exists
        with open(USERS_CSV, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['email'] == user_data.get('email'):
                    return {'success': False, 'error': 'Email already registered'}
        
        # Add new user
        user_id = str(uuid.uuid4())
        password_hash = generate_password_hash(user_data.get('password'))
        
        with open(USERS_CSV, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                user_id,
                user_data.get('name'),
                user_data.get('email'),
                user_data.get('phone'),
                password_hash,
                datetime.now().isoformat()
            ])
        
        return {'success': True, 'message': 'User registered successfully'}
    except Exception as e:
        print(f"Error registering user: {e}")
        return {'success': False, 'error': str(e)}

def verify_user_credentials(email, password):
    """Verify user login credentials"""
    try:
        with open(USERS_CSV, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['email'] == email:
                    if check_password_hash(row['password_hash'], password):
                        return {
                            'success': True, 
                            'user': {
                                'id': row['id'],
                                'name': row['name'],
                                'email': row['email'],
                                'phone': row['phone']
                            }
                        }
                    else:
                        return {'success': False, 'error': 'Invalid password'}
            return {'success': False, 'error': 'Email not found'}
    except FileNotFoundError:
        return {'success': False, 'error': 'User database not found'}

def save_comprehensive_loan_application(loan_data):
    """Save comprehensive loan application to CSV with Watson AI eligibility assessment"""
    try:
        application_id = str(uuid.uuid4())[:8].upper()
        print(f"🔄 Processing loan application {application_id} for {loan_data.get('userEmail', 'unknown user')}")
        
        # Get Watson AI eligibility assessment
        eligibility_assessment = assess_loan_eligibility_with_watson(loan_data)
        print(f"✅ Eligibility assessment completed for {application_id}: {eligibility_assessment['status']}")
        
        print(f"💾 Writing application {application_id} to CSV file {COMPREHENSIVE_LOANS_CSV}")
        with open(COMPREHENSIVE_LOANS_CSV, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                application_id,
                loan_data.get('userEmail', ''),
                loan_data.get('full-name', ''),
                loan_data.get('date-of-birth', ''),
                loan_data.get('gender', ''),
                loan_data.get('marital-status', ''),
                loan_data.get('nationality', ''),
                loan_data.get('contact-number', ''),
                loan_data.get('employment-type', ''),
                loan_data.get('employer-name', ''),
                loan_data.get('annual-income', ''),
                loan_data.get('existing-loans', ''),
                loan_data.get('loan-type', ''),
                loan_data.get('loan-amount', ''),
                loan_data.get('loan-tenure', ''),
                loan_data.get('loan-purpose', ''),
                loan_data.get('preferred-emi', ''),
                loan_data.get('cibil-score', ''),
                'eligibility_assessed',  # status
                eligibility_assessment['status'],  # eligibility_status
                eligibility_assessment['reason'],  # eligibility_reason
                eligibility_assessment['documents'],  # required_documents
                '',  # uploaded_documents (empty initially)
                eligibility_assessment['recommendations'],  # admin_notes
                'pending',  # verification_status
                datetime.now().isoformat(),  # created_at
                datetime.now().isoformat()   # updated_at
            ])
        
        print(f"✅ Application {application_id} saved successfully to {COMPREHENSIVE_LOANS_CSV}")
        
        # Send eligibility notification email
        user_email = loan_data.get('userEmail', '')
        user_name = loan_data.get('full-name', 'Applicant')
        
        if eligibility_assessment['status'] == 'APPROVED':
            # Create alert for document submission
            create_user_alert(
                user_email, application_id, 'document_required',
                'Documents Required - Loan Application',
                f'Congratulations! Your loan application {application_id} is pre-approved. Please submit the required documents to complete the process.',
                'high'
            )
            
            email_subject = f"🎉 Loan Pre-Approval - Application {application_id}"            
            email_message = f"""Dear {user_name},

Great news! Your loan application has been PRE-APPROVED by our Watson AI assessment system.

Application Details:
• Application ID: {application_id}
• Loan Type: {loan_data.get('loan-type', 'N/A')}
• Loan Amount: {format_currency(loan_data.get('loan-amount', 'N/A'))}
• Assessment Status: APPROVED

Next Steps:
1. Submit the required documents through your dashboard
2. Wait for our team to verify your documents
3. Receive final approval after document verification

Required Documents:
{eligibility_assessment['documents']}

Please log in to your account and upload these documents to proceed with your loan application.

This pre-approval is valid for 30 days from the date of this email.

Best regards,
AI Banking Portal Team"""

            html_content = create_html_email_template(
                title="Loan Pre-Approval Success!",
                content=f"""Your loan application for {format_currency(loan_data.get('loan-amount', 'N/A'))} has been pre-approved by Watson AI.

Application ID: {application_id}
Loan Type: {loan_data.get('loan-type', 'N/A')}

Required Documents:
{eligibility_assessment['documents']}

Please upload the required documents through your dashboard to complete the process.""",
                cta_text="Upload Documents Now",
                cta_link="http://127.0.0.1:5001/",
                alert_type="success"
            )
            
        elif eligibility_assessment['status'] == 'CONDITIONALLY_APPROVED':
            create_user_alert(
                user_email, application_id, 'conditional_approval',
                'Conditional Approval - Additional Requirements',
                f'Your loan application {application_id} is conditionally approved. Please review requirements and submit documents.',
                'medium'
            )
            
            email_subject = f"⚠️ Conditional Approval - Application {application_id}"
            email_message = f"""Dear {user_name},

Your loan application has received CONDITIONAL APPROVAL from our Watson AI assessment system.

Application Details:
• Application ID: {application_id}
• Loan Type: {loan_data.get('loan-type', 'N/A')}
• Loan Amount: {format_currency(loan_data.get('loan-amount', 'N/A'))}
• Assessment Status: CONDITIONALLY APPROVED

Assessment Details:
Reason: {eligibility_assessment['reason']}

Required Documents:
{eligibility_assessment['documents']}

Recommendations:
{eligibility_assessment['recommendations']}

Please submit the required documents and fulfill the conditions mentioned above to proceed with your loan application.

Best regards,
AI Banking Portal Team"""

            html_content = create_html_email_template(
                title="Conditional Loan Approval",
                content=f"""Your loan application requires additional documentation and review.

Application ID: {application_id}
Status: CONDITIONALLY APPROVED

Assessment Reason:
{eligibility_assessment['reason']}

Required Documents:
{eligibility_assessment['documents']}

Recommendations:
{eligibility_assessment['recommendations']}""",
                cta_text="Complete Requirements",
                cta_link="http://127.0.0.1:5001/",
                alert_type="warning"
            )
            
        else:  # REJECTED
            create_user_alert(
                user_email, application_id, 'rejection',
                'Loan Application Not Approved',
                f'Unfortunately, your loan application {application_id} does not meet current eligibility criteria. Please review the reasons and consider reapplying.',
                'high'
            )
            
            email_subject = f"📋 Loan Application Status - Application {application_id}"
            email_message = f"""Dear {user_name},

Thank you for your interest in our loan services. After careful review by our Watson AI system, your loan application does not currently meet our eligibility criteria.

Application Details:
• Application ID: {application_id}
• Loan Type: {loan_data.get('loan-type', 'N/A')}
• Loan Amount: {format_currency(loan_data.get('loan-amount', 'N/A'))}
• Assessment Status: NOT APPROVED

Assessment Details:
Reason: {eligibility_assessment['reason']}

Recommendations for Future Applications:
{eligibility_assessment['recommendations']}

You may reapply after addressing these requirements. Our customer service team is available to help you improve your eligibility.

We appreciate your interest in our services and look forward to serving you in the future.

Best regards,
AI Banking Portal Team"""

            html_content = create_html_email_template(
                title="Loan Application Status Update",
                content=f"""We have carefully reviewed your loan application using Watson AI technology.

Application ID: {application_id}
Status: NOT APPROVED

Assessment Reason:
{eligibility_assessment['reason']}

Improvement Recommendations:
{eligibility_assessment['recommendations']}

You may reapply once you have addressed these requirements.""",
                cta_text="Learn More About Requirements",
                cta_link="http://127.0.0.1:5001/",
                alert_type="danger"
            )
        
        # Send email notification with HTML content
        send_email_notification(user_email, email_subject, email_message, 'application_status', html_content)
        
        return {
            'success': True, 
            'application_id': application_id,
            'eligibility_status': eligibility_assessment['status'],
            'eligibility_reason': eligibility_assessment['reason'],
            'required_documents': eligibility_assessment['documents'],
            'next_step': 'document_upload' if eligibility_assessment['status'] in ['APPROVED', 'CONDITIONALLY_APPROVED'] else 'eligibility_review'
        }
        
    except Exception as e:
        print(f"Error saving comprehensive loan application: {e}")
        return {'success': False, 'error': str(e)}

def get_user_applications(user_email):
    """Get all loan applications for a specific user"""
    try:
        applications = []
        
        # Get simple applications
        try:
            with open(LOAN_APPLICATIONS_CSV, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['email'] == user_email:
                        applications.append(row)
        except FileNotFoundError:
            pass
        
        # Get comprehensive applications
        try:
            with open(COMPREHENSIVE_LOANS_CSV, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['user_email'] == user_email:
                        # Convert comprehensive loan format to simple format for consistency
                        applications.append({
                            'application_id': row['application_id'],
                            'loan_type': row['loan_type'],
                            'loan_amount': row['loan_amount'],
                            'status': row['status'],
                            'created_at': row['created_at'],
                            'eligibility_status': row.get('eligibility_status', ''),
                            'eligibility_reason': row.get('eligibility_reason', ''),
                            'required_documents': row.get('required_documents', ''),
                            'admin_notes': row.get('admin_notes', '')
                        })
        except FileNotFoundError:
            pass
        
        return applications
    except Exception as e:
        print(f"Error getting user applications: {e}")
        return []

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

        if IBM_ENABLED:
            # Get Watson AI assessment
            access_token = get_iam_token()
            if access_token:
                agent_headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}"
                }
                
                payload = {
                    "messages": [
                        {
                            "role": "user",
                            "content": eligibility_prompt
                        }
                    ]
                }

                try:
                    agent_response = requests.post(AGENT_ENDPOINT, headers=agent_headers, json=payload)
                    agent_response.raise_for_status()
                    response_json = agent_response.json()
                    
                    choices = response_json.get("choices", [])
                    if choices:
                        message = choices[0].get("message", {})
                        watson_response = message.get("content", "")
                        
                        # Parse Watson response
                        return parse_watson_eligibility_response(watson_response)
                
                except Exception as e:
                    print(f"Watson AI request failed: {e}")
                    # Fall back to rule-based assessment
                    return rule_based_eligibility_assessment(loan_data)
        
        # Fallback to rule-based assessment when Watson is not available
        return rule_based_eligibility_assessment(loan_data)
        
    except Exception as e:
        print(f"Eligibility assessment error: {e}")
        return rule_based_eligibility_assessment(loan_data)

def calculate_age_from_dob(dob_str):
    """Calculate age from date of birth string"""
    try:
        if not dob_str:
            return "Unknown"
        
        from datetime import datetime
        dob = datetime.strptime(dob_str, '%Y-%m-%d')
        today = datetime.now()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    except:
        return "Unknown"

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

def rule_based_eligibility_assessment(loan_data):
    """Rule-based eligibility assessment when Watson AI is not available"""
    try:
        annual_income = float(loan_data.get('annual-income', 0))
        loan_amount = float(loan_data.get('loan-amount', 0))
        cibil_score = int(loan_data.get('cibil-score', 0)) if loan_data.get('cibil-score', '').isdigit() else 0
        age = calculate_age_from_dob(loan_data.get('date-of-birth', ''))
        
        # Basic eligibility rules
        reasons = []
        status = 'APPROVED'
        
        # Age check
        if isinstance(age, int):
            if age < 21:
                reasons.append('Applicant below minimum age of 21 years')
                status = 'REJECTED'
            elif age > 65:
                reasons.append('Applicant above maximum age of 65 years')
                status = 'REJECTED'
        
        # Income check
        if annual_income < 300000:  # Minimum 3 LPA
            reasons.append('Annual income below minimum requirement of ₹3,00,000')
            status = 'REJECTED'
        
        # Loan amount to income ratio
        if annual_income > 0 and (loan_amount / annual_income) > 5:
            reasons.append('Loan amount exceeds 5 times annual income')
            status = 'CONDITIONALLY_APPROVED'
        
        # CIBIL score check
        if cibil_score < 650:
            reasons.append('CIBIL score below 650')
            if cibil_score < 550:
                status = 'REJECTED'
            else:
                status = 'CONDITIONALLY_APPROVED'
        
        # Determine documents based on loan type and employment
        documents = []
        loan_type = loan_data.get('loan-type', '').lower()
        employment_type = loan_data.get('employment-type', '').lower()
        
        # Common documents
        documents.extend(['Aadhaar Card', 'PAN Card', 'Passport Size Photos', 'Bank Statements (6 months)'])
        
        # Employment specific documents
        if 'salaried' in employment_type:
            documents.extend(['Salary Slips (3 months)', 'Employment Certificate', 'Form 16'])
        else:
            documents.extend(['Business Registration', 'ITR (2 years)', 'Profit & Loss Statement', 'Balance Sheet'])
        
        # Loan type specific documents
        if 'home' in loan_type:
            documents.extend(['Property Documents', 'Sale Agreement', 'Approved Building Plan'])
        elif 'car' in loan_type:
            documents.extend(['Vehicle Quotation', 'Insurance Details'])
        elif 'education' in loan_type:
            documents.extend(['Admission Letter', 'Fee Structure', 'Academic Records'])
        
        # Prepare recommendations
        recommendations = []
        if status == 'REJECTED':
            recommendations.append('Improve CIBIL score and reapply after 6 months')
            recommendations.append('Consider applying for a smaller loan amount')
        elif status == 'CONDITIONALLY_APPROVED':
            recommendations.append('Additional verification required')
            recommendations.append('Co-applicant may be required')
        else:
            recommendations.append('Please submit all required documents for final approval')
        
        return {
            'status': status,
            'reason': '; '.join(reasons) if reasons else 'All eligibility criteria met',
            'documents': ', '.join(documents),
            'recommendations': '; '.join(recommendations)
        }
        
    except Exception as e:
        print(f"Rule-based assessment error: {e}")
        return {
            'status': 'PENDING_REVIEW',
            'reason': 'Manual review required due to assessment error',
            'documents': 'Identity Proof, Income Proof, Address Proof',
            'recommendations': 'Please contact bank for manual assessment'
        }

def send_email_notification(to_email, subject, message, notification_type='info', html_content=None):
    """Send email notification using SMTP"""
    try:
        if not EMAIL_ENABLED:
            # Log email content when SMTP is not configured
            print(f"\n{'='*60}")
            print(f"EMAIL NOTIFICATION [{notification_type.upper()}]")
            print(f"{'='*60}")
            print(f"To: {to_email}")
            print(f"From: {FROM_NAME} <{FROM_EMAIL}>")
            print(f"Subject: {subject}")
            print(f"{'='*60}")
            print(f"Message:\n{message}")
            if html_content:
                print(f"\nHTML Content:\n{html_content}")
            print(f"{'='*60}\n")
            
            # Save notification to CSV for tracking
            save_notification_log(to_email, subject, message, notification_type)
            return True

        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{FROM_NAME} <{FROM_EMAIL}>"
        msg['To'] = to_email
        msg['Subject'] = subject

        # Create plain text part
        text_part = MIMEText(message, 'plain', 'utf-8')
        msg.attach(text_part)

        # Create HTML part if provided
        if html_content:
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
        else:
            # Create a basic HTML version from plain text
            html_content = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 30px;">
                        <h1 style="margin: 0; font-size: 24px;">🏦 {FROM_NAME}</h1>
                    </div>
                    
                    <div style="background: #f8f9fa; padding: 30px; border-radius: 10px; border-left: 4px solid #667eea;">
                        <h2 style="color: #495057; margin-top: 0;">{subject}</h2>
                        <div style="white-space: pre-line; font-size: 16px; line-height: 1.8;">
                            {message}
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 30px; padding: 20px; background: #e9ecef; border-radius: 10px;">
                        <p style="margin: 0; color: #6c757d; font-size: 14px;">
                            This is an automated message from AI Banking Portal.<br>
                            Please do not reply to this email.
                        </p>
                        <p style="margin: 10px 0 0 0; color: #6c757d; font-size: 12px;">
                            Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
                        </p>
                    </div>
                </body>
            </html>
            """
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)

        # Connect to server and send email
        context = ssl.create_default_context()
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            
            text = msg.as_string()
            server.sendmail(FROM_EMAIL, to_email, text)
            
        print(f"✅ Email sent successfully to {to_email}: {subject}")
        
        # Save notification to CSV for tracking
        save_notification_log(to_email, subject, message, notification_type)
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP Authentication failed: {e}")
        print("Please check your email credentials in the .env file")
        # Fallback to logging
        print(f"\n📧 EMAIL FALLBACK - To: {to_email}, Subject: {subject}")
        save_notification_log(to_email, subject, message, f"{notification_type}_failed")
        return False
        
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error occurred: {e}")
        # Fallback to logging
        print(f"\n📧 EMAIL FALLBACK - To: {to_email}, Subject: {subject}")
        save_notification_log(to_email, subject, message, f"{notification_type}_failed")
        return False
        
    except Exception as e:
        print(f"❌ Email notification error: {e}")
        # Fallback to logging
        print(f"\n📧 EMAIL FALLBACK - To: {to_email}, Subject: {subject}")
        save_notification_log(to_email, subject, message, f"{notification_type}_error")
        return False

def create_html_email_template(title, content, cta_text=None, cta_link=None, alert_type="info"):
    """Create HTML email template"""
    alert_colors = {
        "success": {"bg": "#d4edda", "border": "#28a745", "icon": "✅"},
        "warning": {"bg": "#fff3cd", "border": "#ffc107", "icon": "⚠️"},
        "danger": {"bg": "#f8d7da", "border": "#dc3545", "icon": "❌"},
        "info": {"bg": "#cce7ff", "border": "#007bff", "icon": "ℹ️"}
    }
    
    colors = alert_colors.get(alert_type, alert_colors["info"])
    
    html_template = f"""
    <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f5f5f5;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); overflow: hidden;">
                
                <!-- Header -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px 20px; text-align: center;">
                    <h1 style="margin: 0; font-size: 28px; font-weight: 600;">🏦 AI Banking Portal</h1>
                    <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">Powered by Watson AI Technology</p>
                </div>
                
                <!-- Content -->
                <div style="padding: 40px 30px;">
                    <div style="background: {colors['bg']}; padding: 25px; border-radius: 12px; border-left: 6px solid {colors['border']}; margin-bottom: 30px;">
                        <h2 style="margin: 0 0 15px 0; color: #495057; font-size: 24px; display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 28px;">{colors['icon']}</span>
                            {title}
                        </h2>
                        <div style="font-size: 16px; line-height: 1.8; white-space: pre-line;">
                            {content}
                        </div>
                    </div>
                    
                    {f'''
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{cta_link}" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; font-weight: 600; font-size: 16px; box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);">
                            {cta_text}
                        </a>
                    </div>
                    ''' if cta_text and cta_link else ''}
                </div>
                
                <!-- Footer -->
                <div style="background: #f8f9fa; padding: 25px 30px; text-align: center; border-top: 1px solid #e9ecef;">
                    <p style="margin: 0; color: #6c757d; font-size: 14px;">
                        This is an automated message from <strong>AI Banking Portal</strong><br>
                        Please do not reply to this email.
                    </p>
                    <p style="margin: 15px 0 0 0; color: #adb5bd; font-size: 12px;">
                        Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
                    </p>
                </div>
            </div>
        </body>
    </html>
    """
    
    return html_template

def save_notification_log(email, subject, message, notification_type):
    """Save email notification log to CSV"""
    try:
        notifications_csv = os.path.join(CSV_DIR, "notifications.csv")
        
        # Initialize file if doesn't exist
        if not os.path.exists(notifications_csv):
            with open(notifications_csv, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'email', 'subject', 'message', 'type', 'sent_at'])
        
        # Add notification log
        with open(notifications_csv, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                str(uuid.uuid4()),
                email,
                subject,
                message,
                notification_type,
                datetime.now().isoformat()
            ])
    except Exception as e:
        print(f"Error saving notification log: {e}")

def create_user_alert(user_email, application_id, alert_type, title, message, priority='medium'):
    """Create user alert and save to CSV"""
    try:
        alerts_csv = os.path.join(CSV_DIR, "user_alerts.csv")
        
        with open(alerts_csv, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                str(uuid.uuid4()),
                user_email,
                application_id,
                alert_type,
                title,
                message,
                priority,
                'unread',
                datetime.now().isoformat()
            ])
    except Exception as e:
        print(f"Error creating user alert: {e}")

def get_user_alerts(user_email):
    """Get all alerts for a specific user"""
    try:
        alerts = []
        alerts_csv = os.path.join(CSV_DIR, "user_alerts.csv")
        
        if os.path.exists(alerts_csv):
            with open(alerts_csv, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['user_email'] == user_email:
                        alerts.append(row)
        
        # Sort by created_at descending (newest first)
        alerts.sort(key=lambda x: x['created_at'], reverse=True)
        return alerts
    except Exception as e:
        print(f"Error getting user alerts: {e}")
        return []

def save_document_upload(application_id, user_email, document_type, file_name, file_path):
    """Save document upload information to CSV"""
    try:
        documents_csv = os.path.join(CSV_DIR, "document_uploads.csv")
        
        with open(documents_csv, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                str(uuid.uuid4()),
                application_id,
                user_email,
                document_type,
                file_name,
                file_path,
                'uploaded',
                'pending',
                '',
                datetime.now().isoformat()
            ])
        
        return True
    except Exception as e:
        print(f"Error saving document upload: {e}")
        return False

def get_application_documents(application_id):
    """Get all documents for a specific application"""
    try:
        documents = []
        documents_csv = os.path.join(CSV_DIR, "document_uploads.csv")
        
        if os.path.exists(documents_csv):
            with open(documents_csv, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['application_id'] == application_id:
                        documents.append(row)
        
        return documents
    except Exception as e:
        print(f"Error getting application documents: {e}")
        return []

def update_application_status(application_id, new_status, admin_notes='', verification_status=''):
    """Update application status and admin notes"""
    try:
        # Read all records
        rows = []
        with open(COMPREHENSIVE_LOANS_CSV, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        
        # Update specific application
        updated = False
        for row in rows:
            if row['application_id'] == application_id:
                row['status'] = new_status
                row['updated_at'] = datetime.now().isoformat()
                if admin_notes:
                    row['admin_notes'] = admin_notes
                if verification_status:
                    row['verification_status'] = verification_status
                updated = True
                break
        
        if updated:
            # Write back to file
            with open(COMPREHENSIVE_LOANS_CSV, 'w', newline='', encoding='utf-8') as file:
                if rows:
                    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
                    writer.writeheader()
                    writer.writerows(rows)
            return True
        
        return False
    except Exception as e:
        print(f"Error updating application status: {e}")
        return False

def update_uploaded_documents(application_id, uploaded_files):
    """Update the uploaded_documents field for an application"""
    try:
        # Read all records
        rows = []
        with open(COMPREHENSIVE_LOANS_CSV, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        
        # Update specific application
        for row in rows:
            if row['application_id'] == application_id:
                row['uploaded_documents'] = ', '.join(uploaded_files)
                row['updated_at'] = datetime.now().isoformat()
                break
        
        # Write back to file
        with open(COMPREHENSIVE_LOANS_CSV, 'w', newline='', encoding='utf-8') as file:
            if rows:
                writer = csv.DictWriter(file, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
        return True
    except Exception as e:
        print(f"Error updating uploaded documents: {e}")
        return False

def create_admin_alert(application_id, alert_type, title, message):
    """Create alert for admin dashboard"""
    try:
        admin_alerts_csv = os.path.join(CSV_DIR, "admin_alerts.csv")
        
        # Initialize file if doesn't exist
        if not os.path.exists(admin_alerts_csv):
            with open(admin_alerts_csv, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'application_id', 'alert_type', 'title', 'message', 'status', 'created_at'])
        
        with open(admin_alerts_csv, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                str(uuid.uuid4()),
                application_id,
                alert_type,
                title,
                message,
                'unread',
                datetime.now().isoformat()
            ])
    except Exception as e:
        print(f"Error creating admin alert: {e}")

def get_admin_alerts():
    """Get all alerts for admin dashboard"""
    try:
        alerts = []
        admin_alerts_csv = os.path.join(CSV_DIR, "admin_alerts.csv")
        
        if os.path.exists(admin_alerts_csv):
            with open(admin_alerts_csv, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    alerts.append(row)
        
        # Sort by created_at descending (newest first)
        alerts.sort(key=lambda x: x['created_at'], reverse=True)
        return alerts
    except Exception as e:
        print(f"Error getting admin alerts: {e}")
        return []
        admin_alerts_csv = os.path.join(CSV_DIR, "admin_alerts.csv")
        
        if os.path.exists(admin_alerts_csv):
            with open(admin_alerts_csv, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    alerts.append(row)
        
        # Sort by created_at descending (newest first)
        alerts.sort(key=lambda x: x['created_at'], reverse=True)
        return alerts
    except Exception as e:
        print(f"Error getting admin alerts: {e}")
        return []

# --- API Routes ---
# @app.route('/ask', methods=['POST'])
# def ask_agent():
#     """
#     This endpoint receives a user query, authenticates with IBM,
#     forwards the query to the agent, and returns the agent's response.
#     """
#     # 1. Get a fresh IAM token for this request
#     # This ensures the token is always valid. For higher performance, you could
#     # cache the token and refresh it only when it's about to expire.
#     access_token = get_iam_token()
#     if not access_token:
#         return jsonify({"error": "Failed to authenticate with IBM Cloud. Check API Key and server logs."}), 500

#     # 2. Get the user's query from the incoming request
#     try:
#         request_data = request.get_json()
#         user_query = request_data.get("query")

#         if not user_query:
#             return jsonify({"error": "Query field cannot be empty."}), 400
#     except Exception:
#         return jsonify({"error": "Invalid request format. JSON body with 'query' key is expected."}), 400

#     # 3. Prepare and send the request to the IBM Watsonx Agent
#     agent_headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {access_token}"
#     }
    
#     payload = {
#         "input": user_query
#         # Add other parameters like 'conversation_id' if needed by your agent
#         # "conversation_id": "some-session-id"
#     }

#     try:
#         agent_response = requests.post(AGENT_ENDPOINT, headers=agent_headers, json=payload)
#         agent_response.raise_for_status() # Raise an exception for bad status codes

#         response_json = agent_response.json()
#         # The key for the agent's reply might be 'output' or nested deeper.
#         # Check your agent's response format. Example: result['output']['generic'][0]['text']
#         reply = response_json.get("output", "No output received from agent.")
        
#         return jsonify({"response": reply})

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



@app.route('/ask', methods=['POST'])
def ask_agent():
    """
    This endpoint receives a user query, authenticates with IBM,
    forwards the query to the agent, and returns the agent's response.
    """
    
    # Handle case where IBM credentials are not configured
    if not IBM_ENABLED:
        request_data = request.get_json()
        user_query = request_data.get("query", "")
        
        # Provide a mock response for testing
        mock_response = f"Thank you for your message: '{user_query}'. This is a demo response as IBM Watson is not configured. I can help you with loan information, account queries, and banking services."
        
        # Save the chat interaction to CSV
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
            error_response = "Query field cannot be empty."
            return jsonify({"error": error_response}), 400
    except Exception:
        error_response = "Invalid request format. JSON body with 'query' key is expected."
        return jsonify({"error": error_response}), 400

    # 3. Prepare and send the request to the IBM Watsonx Agent
    agent_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    # --- THIS IS THE CORRECTED PAYLOAD STRUCTURE ---
    # Watsonx agents typically expect a "messages" array.
    payload = {
        "messages": [
            {
                "role": "user",
                "content": user_query
            }
        ]
    }

    try:
        agent_response = requests.post(AGENT_ENDPOINT, headers=agent_headers, json=payload)
        agent_response.raise_for_status() # Raise an exception for bad status codes

        response_json = agent_response.json()
        
        # --- FINAL FIX: Correctly parse the agent's response structure ---
        reply = "Could not parse agent response." # Default message
        # Use .get() for safe access to prevent errors if the structure is unexpected
        choices = response_json.get("choices", [])
        if choices:
            message = choices[0].get("message", {})
            reply = message.get("content", reply)

        # Save the chat interaction to CSV
        save_chat_log(user_query, reply, session.get('session_id'))
        
        return jsonify({"response": reply})

    except requests.exceptions.HTTPError as e:
        # This catches errors from the agent endpoint (e.g., 400, 404, 500)
        error_response = f"Failed to fetch response from IBM Agent. Status: {e.response.status_code}"
        save_chat_log(user_query, error_response)
        return jsonify({
            "error": "Failed to fetch response from IBM Agent.",
            "status_code": e.response.status_code,
            "details": e.response.text
        }), e.response.status_code
    except Exception as e:
        # This catches other errors (e.g., network issues, invalid JSON response)
        error_response = f"An unexpected error occurred: {str(e)}"
        save_chat_log(user_query, error_response)
        return jsonify({"error": error_response}), 500

@app.route('/staff-login', methods=['POST'])
def staff_login():
    """Handle staff login"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'error': 'Username and password required'})
        
        auth_result = verify_staff_credentials(username, password)
        
        if auth_result['success']:
            session['staff_user'] = auth_result['user']
            session['logged_in'] = True
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'error': auth_result['error']})
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Login error: {str(e)}'})

@app.route('/apply-loan', methods=['POST'])
def apply_loan():
    """Handle loan application submission"""
    try:
        loan_data = request.get_json()
        
        # Basic validation
        required_fields = ['firstName', 'lastName', 'email', 'phone', 'loanType', 'loanAmount', 'annualIncome', 'employmentStatus', 'purpose']
        for field in required_fields:
            if not loan_data.get(field):
                return jsonify({'success': False, 'error': f'Missing required field: {field}'})
        
        result = save_loan_application(loan_data)
        
        if result['success']:
            return jsonify({
                'success': True, 
                'message': 'Application submitted successfully',
                'applicationId': result['application_id']
            })
        else:
            return jsonify({'success': False, 'error': result['error']})
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Application error: {str(e)}'})

@app.route('/admin-dashboard')
def admin_dashboard():
    """Admin dashboard to view loan applications and chat logs"""
    if not session.get('logged_in'):
        return redirect('/')
    
    # Get all loan applications and recent chat logs
    applications = get_all_loan_applications()
    chat_logs = get_chat_logs(50)  # Get last 50 chat interactions
    
    # Debug: Print number of applications found
    print(f"Admin Dashboard: Found {len(applications)} applications")
    for app in applications[:3]:  # Print first 3 for debugging
        print(f"Application: {app.get('application_id', 'N/A')} - {app.get('email', app.get('user_email', 'N/A'))}")
    
    # Simple HTML template for admin dashboard
    dashboard_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .header { background: #2563eb; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
            .section { margin: 20px 0; }
            .section h2 { color: #1e293b; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }
            table { width: 100%; border-collapse: collapse; margin: 10px 0; }
            th, td { border: 1px solid #e2e8f0; padding: 12px; text-align: left; }
            th { background: #f8fafc; font-weight: 600; }
            .status-pending { background: #fef3c7; color: #92400e; padding: 4px 8px; border-radius: 4px; }
            .status-approved { background: #dcfce7; color: #166534; padding: 4px 8px; border-radius: 4px; }
            .status-rejected { background: #fee2e2; color: #991b1b; padding: 4px 8px; border-radius: 4px; }
            .logout-btn { background: #dc2626; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
            .logout-btn:hover { background: #b91c1c; }
            .source-tag { font-size: 0.8em; padding: 2px 6px; border-radius: 3px; }
            .source-basic { background: #e0f2fe; color: #0277bd; }
            .source-comprehensive { background: #f3e5f5; color: #7b1fa2; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏦 Banking Admin Dashboard</h1>
            <p>Welcome, """ + session['staff_user']['username'] + """</p>
            <button class="logout-btn" onclick="location.href='/logout'">Logout</button>
        </div>
        
        <div class="section">
            <h2>📋 Loan Applications (""" + str(len(applications)) + """)</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Loan Type</th>
                        <th>Amount</th>
                        <th>Status</th>
                        <th>Type</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    for app in applications:
        # Handle different status values
        status = app.get('status', 'pending')
        status_class = 'status-pending'
        if status.lower() in ['approved', 'eligibility_assessed']:
            status_class = 'status-approved'
        elif status.lower() == 'rejected':
            status_class = 'status-rejected'
        
        # Handle different source types
        source = app.get('source', 'unknown')
        source_class = f'source-{source}'
        
        # Get the display name
        name = f"{app.get('first_name', '')} {app.get('last_name', '')}".strip()
        if not name:
            name = app.get('full_name', 'N/A')
        
        # Get email
        email = app.get('email', app.get('user_email', 'N/A'))
        
        # Format amount
        amount = app.get('loan_amount', app.get('loanAmount', 'N/A'))
        if amount and amount != 'N/A':
            try:
                amount = f"${float(amount):,.0f}"
            except:
                amount = f"${amount}"
        
        dashboard_html += f"""
                    <tr>
                        <td>{app.get('application_id', 'N/A')}</td>
                        <td>{name}</td>
                        <td>{email}</td>
                        <td>{app.get('loan_type', app.get('loanType', 'N/A'))}</td>
                        <td>{amount}</td>
                        <td><span class="{status_class}">{status}</span></td>
                        <td><span class="source-tag {source_class}">{source}</span></td>
                        <td>{app.get('created_at', 'N/A')[:10]}</td>
                    </tr>
        """
    
    dashboard_html += """
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>💬 Recent Chat Interactions (""" + str(len(chat_logs)) + """)</h2>
            <table>
                <thead>
                    <tr>
                        <th>Time</th>
                        <th>User Message</th>
                        <th>Bot Response</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    for log in chat_logs:
        dashboard_html += f"""
                    <tr>
                        <td>{log.get('timestamp', 'N/A')[:19].replace('T', ' ')}</td>
                        <td>{log.get('user_message', 'N/A')[:100]}{'...' if len(log.get('user_message', '')) > 100 else ''}</td>
                        <td>{log.get('bot_response', 'N/A')[:100]}{'...' if len(log.get('bot_response', '')) > 100 else ''}</td>
                    </tr>
        """
    
    dashboard_html += """
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    
    return dashboard_html

@app.route('/logout')
def logout():
    """Handle staff logout"""
    session.clear()
    return redirect('/')

@app.route('/user-register', methods=['POST'])
def user_register():
    """User registration endpoint"""
    try:
        data = request.json
        result = register_user(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/user-login', methods=['POST'])
def user_login():
    """User login endpoint"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        result = verify_user_credentials(email, password)
        if result['success']:
            session['user_logged_in'] = True
            session['user_email'] = email
            session['user_data'] = result['user']
            
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/user-logout', methods=['POST'])
def user_logout():
    """User logout endpoint"""
    session.pop('user_logged_in', None)
    session.pop('user_email', None)
    session.pop('user_data', None)
    return jsonify({'success': True})

@app.route('/user-auth-status', methods=['GET'])
def user_auth_status():
    """Check user authentication status and automatically clear staff sessions"""
    # Automatically clear any staff sessions when checking user auth
    staff_keys = ['logged_in', 'staff_user', 'username', 'role', 'admin_logged_in']
    for key in staff_keys:
        session.pop(key, None)
    
    if session.get('user_logged_in'):
        return jsonify({
            'logged_in': True, 
            'email': session.get('user_email')
        })
    else:
        return jsonify({'logged_in': False})

@app.route('/clear-staff-session', methods=['POST'])
def clear_staff_session():
    """Clear staff session when user interface is accessed"""
    try:
        # Clear all staff-related session keys more thoroughly
        staff_keys = ['logged_in', 'staff_user', 'username', 'role', 'admin_logged_in']
        for key in staff_keys:
            session.pop(key, None)
        
        # Force session regeneration to prevent conflicts
        session.permanent = False
        
        return jsonify({'success': True, 'message': 'Staff session cleared completely'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin-logout', methods=['POST'])
def admin_logout():
    """Force admin logout - more aggressive clearing"""
    try:
        # Clear all session data
        session.clear()
        return jsonify({'success': True, 'message': 'Admin logged out completely'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/clear-user-session', methods=['POST'])
def clear_user_session():
    """Clear user session when staff logs in"""
    session.pop('user_logged_in', None)
    session.pop('user_email', None)
    session.pop('user_data', None)
    return jsonify({'success': True})

@app.route('/clear-all-sessions', methods=['POST'])
def clear_all_sessions():
    """Clear all sessions (used when returning to main chat)"""
    session.clear()
    return jsonify({'success': True})

@app.route('/user-applications', methods=['GET'])
def get_user_applications_endpoint():
    """Get all applications for logged-in user"""
    try:
        if not session.get('user_logged_in'):
            return jsonify({'success': False, 'error': 'Not authenticated'})
        
        user_email = session.get('user_email')
        applications = get_user_applications(user_email)
        return jsonify({'success': True, 'applications': applications})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/apply-comprehensive-loan', methods=['POST'])
def apply_comprehensive_loan():
    """Handle comprehensive loan application"""
    try:
        if not session.get('user_logged_in'):
            return jsonify({'success': False, 'error': 'Not authenticated'})
        
        data = request.json
        data['userEmail'] = session.get('user_email')  # Add user email from session
        
        result = save_comprehensive_loan_application(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/user-alerts', methods=['GET'])
def get_user_alerts_endpoint():
    """Get all alerts for logged-in user"""
    try:
        if not session.get('user_logged_in'):
            return jsonify({'success': False, 'error': 'Not authenticated'})
        
        user_email = session.get('user_email')
        alerts = get_user_alerts(user_email)
        return jsonify({'success': True, 'alerts': alerts})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/upload-documents', methods=['POST'])
def upload_documents():
    """Handle document upload for loan applications"""
    try:
        if not session.get('user_logged_in'):
            return jsonify({'success': False, 'error': 'Not authenticated'})
        
        application_id = request.form.get('application_id')
        document_type = request.form.get('document_type')
        user_email = session.get('user_email')
        
        if not application_id or not document_type:
            return jsonify({'success': False, 'error': 'Application ID and document type required'})
        
        # Create uploads directory if it doesn't exist
        uploads_dir = os.path.join(CSV_DIR, 'uploads', application_id)
        os.makedirs(uploads_dir, exist_ok=True)
        
        uploaded_files = []
        
        # Process the uploaded file
        if 'document' in request.files:
            file = request.files['document']
            if file and file.filename:
                # Secure filename
                filename = f"{document_type}_{file.filename}"
                file_path = os.path.join(uploads_dir, filename)
                
                try:
                    file.save(file_path)
                    
                    # Save to database
                    save_document_upload(application_id, user_email, document_type, filename, file_path)
                    uploaded_files.append(filename)
                    
                except Exception as e:
                    print(f"Error saving file {filename}: {e}")
                    return jsonify({'success': False, 'error': f'Error saving file: {str(e)}'})
        
        if uploaded_files:
            # Update application with uploaded documents
            update_uploaded_documents(application_id, uploaded_files)
            
            # Create alert for admin
            create_admin_alert(application_id, 'documents_uploaded', 
                             'Documents Uploaded for Review',
                             f'Application {application_id} has uploaded {document_type} for verification')
            
            # Send email to user
            send_email_notification(
                user_email,
                f"Document Uploaded Successfully - Application {application_id}",
                f"Your {document_type} has been successfully uploaded for application {application_id}. Our team will review it shortly and contact you if any additional information is needed.",
                'document_upload'
            )
            
            return jsonify({
                'success': True, 
                'message': f'Successfully uploaded {document_type}',
                'files': uploaded_files
            })
        else:
            return jsonify({'success': False, 'error': 'No valid files uploaded'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/notify-admin-document-upload', methods=['POST'])
def notify_admin_document_upload():
    """Send email notification to admin when documents are uploaded"""
    try:
        if not session.get('user_logged_in'):
            return jsonify({'success': False, 'error': 'Not authenticated'})
        
        data = request.json
        application_id = data.get('application_id')
        document_type = data.get('document_type')
        user_email = data.get('user_email')
        
        if not all([application_id, document_type, user_email]):
            return jsonify({'success': False, 'error': 'Missing required fields'})
        
        # Get admin email (you can configure this)
        admin_email = "singhishant37@gmail.com"  # Change this to actual admin email
        
        # Create admin alert
        create_admin_alert(
            application_id, 
            'document_uploaded',
            f'New Document Uploaded - {document_type}',
            f'User {user_email} has uploaded {document_type} for application {application_id}. Please review and verify the document.'
        )
        
        # Send email to admin
        admin_subject = f"🔔 Document Upload Alert - Application {application_id}"
        admin_message = f"""A new document has been uploaded for review.

Application Details:
• Application ID: {application_id}
• User Email: {user_email}
• Document Type: {document_type}
• Upload Time: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

Action Required:
Please log in to the admin dashboard to review and verify the uploaded document.

Direct Link: http://127.0.0.1:5001/staff.html

Best regards,
AI Banking Portal System"""

        html_content = create_html_email_template(
            title="New Document Upload",
            content=f"""A user has uploaded a new document for verification.

Application ID: {application_id}
User: {user_email}
Document: {document_type}

Please review the document in your admin dashboard.""",
            cta_text="Review Document",
            cta_link="http://127.0.0.1:5001/staff.html",
            alert_type="info"
        )
        
        send_email_notification(admin_email, admin_subject, admin_message, 'admin_alert', html_content)
        
        return jsonify({'success': True, 'message': 'Admin notified successfully'})
        
    except Exception as e:
        print(f"Error notifying admin: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/application-details/<application_id>', methods=['GET'])
def get_application_details(application_id):
    """Get detailed application information including documents"""
    try:
        if not session.get('user_logged_in'):
            return jsonify({'success': False, 'error': 'Not authenticated'})
        
        user_email = session.get('user_email')
        
        # Get application details
        with open(COMPREHENSIVE_LOANS_CSV, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['application_id'] == application_id and row['user_email'] == user_email:
                    # Get associated documents
                    documents = get_application_documents(application_id)
                    
                    return jsonify({
                        'success': True,
                        'application': row,
                        'documents': documents
                    })
        
        return jsonify({'success': False, 'error': 'Application not found'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/applications', methods=['GET'])
def admin_get_applications():
    """Get all applications for admin review"""
    try:
        if not session.get('logged_in'):
            return jsonify({'success': False, 'error': 'Admin authentication required'})
        
        applications = []
        
        # Get comprehensive applications
        try:
            with open(COMPREHENSIVE_LOANS_CSV, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Get associated documents count
                    documents = get_application_documents(row['application_id'])
                    row['document_count'] = len(documents)
                    applications.append(row)
        except FileNotFoundError:
            pass
        
        return jsonify({'success': True, 'applications': applications})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/verify-application', methods=['POST'])
def admin_verify_application():
    """Admin endpoint to verify/approve/reject applications"""
    try:
        if not session.get('logged_in'):
            return jsonify({'success': False, 'error': 'Admin authentication required'})
        
        data = request.json
        application_id = data.get('application_id')
        action = data.get('action')  # 'approve', 'reject', 'request_revision'
        admin_notes = data.get('admin_notes', '')
        
        if not application_id or not action:
            return jsonify({'success': False, 'error': 'Application ID and action required'})
        
        # Get application details for email notification
        application_data = None
        with open(COMPREHENSIVE_LOANS_CSV, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['application_id'] == application_id:
                    application_data = row
                    break
        
        if not application_data:
            return jsonify({'success': False, 'error': 'Application not found'})
        
        user_email = application_data['user_email']
        user_name = application_data['full_name']
        
        # Update application status
        if action == 'approve':
            success = update_application_status(application_id, 'approved', admin_notes, 'verified')
            
            # Send approval notification
            create_user_alert(
                user_email, application_id, 'approval',
                'Loan Application Approved!',
                f'Congratulations! Your loan application {application_id} has been approved.',
                'high'
            )
            
            email_subject = f"🎉 Loan Approved - Application {application_id}"
            email_message = f"""Dear {user_name},

Congratulations! Your loan application has been APPROVED after thorough review and document verification.

Application Details:
• Application ID: {application_id}
• Loan Type: {application_data.get('loan_type', 'N/A')}
• Loan Amount: {format_currency(application_data.get('loan_amount', 'N/A'))}
• Status: APPROVED

Admin Review Notes: {admin_notes}

Next Steps:
1. You will receive loan agreement documents via email within 24 hours
2. Please review and digitally sign the loan agreement
3. Loan disbursement will be processed within 3-5 business days after agreement completion
4. Our relationship manager will contact you to complete the process

Thank you for choosing AI Banking Portal for your financial needs.

Best regards,
AI Banking Portal Team"""

            html_content = create_html_email_template(
                title="Loan Application Approved!",
                content=f"""Your loan application has been successfully approved after document verification.

Application ID: {application_id}
Loan Amount: {format_currency(application_data.get('loan_amount', 'N/A'))}
Status: APPROVED

Admin Notes: {admin_notes}

Next Steps:
• Loan agreement documents will be sent within 24 hours
• Digital signature required
• Disbursement within 3-5 business days""",
                cta_text="View Application Status",
                cta_link="http://127.0.0.1:5001/",
                alert_type="success"
            )
            
            send_email_notification(
                user_email, email_subject, email_message, 'approval', html_content
            )
            
        elif action == 'reject':
            success = update_application_status(application_id, 'rejected', admin_notes, 'rejected')
            
            # Send rejection notification
            create_user_alert(
                user_email, application_id, 'rejection',
                'Loan Application Decision',
                f'Your loan application {application_id} has been reviewed. Please check your email for details.',
                'high'
            )
            
            email_subject = f"📋 Loan Application Decision - Application {application_id}"
            email_message = f"""Dear {user_name},

After careful review of your loan application and submitted documents, we are unable to approve your request at this time.

Application Details:
• Application ID: {application_id}
• Loan Type: {application_data.get('loan_type', 'N/A')}
• Loan Amount: {format_currency(application_data.get('loan_amount', 'N/A'))}
• Status: NOT APPROVED

Review Notes: {admin_notes}

We understand this may be disappointing, and we want to help you succeed in future applications:

• You may reapply after addressing the mentioned concerns
• Our customer service team is available to discuss improvement strategies
• Consider applying for a smaller loan amount or improving your credit profile

We appreciate your interest in our services and hope to serve you in the future.

Best regards,
AI Banking Portal Team"""

            html_content = create_html_email_template(
                title="Loan Application Decision",
                content=f"""After thorough review, we are unable to approve your loan application at this time.

Application ID: {application_id}
Status: NOT APPROVED

Review Notes:
{admin_notes}

We encourage you to:
• Address the mentioned concerns
• Consider reapplying with improved documentation
• Contact our team for guidance on eligibility improvement""",
                cta_text="Contact Customer Service",
                cta_link="http://127.0.0.1:5001/",
                alert_type="danger"
            )
            
            send_email_notification(
                user_email, email_subject, email_message, 'rejection', html_content
            )
            
        elif action == 'request_revision':
            success = update_application_status(application_id, 'revision_requested', admin_notes, 'revision_required')
            
            # Send revision request notification
            create_user_alert(
                user_email, application_id, 'revision_required',
                'Application Revision Required',
                f'Your loan application {application_id} requires additional information or corrected documents.',
                'medium'
            )
            
            email_subject = f"📝 Additional Information Required - Application {application_id}"
            email_message = f"""Dear {user_name},

Your loan application has been reviewed and we need additional information or document corrections to proceed.

Application Details:
• Application ID: {application_id}
• Loan Type: {application_data.get('loan_type', 'N/A')}
• Loan Amount: {format_currency(application_data.get('loan_amount', 'N/A'))}
• Status: REVISION REQUIRED

Required Changes: {admin_notes}

Next Steps:
1. Log in to your account dashboard
2. Review the specific requirements mentioned above
3. Upload corrected or additional documents as needed
4. Resubmit your application for review

Our team will prioritize the review of your updated application.

Best regards,
AI Banking Portal Team"""

            html_content = create_html_email_template(
                title="Application Revision Required",
                content=f"""We need additional information to complete the review of your loan application.

Application ID: {application_id}
Status: REVISION REQUIRED

Required Changes:
{admin_notes}

Please log in to your dashboard and provide the requested information or corrected documents.""",
                cta_text="Update Application",
                cta_link="http://127.0.0.1:5001/",
                alert_type="warning"
            )
            
            send_email_notification(
                user_email, email_subject, email_message, 'revision_request', html_content
            )
        
        if success:
            return jsonify({'success': True, 'message': f'Application {action}d successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to update application'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/')
def serve_main():
    """Serve the main LoanBot chatbot interface"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/staff')
def serve_staff():
    """Serve the staff login page"""
    return send_from_directory('../frontend', 'staff.html')

@app.route('/apply')
def serve_apply():
    """Serve the loan application page"""
    return send_from_directory('../frontend', 'apply.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('../frontend', filename)

# Initialize CSV files on startup
initialize_csv_files()

# --- Main Execution ---
if __name__ == "__main__":
    # The app runs on port 5000 by default.
    # You can change it with: app.run(debug=True, port=5001)
    app.run(debug=False, port=5001)  # Disabled debug to avoid watchdog issues