# Key Changes required 
# Go through every function you moved into csv_handler.py. Look for any line that opens a file, like open(STAFF_CSV, ...). You need to change it.
# Here is the "Before and After" pattern:
# BEFORE (the old way):
# Python
# with open(STAFF_CSV, 'r', newline='', encoding='utf-8') as file:
# AFTER (the new, correct way):
# Python
# with open(current_app.config['STAFF_CSV'], 'r', newline='', encoding='utf-8') as file:
# You are replacing the variable name (e.g., STAFF_CSV) with current_app.config['STAFF_CSV']. You must do this for every single file path in every function in this file.



# backend/app/utils/csv_handler.py
import csv
import os
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app


# --- CSV Helper Functions ---
# In backend/app/utils/csv_handler.py

def initialize_csv_files(config):
    """Initialize CSV files with headers if they don't exist"""

    # Create data directory if it doesn't exist. This is the key fix.
    os.makedirs(config['CSV_DIR'], exist_ok=True)
    
    # --- The Fix: Use the 'config' parameter, not 'current_app.config' ---

    # Initialize staff.csv
    if not os.path.exists(config['STAFF_CSV']):
        with open(config['STAFF_CSV'], 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'username', 'password_hash', 'email', 'role', 'created_at'])
            # Add default admin user
            admin_id = str(uuid.uuid4())
            admin_password_hash = generate_password_hash('admin123')
            writer.writerow([admin_id, 'admin', admin_password_hash, 'singhishant37@gmail.com', 'admin', datetime.now().isoformat()])
    
    # Initialize users.csv
    if not os.path.exists(config['USERS_CSV']):
        with open(config['USERS_CSV'], 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'name', 'email', 'phone', 'password_hash', 'created_at'])
    
    # Initialize loan_applications.csv (simple form)
    if not os.path.exists(config['LOAN_APPLICATIONS_CSV']):
        with open(config['LOAN_APPLICATIONS_CSV'], 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'application_id', 'first_name', 'last_name', 'email', 'phone', 
                'loan_type', 'loan_amount', 'annual_income', 'employment_status', 
                'purpose', 'status', 'created_at'
            ])
    
    # Initialize comprehensive_loans.csv (detailed form)
    if not os.path.exists(config['COMPREHENSIVE_LOANS_CSV']): # <-- Corrected syntax here
        with open(config['COMPREHENSIVE_LOANS_CSV'], 'w', newline='', encoding='utf-8') as file:
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
    # --- Corrected the path creation logic below ---
    documents_csv = os.path.join(config['CSV_DIR'], "document_uploads.csv")
    if not os.path.exists(documents_csv):
        with open(documents_csv, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'id', 'application_id', 'user_email', 'document_type', 
                'file_name', 'file_path', 'upload_status', 'verified', 
                'admin_comments', 'uploaded_at'
            ])
    
    # Initialize user_alerts.csv
    alerts_csv = os.path.join(config['CSV_DIR'], "user_alerts.csv")
    if not os.path.exists(alerts_csv):
        with open(alerts_csv, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'id', 'user_email', 'application_id', 'alert_type', 
                'title', 'message', 'priority', 'read', 'created_at'
            ])
    
    # Initialize chat_logs.csv
    if not os.path.exists(config['CHAT_LOGS_CSV']): # <-- Corrected syntax here
        with open(config['CHAT_LOGS_CSV'], 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'user_message', 'bot_response', 'timestamp', 'session_id'])
            
