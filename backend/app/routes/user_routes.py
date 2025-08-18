# backend/app/routes/user_routes.py file

from flask import Blueprint, request, jsonify, session, current_app
import os
import csv
from werkzeug.utils import secure_filename
from datetime import datetime

# Import all the necessary functions from our other modules
from ..utils.csv_handler import (
    register_user, verify_user_credentials, save_loan_application,
    get_user_applications, get_user_objected_applications,
    get_user_alerts, save_document_upload, update_uploaded_documents,
    get_application_documents, add_application_history, update_application_status,
    create_admin_alert
)
from ..services.watson_service import assess_loan_eligibility_with_watson
from ..services.notification_service import send_email_notification, create_html_email_template
from ..utils.helpers import format_currency

user_bp = Blueprint('user_bp', __name__)

# --- Helper "Manager" Function ---
# This complex function coordinates multiple services, so we keep it here with the route that uses it.
def save_comprehensive_loan_application(loan_data):
    """
    Orchestrates the comprehensive loan application process:
    1. Gets AI assessment from Watson.
    2. Saves the combined result to the CSV.
    3. Creates user alerts and sends email notifications.
    """
    # This function needs to be copied here from your original agent.py.
    # Make sure it uses the imported functions like assess_loan_eligibility_with_watson,
    # create_user_alert, and send_email_notification.
    # Remember to import any other dependencies it needs, like uuid and datetime.
    # ... (Paste the full save_comprehensive_loan_application function here) ...


# --- User Account Routes ---

@user_bp.route('/user-register', methods=['POST'])
def user_register_route():
    try:
        data = request.json
        result = register_user(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@user_bp.route('/user-login', methods=['POST'])
def user_login_route():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        result = verify_user_credentials(email, password)
        if result['success']:
            session.permanent = True
            session['user_logged_in'] = True
            session['user_email'] = email
            session['user_data'] = result['user']
            
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@user_bp.route('/user-logout', methods=['POST'])
def user_logout_route():
    session.pop('user_logged_in', None)
    session.pop('user_email', None)
    session.pop('user_data', None)
    return jsonify({'success': True})

@user_bp.route('/user-auth-status', methods=['GET'])
def user_auth_status_route():
    if session.get('user_logged_in'):
        return jsonify({
            'logged_in': True,
            'email': session.get('user_email')
        })
    else:
        return jsonify({'logged_in': False})


# --- Loan Application Routes ---

@user_bp.route('/apply-loan', methods=['POST'])
def apply_loan_route():
    try:
        loan_data = request.get_json()
        result = save_loan_application(loan_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': f'Application error: {str(e)}'})

@user_bp.route('/apply-comprehensive-loan', methods=['POST'])
def apply_comprehensive_loan_route():
    try:
        if not session.get('user_logged_in'):
            return jsonify({'success': False, 'error': 'Not authenticated'})
        
        data = request.json
        data['userEmail'] = session.get('user_email')
        
        # This is where we call the complex "manager" function
        result = save_comprehensive_loan_application(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@user_bp.route('/user-applications', methods=['GET'])
def get_user_applications_route():
    if not session.get('user_logged_in'):
        return jsonify({'success': False, 'error': 'Not authenticated'})
    
    user_email = session.get('user_email')
    applications = get_user_applications(user_email)
    return jsonify({'success': True, 'applications': applications})

@user_bp.route('/user-drafts', methods=['GET'])
def get_user_drafts_route():
    if not session.get('user_logged_in'):
        return jsonify({'success': False, 'error': 'Not authenticated'})
        
    user_email = session.get('user_email')
    drafts = get_user_objected_applications(user_email)
    return jsonify({'success': True, 'drafts': drafts})


# --- Helper "Manager" Function for Resubmission ---
def resubmit_objected_application(application_id, user_email, new_documents=None):
    """Resubmit an objected application with new documents"""
    try:
        # Update application status to pending review
        update_application_status(application_id, 'resubmitted', 'Application resubmitted with new documents')
        
        # Update objection status to resolved
        objections_csv = current_app.config['OBJECTIONS_CSV'] # You will need to add OBJECTIONS_CSV to your config.py
        if os.path.exists(objections_csv):
            rows = []
            fieldnames = []
            with open(objections_csv, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                for row in reader:
                    if row['application_id'] == application_id and row['user_email'] == user_email and row['status'] == 'pending':
                        row['status'] = 'resolved'
                        row['resolved_at'] = datetime.now().isoformat()
                    rows.append(row)
            
            with open(objections_csv, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
        
        # Add to application history
        add_application_history(application_id, user_email, 'RESUBMITTED', user_email, f'Application resubmitted with new documents: {new_documents or "No new documents"}')
        
        return True
    except Exception as e:
        print(f"Error resubmitting application: {e}")
        return False


# --- The Route that uses the function above ---
@user_bp.route('/resubmit-application', methods=['POST'])
def resubmit_application_route():
    """Resubmit an objected application"""
    try:
        if not session.get('user_logged_in'):
            return jsonify({'success': False, 'error': 'Not authenticated'})
        
        data = request.get_json()
        application_id = data.get('application_id')
        user_email = session.get('user_email')
        
        if not application_id:
            return jsonify({'success': False, 'error': 'Application ID is required'})
        
        # Verify this application belongs to the user and is objected
        drafts = get_user_objected_applications(user_email)
        app_exists = any(draft['application_id'] == application_id for draft in drafts)
        
        if not app_exists:
            return jsonify({'success': False, 'error': 'Application not found or not accessible'})
        
        # Get the latest uploaded documents for this application
        uploaded_docs = ""
        # This logic should also be moved to csv_handler, but we'll keep it for now
        try:
            with open(current_app.config['COMPREHENSIVE_LOANS_CSV'], 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['application_id'] == application_id:
                        uploaded_docs = row.get('uploaded_documents', '')
                        break
        except FileNotFoundError:
            pass
        
        success = resubmit_objected_application(application_id, user_email, uploaded_docs)
        
        if success:
            return jsonify({'success': True, 'message': 'Application resubmitted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to resubmit application'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


# @user_bp.route('/resubmit-application', methods=['POST'])
# def resubmit_application_route():
#     if not session.get('user_logged_in'):
#         return jsonify({'success': False, 'error': 'Not authenticated'})
    
#     data = request.json
#     application_id = data.get('application_id')
#     user_email = session.get('user_email')
    
#     # This calls the resubmit function now located in csv_handler.py
#     success = resubmit_objected_application(application_id, user_email)
    
#     if success:
#         return jsonify({'success': True, 'message': 'Application resubmitted successfully'})
#     else:
#         return jsonify({'success': False, 'error': 'Failed to resubmit application'})


# --- Document and Notification Routes ---

@user_bp.route('/upload-documents', methods=['POST'])
def upload_documents_route():
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
        uploads_dir = os.path.join(current_app.config['CSV_DIR'], 'uploads', application_id)
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

@user_bp.route('/user-alerts', methods=['GET'])
def get_user_alerts_route():
    if not session.get('user_logged_in'):
        return jsonify({'success': False, 'error': 'Not authenticated'})
        
    user_email = session.get('user_email')
    alerts = get_user_alerts(user_email)
    return jsonify({'success': True, 'alerts': alerts})