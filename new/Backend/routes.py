from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from models import db, User, LoanApplication
from helpers import validate_email, validate_phone, validate_aadhaar, admin_required, get_current_user
from smtp_mailing import (send_application_confirmation, send_document_request, 
                         send_application_status_update, send_admin_notification)

routes = Blueprint('routes', __name__)

@routes.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        required_fields = ['fullName', 'email', 'phone', 'aadhaar', 'password']
        for field in required_fields:
            if field not in data or not data[field].strip():
                return jsonify({'message': f'{field} is required'}), 400
        if not validate_email(data['email']):
            return jsonify({'message': 'Invalid email format'}), 400
        if not validate_phone(data['phone']):
            return jsonify({'message': 'Phone number must be 10 digits'}), 400
        if not validate_aadhaar(data['aadhaar']):
            return jsonify({'message': 'Aadhaar number must be 12 digits'}), 400
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already registered'}), 400
        if User.query.filter_by(aadhaar=data['aadhaar']).first():
            return jsonify({'message': 'Aadhaar number already registered'}), 400
        user = User(
            full_name=data['fullName'].strip(),
            email=data['email'].strip().lower(),
            phone=data['phone'].strip(),
            aadhaar=data['aadhaar'].strip(),
            role=data.get('role', 'user')  # Allow admin creation
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully', 'user': user.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Registration failed: {str(e)}', 'error': str(e)}), 500

@routes.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Email and password are required'}), 400
        user = User.query.filter_by(email=data['email'].strip().lower()).first()
        if not user or not user.check_password(data['password']):
            return jsonify({'message': 'Invalid email or password'}), 401
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'message': 'Login successful', 'token': access_token, 'user': user.to_dict()}), 200
    except Exception as e:
        return jsonify({'message': f'Login failed: {str(e)}', 'error': str(e)}), 500