def verify_staff_credentials(username, password):
    """Verify staff login credentials"""
    try:
        with open(current_app.config['STAFF_CSV'], 'r', newline='', encoding='utf-8') as file:
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
        
        with open(current_app.config['LOAN_APPLICATIONS_CSV'], 'a', newline='', encoding='utf-8') as file:
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
        
        with open(current_app.config['CHAT_LOGS_CSV'], 'a', newline='', encoding='utf-8') as file:
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
            with open(current_app.config['LOAN_APPLICATIONS_CSV'], 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Add source indicator
                    row['source'] = 'basic'
                    applications.append(row)
        except FileNotFoundError:
            pass
        
        # Read comprehensive loan applications (new format)
        try:
            with open(current_app.config['COMPREHENSIVE_LOANS_CSV'], 'r', newline='', encoding='utf-8') as file:
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
        with open(current_app.config['CHAT_LOGS_CSV'], 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                logs.append(row)
        return logs[-limit:]  # Return last N logs
    except FileNotFoundError:
        return []

def update_application_status(app_id, new_status, admin_notes=''):
    """Update the status of a loan application"""
    updated = False
    
    # Try updating in comprehensive loans CSV
    try:
        rows = []
        with open(current_app.config['COMPREHENSIVE_LOANS_CSV'], 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            for row in reader:
                if row.get('application_id') == app_id:
                    row['eligibility_status'] = new_status
                    row['status'] = 'eligibility_assessed'
                    if admin_notes:
                        row['admin_notes'] = admin_notes
                    row['updated_at'] = datetime.now().isoformat()
                    updated = True
                rows.append(row)
        
        if updated:
            with open(current_app.config['COMPREHENSIVE_LOANS_CSV'], 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            return True
    except FileNotFoundError:
        pass
    
    # Try updating in basic loan applications CSV
    try:
        rows = []
        with open(current_app.config['LOAN_APPLICATIONS_CSV'], 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            for row in reader:
                if row.get('application_id') == app_id:
                    row['status'] = new_status.lower()
                    if admin_notes:
                        row['admin_notes'] = admin_notes
                    row['updated_at'] = datetime.now().isoformat()
                    updated = True
                rows.append(row)
        
        if updated:
            with open(current_app.config['LOAN_APPLICATIONS_CSV'], 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            return True
    except FileNotFoundError:
        pass
    
    return False

def get_application_documents(app_id):
    """Get all documents for a specific application"""
    documents = []
    try:
        DOCUMENT_UPLOADS_CSV = os.path.join(current_app.config['CSV_DIR'], "document_uploads.csv")
        with open(DOCUMENT_UPLOADS_CSV, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('application_id') == app_id:
                    documents.append(row)
    except FileNotFoundError:
        pass
    return documents

def get_application_history(app_id):
    """Get history for a specific application"""
    history = []
    try:
        HISTORY_CSV = os.path.join(current_app.config['CSV_DIR'], "application_history.csv")
        with open(HISTORY_CSV, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('application_id') == app_id:
                    history.append(row)
    except FileNotFoundError:
        pass
    return sorted(history, key=lambda x: x.get('created_at', ''), reverse=True)

def add_application_history(app_id, user_email, action_type, action_by, action_reason=''):
    """Add an entry to application history"""
    try:
        HISTORY_CSV = os.path.join(current_app.config['CSV_DIR'], "application_history.csv")
        
        # Create file with headers if it doesn't exist
        if not os.path.exists(HISTORY_CSV):
            with open(HISTORY_CSV, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['draft_id', 'application_id', 'user_email', 'status', 'action_type', 'action_by', 'action_reason', 'created_at', 'updated_at'])
        
        # Add new history entry
        with open(HISTORY_CSV, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            timestamp = datetime.now().isoformat()
            draft_id = str(uuid.uuid4())[:8].upper()
            writer.writerow([draft_id, app_id, user_email, 'processed', action_type, action_by, action_reason, timestamp, timestamp])
        
        return True
    except Exception as e:
        print(f"Error adding application history: {e}")
        return False
    
def create_objection(app_id, user_email, reason, requested_docs, created_by):
    """Create a new objection for an application"""
    try:
        OBJECTIONS_CSV = os.path.join(current_app.config['CSV_DIR'], "objections.csv")
        
        # Create file with headers if it doesn't exist
        if not os.path.exists(OBJECTIONS_CSV):
            with open(OBJECTIONS_CSV, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['objection_id', 'application_id', 'user_email', 'objection_reason', 'requested_documents', 'status', 'created_by', 'created_at', 'resolved_at'])
        
        # Add new objection
        with open(OBJECTIONS_CSV, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            objection_id = str(uuid.uuid4())[:8].upper()
            timestamp = datetime.now().isoformat()
            writer.writerow([objection_id, app_id, user_email, reason, requested_docs, 'pending', created_by, timestamp, ''])
        
        # Add to application history
        add_application_history(app_id, user_email, 'OBJECTION RAISED', created_by, reason)
        
        # Update application status to pending
        update_application_status(app_id, 'OBJECTION_RAISED', f'Objection raised: {reason}')
        
        return objection_id
    except Exception as e:
        print(f"Error creating objection: {e}")
        import traceback
        traceback.print_exc()
        return None

def register_user(user_data):
    """Register a new user"""
    try:
        # Check if user already exists
        with open(current_app.config['USERS_CSV'], 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['email'] == user_data.get('email'):
                    return {'success': False, 'error': 'Email already registered'}
        
        # Add new user
        user_id = str(uuid.uuid4())
        password_hash = generate_password_hash(user_data.get('password'))
        
        with open(current_app.config['USERS_CSV'], 'a', newline='', encoding='utf-8') as file:
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
        with open(current_app.config['USERS_CSV'], 'r', newline='', encoding='utf-8') as file:
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

def get_user_applications(user_email):
    """Get all loan applications for a specific user"""
    try:
        applications = []
        
        # Get simple applications
        try:
            with open(current_app.config['LOAN_APPLICATIONS_CSV'], 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['email'] == user_email:
                        applications.append(row)
        except FileNotFoundError:
            pass
        
        # Get comprehensive applications
        try:
            with open(current_app.config['COMPREHENSIVE_LOANS_CSV'], 'r', newline='', encoding='utf-8') as file:
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

def get_user_objected_applications(user_email):
    """Get all objected applications (drafts) for a specific user"""
    try:
        drafts = []
        
        # Get objections for this user
        OBJECTIONS_CSV = os.path.join(current_app.config['CSV_DIR'], "objections.csv")
        if not os.path.exists(OBJECTIONS_CSV):
            return []
            
        with open(OBJECTIONS_CSV, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            user_objections = [row for row in reader if row['user_email'] == user_email and row['status'] == 'pending']
        
        # Get application details for each objection
        for objection in user_objections:
            app_id = objection['application_id']
            
            # Get application details from comprehensive loans
            try:
                with open(current_app.config['COMPREHENSIVE_LOANS_CSV'], 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row['application_id'] == app_id and row['status'] == 'OBJECTION_RAISED':
                            draft = {
                                'application_id': app_id,
                                'objection_id': objection['objection_id'],
                                'loan_type': row['loan_type'],
                                'loan_amount': row['loan_amount'],
                                'objection_reason': objection['objection_reason'],
                                'requested_documents': objection['requested_documents'],
                                'created_at': row['created_at'],
                                'objection_created_at': objection['created_at'],
                                'current_documents': row.get('uploaded_documents', ''),
                                'full_application': row
                            }
                            drafts.append(draft)
                            break
            except FileNotFoundError:
                continue
                
        return drafts
    except Exception as e:
        print(f"Error getting user objected applications: {e}")
        return []
    
def save_notification_log(email, subject, message, notification_type):
    """Save email notification log to CSV"""
    try:
        notifications_csv = os.path.join(current_app.config['CSV_DIR'], "notifications.csv")
        
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
        alerts_csv = os.path.join(current_app.config['CSV_DIR'], "user_alerts.csv")
        
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
        alerts_csv = os.path.join(current_app.config['CSV_DIR'], "user_alerts.csv")
        
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
        documents_csv = os.path.join(current_app.config['CSV_DIR'], "document_uploads.csv")
        
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
    
def update_uploaded_documents(application_id, uploaded_files):
    """Update the uploaded_documents field for an application"""
    try:
        # Read all records
        rows = []
        with open(current_app.config['COMPREHENSIVE_LOANS_CSV'], 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        
        # Update specific application
        for row in rows:
            if row['application_id'] == application_id:
                row['uploaded_documents'] = ', '.join(uploaded_files)
                row['updated_at'] = datetime.now().isoformat()
                break
        
        # Write back to file
        with open(current_app.config['COMPREHENSIVE_LOANS_CSV'], 'w', newline='', encoding='utf-8') as file:
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
        admin_alerts_csv = os.path.join(current_app.config['CSV_DIR'], "admin_alerts.csv")
        
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
        admin_alerts_csv = os.path.join(current_app.config['CSV_DIR'], "admin_alerts.csv")
        
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
