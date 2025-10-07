# SMTP mailing service for automatic email notifications
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Email configuration (use environment variables for security)
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SMTP_USERNAME = os.environ.get('SMTP_USERNAME', 'your-email@gmail.com')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', 'your-app-password')
FROM_EMAIL = os.environ.get('FROM_EMAIL', SMTP_USERNAME)
FROM_NAME = os.environ.get('FROM_NAME', 'Bank Loan Portal')

def send_email(to_email, subject, body, is_html=False):
    """Send email via SMTP"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = f"{FROM_NAME} <{FROM_EMAIL}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'html' if is_html else 'plain'))
        
        # Create SMTP session
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Enable security
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        
        # Send email
        text = msg.as_string()
        server.sendmail(FROM_EMAIL, to_email, text)
        server.quit()
        
        print(f"✅ Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {str(e)}")
        return False

def get_email_template():
    """Return the base HTML email template with modern styling"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bank of India - Loan Portal</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333333;
                background-color: #f8fafc;
            }
            
            .email-container {
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
                padding: 40px 30px;
                text-align: center;
                position: relative;
            }
            
            .header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
                opacity: 0.3;
            }
            
            .logo {
                position: relative;
                z-index: 2;
            }
            
            .logo h1 {
                color: #ffffff;
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 8px;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            }
            
            .logo p {
                color: #e2e8f0;
                font-size: 14px;
                font-weight: 500;
            }
            
            .content {
                padding: 40px 30px;
            }
            
            .status-badge {
                display: inline-block;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin: 10px 0;
            }
            
            .status-approved {
                background-color: #dcfce7;
                color: #16a34a;
                border: 1px solid #bbf7d0;
            }
            
            .status-rejected {
                background-color: #fef2f2;
                color: #dc2626;
                border: 1px solid #fecaca;
            }
            
            .status-pending {
                background-color: #fef3c7;
                color: #d97706;
                border: 1px solid #fed7aa;
            }
            
            .status-review {
                background-color: #e0f2fe;
                color: #0369a1;
                border: 1px solid #bae6fd;
            }
            
            .info-card {
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 25px;
                margin: 25px 0;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            }
            
            .info-row {
                display: flex;
                justify-content: space-between;
                margin-bottom: 12px;
                padding-bottom: 8px;
                border-bottom: 1px solid #e2e8f0;
            }
            
            .info-row:last-child {
                margin-bottom: 0;
                border-bottom: none;
                padding-bottom: 0;
            }
            
            .info-label {
                font-weight: 600;
                color: #64748b;
                font-size: 14px;
            }
            
            .info-value {
                font-weight: 700;
                color: #1e293b;
                font-size: 14px;
            }
            
            .message-box {
                background: #f0f9ff;
                border-left: 4px solid #0369a1;
                padding: 20px;
                margin: 20px 0;
                border-radius: 0 8px 8px 0;
            }
            
            .document-list {
                background: #fffbeb;
                border: 1px solid #fed7aa;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
            }
            
            .document-list h4 {
                color: #92400e;
                margin-bottom: 15px;
                font-size: 16px;
            }
            
            .document-list ul {
                list-style: none;
                padding: 0;
            }
            
            .document-list li {
                padding: 8px 0;
                color: #78350f;
                position: relative;
                padding-left: 20px;
            }
            
            .document-list li::before {
                content: '📄';
                position: absolute;
                left: 0;
                top: 8px;
            }
            
            .cta-button {
                display: inline-block;
                background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
                color: #ffffff;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
                margin: 20px 0;
                box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
                transition: all 0.3s ease;
            }
            
            .cta-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
            }
            
            .footer {
                background-color: #1e293b;
                color: #94a3b8;
                padding: 30px;
                text-align: center;
            }
            
            .footer-links {
                margin: 20px 0;
            }
            
            .footer-links a {
                color: #60a5fa;
                text-decoration: none;
                margin: 0 15px;
                font-size: 14px;
            }
            
            .social-icons {
                margin: 20px 0;
            }
            
            .divider {
                height: 2px;
                background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
                margin: 30px 0;
            }
            
            @media (max-width: 600px) {
                .email-container {
                    margin: 0;
                    box-shadow: none;
                }
                
                .header, .content, .footer {
                    padding: 25px 20px;
                }
                
                .info-row {
                    flex-direction: column;
                    gap: 5px;
                }
            }
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <div class="logo">
                    <h1>🏛️ Bank of India</h1>
                    <p>Digital Loan Portal - Ministry of Finance</p>
                </div>
            </div>
            
            <div class="content">
                {content}
            </div>
            
            <div class="footer">
                <p><strong>Bank of India - Digital Loan Portal</strong></p>
                <p>Ministry of Finance, Government of India</p>
                
                <div class="footer-links">
                    <a href="#">Help Center</a>
                    <a href="#">Contact Support</a>
                    <a href="#">Privacy Policy</a>
                    <a href="#">Terms of Service</a>
                </div>
                
                <div class="divider"></div>
                
                <p style="font-size: 12px; color: #64748b;">
                    This is an automated message from Bank of India Digital Loan Portal.<br>
                    Please do not reply to this email. For support, visit our help center.
                </p>
                
                <p style="font-size: 11px; color: #475569; margin-top: 15px;">
                    © 2025 Bank of India. All rights reserved. | Government of India
                </p>
            </div>
        </div>
    </body>
    </html>
    """

def send_application_confirmation(user_email, user_name, application_id):
    """Send beautifully designed confirmation email when loan application is submitted"""
    content = f"""
        <h2 style="color: #1e293b; font-size: 24px; margin-bottom: 20px;">
            🎉 Application Submitted Successfully!
        </h2>
        
        <p style="font-size: 16px; color: #475569; margin-bottom: 25px;">
            Dear <strong>{user_name}</strong>,
        </p>
        
        <p style="font-size: 16px; color: #475569; margin-bottom: 25px;">
            Thank you for choosing Bank of India for your loan requirements. Your application has been successfully submitted and is now under review by our expert team.
        </p>
        
        <div class="info-card">
            <div class="info-row">
                <span class="info-label">Application ID</span>
                <span class="info-value">{application_id}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Submitted Date</span>
                <span class="info-value">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Current Status</span>
                <span class="info-value">
                    <span class="status-badge status-review">Under Review</span>
                </span>
            </div>
            <div class="info-row">
                <span class="info-label">Expected Response</span>
                <span class="info-value">3-5 Business Days</span>
            </div>
        </div>
        
        <div class="message-box">
            <h3 style="color: #0369a1; margin-bottom: 15px;">📋 What happens next?</h3>
            <ul style="margin: 0; padding-left: 20px; color: #475569;">
                <li>Our loan officers will review your application within 24 hours</li>
                <li>You may be contacted for additional documentation if required</li>
                <li>We'll notify you of any status updates via email and SMS</li>
                <li>Final decision will be communicated within 3-5 business days</li>
            </ul>
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="http://localhost:3000/application" class="cta-button">
                📊 Track Your Application
            </a>
        </div>
        
        <p style="font-size: 14px; color: #64748b; margin-top: 30px;">
            Need help? Contact our customer support at <strong>1800-XXX-XXXX</strong> or email us at 
            <a href="mailto:support@bankofindia.gov.in" style="color: #3b82f6;">support@bankofindia.gov.in</a>
        </p>
    """
    
    subject = f"✅ Loan Application Confirmed - {application_id}"
    email_body = get_email_template().replace('{content}', content)
    return send_email(user_email, subject, email_body, is_html=True)

def send_document_request(user_email, user_name, application_id, documents_required):
    """Send beautifully designed email requesting additional documents"""
    # Parse documents if it's a string with line breaks
    if isinstance(documents_required, str):
        docs_list = [doc.strip() for doc in documents_required.split('\n') if doc.strip()]
    else:
        docs_list = documents_required
    
    docs_html = '\n'.join([f'<li>{doc}</li>' for doc in docs_list])
    
    content = f"""
        <h2 style="color: #1e293b; font-size: 24px; margin-bottom: 20px;">
            📋 Additional Documents Required
        </h2>
        
        <p style="font-size: 16px; color: #475569; margin-bottom: 25px;">
            Dear <strong>{user_name}</strong>,
        </p>
        
        <p style="font-size: 16px; color: #475569; margin-bottom: 25px;">
            Your loan application <strong>{application_id}</strong> is progressing through our review process. To complete the evaluation, we need some additional documents from you.
        </p>
        
        <div class="info-card">
            <div class="info-row">
                <span class="info-label">Application ID</span>
                <span class="info-value">{application_id}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Current Status</span>
                <span class="info-value">
                    <span class="status-badge status-pending">Documents Pending</span>
                </span>
            </div>
            <div class="info-row">
                <span class="info-label">Deadline</span>
                <span class="info-value">7 Business Days</span>
            </div>
        </div>
        
        <div class="document-list">
            <h4>📄 Required Documents:</h4>
            <ul>
                {docs_html}
            </ul>
        </div>
        
        <div class="message-box">
            <h3 style="color: #0369a1; margin-bottom: 15px;">📤 How to submit documents:</h3>
            <ul style="margin: 0; padding-left: 20px; color: #475569;">
                <li>Log in to your account and upload documents securely</li>
                <li>Ensure all documents are clear and legible</li>
                <li>Submit original documents for verification if requested</li>
                <li>Contact our support team if you need assistance</li>
            </ul>
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="http://localhost:3000/application" class="cta-button">
                📤 Upload Documents
            </a>
        </div>
        
        <p style="font-size: 14px; color: #64748b; margin-top: 30px;">
            <strong>Important:</strong> Please submit the required documents within 7 business days to avoid application delay. 
            For queries, call <strong>1800-XXX-XXXX</strong> or email 
            <a href="mailto:documents@bankofindia.gov.in" style="color: #3b82f6;">documents@bankofindia.gov.in</a>
        </p>
    """
    
    subject = f"📋 Documents Required - Application {application_id}"
    email_body = get_email_template().replace('{content}', content)
    return send_email(user_email, subject, email_body, is_html=True)

def send_application_status_update(user_email, user_name, application_id, status, admin_notes=None):
    """Send beautifully designed email when application status changes"""
    status_configs = {
        'approved': {
            'emoji': '🎉',
            'title': 'Congratulations! Your Loan is Approved',
            'message': 'We are pleased to inform you that your loan application has been approved! Our team will contact you shortly with the next steps.',
            'badge_class': 'status-approved',
            'color': '#16a34a',
            'next_steps': [
                'You will receive loan terms and conditions via email',
                'Our representative will contact you for documentation',
                'Loan disbursement will be processed within 2-3 business days',
                'Track your disbursement status in your account'
            ]
        },
        'rejected': {
            'emoji': '❌',
            'title': 'Application Status Update',
            'message': 'After careful review, we regret to inform you that your loan application does not meet our current lending criteria.',
            'badge_class': 'status-rejected',
            'color': '#dc2626',
            'next_steps': [
                'Review the reasons for rejection below',
                'You may reapply after addressing the mentioned concerns',
                'Contact our support team for guidance on improving your profile',
                'Consider other loan products that might suit your needs'
            ]
        },
        'under_review': {
            'emoji': '🔍',
            'title': 'Application Under Review',
            'message': 'Your loan application is currently being reviewed by our underwriting team. We appreciate your patience.',
            'badge_class': 'status-review',
            'color': '#0369a1',
            'next_steps': [
                'Our team is carefully evaluating your application',
                'Additional verification may be required',
                'You will be notified of any document requirements',
                'Expected decision within 2-3 business days'
            ]
        },
        'documents_pending': {
            'emoji': '📋',
            'title': 'Documents Required',
            'message': 'Your application review is on hold pending the submission of additional documents.',
            'badge_class': 'status-pending',
            'color': '#d97706',
            'next_steps': [
                'Check the documents required section',
                'Upload clear and legible copies',
                'Submit documents within the specified deadline',
                'Contact support if you need assistance'
            ]
        }
    }
    
    config = status_configs.get(status, status_configs['under_review'])
    next_steps_html = '\n'.join([f'<li>{step}</li>' for step in config['next_steps']])
    
    content = f"""
        <h2 style="color: #1e293b; font-size: 24px; margin-bottom: 20px;">
            {config['emoji']} {config['title']}
        </h2>
        
        <p style="font-size: 16px; color: #475569; margin-bottom: 25px;">
            Dear <strong>{user_name}</strong>,
        </p>
        
        <p style="font-size: 16px; color: #475569; margin-bottom: 25px;">
            {config['message']}
        </p>
        
        <div class="info-card">
            <div class="info-row">
                <span class="info-label">Application ID</span>
                <span class="info-value">{application_id}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Status Updated</span>
                <span class="info-value">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Current Status</span>
                <span class="info-value">
                    <span class="status-badge {config['badge_class']}">{status.replace('_', ' ').title()}</span>
                </span>
            </div>
        </div>
    """
    
    if admin_notes:
        content += f"""
        <div class="message-box">
            <h3 style="color: #0369a1; margin-bottom: 15px;">💬 Additional Information:</h3>
            <p style="color: #475569; font-style: italic; line-height: 1.6;">
                "{admin_notes}"
            </p>
        </div>
        """
    
    content += f"""
        <div class="message-box">
            <h3 style="color: #0369a1; margin-bottom: 15px;">📋 Next Steps:</h3>
            <ul style="margin: 0; padding-left: 20px; color: #475569;">
                {next_steps_html}
            </ul>
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="http://localhost:3000/application" class="cta-button">
                📊 View Application Details
            </a>
        </div>
        
        <p style="font-size: 14px; color: #64748b; margin-top: 30px;">
            For any questions or concerns, please contact our customer support at <strong>1800-XXX-XXXX</strong> or 
            email us at <a href="mailto:support@bankofindia.gov.in" style="color: #3b82f6;">support@bankofindia.gov.in</a>
        </p>
    """
    
    subject = f"{config['emoji']} Application Update - {application_id}"
    email_body = get_email_template().replace('{content}', content)
    return send_email(user_email, subject, email_body, is_html=True)

def send_admin_notification(admin_email, user_name, application_id, action):
    """Send professional notification to admin about new applications or updates"""
    action_configs = {
        'submitted': {
            'emoji': '📝',
            'title': 'New Loan Application Submitted',
            'priority': 'Normal',
            'color': '#3b82f6'
        },
        'updated': {
            'emoji': '🔄',
            'title': 'Application Updated',
            'priority': 'Low',
            'color': '#6b7280'
        },
        'requires_review': {
            'emoji': '⚠️',
            'title': 'Application Requires Review',
            'priority': 'High',
            'color': '#f59e0b'
        },
        'documents_uploaded': {
            'emoji': '📤',
            'title': 'Documents Uploaded',
            'priority': 'Normal',
            'color': '#10b981'
        }
    }
    
    config = action_configs.get(action, action_configs['submitted'])
    
    content = f"""
        <h2 style="color: #1e293b; font-size: 24px; margin-bottom: 20px;">
            {config['emoji']} {config['title']}
        </h2>
        
        <p style="font-size: 16px; color: #475569; margin-bottom: 25px;">
            Dear Admin,
        </p>
        
        <p style="font-size: 16px; color: #475569; margin-bottom: 25px;">
            A loan application requires your attention in the admin portal.
        </p>
        
        <div class="info-card">
            <div class="info-row">
                <span class="info-label">Application ID</span>
                <span class="info-value">{application_id}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Applicant Name</span>
                <span class="info-value">{user_name}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Action Required</span>
                <span class="info-value">{action.replace('_', ' ').title()}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Priority Level</span>
                <span class="info-value">
                    <span class="status-badge" style="background-color: {config['color']}20; color: {config['color']}; border: 1px solid {config['color']}40;">
                        {config['priority']}
                    </span>
                </span>
            </div>
            <div class="info-row">
                <span class="info-label">Timestamp</span>
                <span class="info-value">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</span>
            </div>
        </div>
        
        <div class="message-box">
            <h3 style="color: #0369a1; margin-bottom: 15px;">🎯 Quick Actions Available:</h3>
            <ul style="margin: 0; padding-left: 20px; color: #475569;">
                <li>Review application details and documentation</li>
                <li>Approve, reject, or request additional documents</li>
                <li>Add admin notes for internal tracking</li>
                <li>Send status updates to the applicant</li>
            </ul>
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="http://localhost:3000/admin" class="cta-button">
                🛡️ Open Admin Portal
            </a>
        </div>
        
        <p style="font-size: 14px; color: #64748b; margin-top: 30px;">
            This is an automated notification from the Bank Loan Portal System. 
            Please ensure timely review to maintain service quality standards.
        </p>
    """
    
    subject = f"{config['emoji']} Admin Alert - {action.replace('_', ' ').title()} - {application_id}"
    email_body = get_email_template().replace('{content}', content)
    return send_email(admin_email, subject, email_body, is_html=True)