@routes.route('/api/loan-applications', methods=['POST'])
@jwt_required()
def submit_loan_application():
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        required_sections = ['personal', 'employment', 'loan', 'metadata']
        for section in required_sections:
            if section not in data:
                return jsonify({'message': f'{section} data is required'}), 400
        personal = data['personal']
        employment = data['employment']
        loan = data['loan']
        metadata = data['metadata']
        loan_application = LoanApplication(
            user_id=current_user_id,
            application_id=metadata.get('applicationId', f'LOAN-{datetime.now().timestamp()}'),
            name=personal['name'],
            age=personal['age'],
            gender=personal['gender'],
            location=personal['location'],
            contact=personal['contact'],
            employment_status=employment['status'],
            monthly_income=employment['income'],
            credit_score=employment['creditScore'],
            loan_type=loan['type'],
            loan_amount=loan['amount'],
            loan_tenure=loan['tenure'],
            submitted_at=datetime.fromisoformat(metadata['submittedAt'].replace('Z', '+00:00'))
        )
        db.session.add(loan_application)
        db.session.commit()
        
        # Get current user for email notifications
        current_user = User.query.get(current_user_id)
        
        # Send confirmation email to user
        send_application_confirmation(
            current_user.email, 
            current_user.full_name, 
            loan_application.application_id
        )
        
        # Notify admins about new application
        admin_users = User.query.filter_by(role='admin').all()
        for admin in admin_users:
            send_admin_notification(
                admin.email,
                current_user.full_name,
                loan_application.application_id,
                "submitted"
            )
        
        return jsonify({'message': 'Loan application submitted successfully', 'application': loan_application.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to submit loan application', 'error': str(e)}), 500

@routes.route('/api/loan-applications', methods=['GET'])
@jwt_required()
def get_loan_applications():
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        # Add filtering options
        status = request.args.get('status')
        loan_type = request.args.get('loan_type')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        if current_user.role == 'admin':
            # Admins can view all applications
            query = LoanApplication.query
        else:
            # Users can only view their own applications
            query = LoanApplication.query.filter_by(user_id=current_user_id)
        
        # Apply filters
        if status:
            query = query.filter_by(status=status)
        if loan_type:
            query = query.filter_by(loan_type=loan_type)
        
        # Order by creation date (newest first)
        query = query.order_by(LoanApplication.created_at.desc())
        
        # Paginate results
        applications = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'applications': [app.to_dict() for app in applications.items],
            'total': applications.total,
            'pages': applications.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
    except Exception as e:
        return jsonify({'message': 'Failed to fetch applications', 'error': str(e)}), 500

@routes.route('/api/loan-applications/<int:application_id>', methods=['GET'])
@jwt_required()
def get_loan_application(application_id):
    try:
        current_user_id = int(get_jwt_identity())
        application = LoanApplication.query.filter_by(id=application_id, user_id=current_user_id).first()
        if not application:
            return jsonify({'message': 'Application not found'}), 404
        return jsonify({'application': application.to_dict()}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to fetch application', 'error': str(e)}), 500

@routes.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200

# Admin Routes
@routes.route('/api/admin/applications', methods=['GET'])
@jwt_required()
@admin_required
def admin_get_all_applications():
    """Admin endpoint to get all applications with advanced filtering"""
    try:
        # Get filtering parameters
        status = request.args.get('status')
        loan_type = request.args.get('loan_type')
        user_id = request.args.get('user_id')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        query = LoanApplication.query
        
        # Apply filters
        if status:
            query = query.filter_by(status=status)
        if loan_type:
            query = query.filter_by(loan_type=loan_type)
        if user_id:
            query = query.filter_by(user_id=user_id)
        if date_from:
            query = query.filter(LoanApplication.submitted_at >= datetime.fromisoformat(date_from))
        if date_to:
            query = query.filter(LoanApplication.submitted_at <= datetime.fromisoformat(date_to))
        
        # Order by submission date (newest first)
        query = query.order_by(LoanApplication.submitted_at.desc())
        
        # Paginate results
        applications = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Include user details in admin view
        result = []
        for app in applications.items:
            app_dict = app.to_dict()
            app_dict['user_details'] = app.user.to_dict()
            result.append(app_dict)
        
        return jsonify({
            'applications': result,
            'total': applications.total,
            'pages': applications.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
    except Exception as e:
        return jsonify({'message': 'Failed to fetch applications', 'error': str(e)}), 500

@routes.route('/api/admin/applications/<int:application_id>/request-documents', methods=['POST'])
@jwt_required()
@admin_required
def admin_request_documents(application_id):
    """Admin endpoint to request additional documents from user"""
    try:
        data = request.get_json()
        documents_required = data.get('documents_required')
        admin_notes = data.get('admin_notes', '')
        
        if not documents_required:
            return jsonify({'message': 'Documents required field is mandatory'}), 400
        
        application = LoanApplication.query.get(application_id)
        if not application:
            return jsonify({'message': 'Application not found'}), 404
        
        current_admin = get_current_user()
        
        # Update application
        application.status = 'documents_pending'
        application.documents_required = documents_required
        application.admin_notes = admin_notes
        application.reviewed_by = current_admin.id
        application.reviewed_at = datetime.utcnow()
        
        db.session.commit()
        
        # Send email to user
        send_document_request(
            application.user.email,
            application.user.full_name,
            application.application_id,
            documents_required
        )
        
        return jsonify({
            'message': 'Document request sent successfully',
            'application': application.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to request documents', 'error': str(e)}), 500

@routes.route('/api/admin/applications/<int:application_id>/approve', methods=['POST'])
@jwt_required()
@admin_required
def admin_approve_application(application_id):
    """Admin endpoint to approve or reject application"""
    try:
        data = request.get_json()
        new_status = data.get('status')  # 'approved' or 'rejected'
        admin_notes = data.get('admin_notes', '')
        
        if new_status not in ['approved', 'rejected']:
            return jsonify({'message': 'Invalid status. Must be approved or rejected'}), 400
        
        application = LoanApplication.query.get(application_id)
        if not application:
            return jsonify({'message': 'Application not found'}), 404
        
        current_admin = get_current_user()
        
        # Update application
        application.status = new_status
        application.admin_notes = admin_notes
        application.reviewed_by = current_admin.id
        application.reviewed_at = datetime.utcnow()
        
        db.session.commit()
        
        # Send email to user
        send_application_status_update(
            application.user.email,
            application.user.full_name,
            application.application_id,
            new_status,
            admin_notes
        )
        
        return jsonify({
            'message': f'Application {new_status} successfully',
            'application': application.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to {new_status} application', 'error': str(e)}), 500

@routes.route('/api/admin/applications/<int:application_id>/update-status', methods=['POST'])
@jwt_required()
@admin_required
def admin_update_application_status(application_id):
    """Admin endpoint to update application status with notes"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        admin_notes = data.get('admin_notes', '')
        
        valid_statuses = ['pending', 'under_review', 'documents_pending', 'approved', 'rejected']
        if new_status not in valid_statuses:
            return jsonify({'message': f'Invalid status. Must be one of: {valid_statuses}'}), 400
        
        application = LoanApplication.query.get(application_id)
        if not application:
            return jsonify({'message': 'Application not found'}), 404
        
        current_admin = get_current_user()
        
        # Update application
        application.status = new_status
        application.admin_notes = admin_notes
        application.reviewed_by = current_admin.id
        application.reviewed_at = datetime.utcnow()
        
        db.session.commit()
        
        # Send email to user
        send_application_status_update(
            application.user.email,
            application.user.full_name,
            application.application_id,
            new_status,
            admin_notes
        )
        
        return jsonify({
            'message': 'Application status updated successfully',
            'application': application.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update application status', 'error': str(e)}), 500

@routes.route('/api/admin/dashboard-stats', methods=['GET'])
@jwt_required()
@admin_required
def admin_dashboard_stats():
    """Admin endpoint to get dashboard statistics"""
    try:
        # Get application counts by status
        stats = {
            'total_applications': LoanApplication.query.count(),
            'pending_applications': LoanApplication.query.filter_by(status='pending').count(),
            'under_review': LoanApplication.query.filter_by(status='under_review').count(),
            'documents_pending': LoanApplication.query.filter_by(status='documents_pending').count(),
            'approved_applications': LoanApplication.query.filter_by(status='approved').count(),
            'rejected_applications': LoanApplication.query.filter_by(status='rejected').count(),
            'total_users': User.query.filter_by(role='user').count(),
        }
        
        # Get recent applications (last 5)
        recent_applications = LoanApplication.query.order_by(
            LoanApplication.submitted_at.desc()
        ).limit(5).all()
        
        stats['recent_applications'] = [app.to_dict() for app in recent_applications]
        
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'message': 'Failed to fetch dashboard stats', 'error': str(e)}), 500

@routes.app_errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

@routes.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'message': 'Internal server error'}), 500