# backend/app/services/notification_service.py file

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from flask import current_app

# Import the function to save logs from our CSV handler
from ..utils.csv_handler import save_notification_log


def create_html_email_template(title, content, cta_text=None, cta_link=None, alert_type="info"):
    """Create a standardized, professional HTML email template."""
    # ... (This is the full function from your agent.py file) ...
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
                
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px 20px; text-align: center;">
                    <h1 style="margin: 0; font-size: 28px; font-weight: 600;">🏦 AI Banking Portal</h1>
                    <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">Powered by Watson AI Technology</p>
                </div>
                
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


def send_email_notification(to_email, subject, message, notification_type='info', html_content=None):
    """Send email notification using SMTP settings from the central config."""
    # Get all SMTP settings from the central config file
    smtp_user = current_app.config['SMTP_USERNAME']
    smtp_pass = current_app.config['SMTP_PASSWORD']
    
    if not (smtp_user and smtp_pass):
        print("\n" + "="*60)
        print(f"EMAIL NOTIFICATION [LOGGED - SMTP NOT CONFIGURED]")
        print(f"To: {to_email}\nSubject: {subject}\nMessage:\n{message}")
        print("="*60 + "\n")
        save_notification_log(to_email, subject, message, notification_type)
        return True

    msg = MIMEMultipart('alternative')
    msg['From'] = f"{current_app.config['FROM_NAME']} <{current_app.config['FROM_EMAIL']}>"
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain', 'utf-8'))
    if html_content:
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(current_app.config['SMTP_SERVER'], current_app.config['SMTP_PORT']) as server:
            server.starttls(context=context)
            server.login(smtp_user, smtp_pass)
            server.sendmail(current_app.config['FROM_EMAIL'], to_email, msg.as_string())
        print(f"✅ Email sent successfully to {to_email}: {subject}")
        save_notification_log(to_email, subject, message, notification_type)
        return True
    except Exception as e:
        print(f"❌ Email notification error: {e}")
        save_notification_log(to_email, subject, message, f"{notification_type}_error")
        return False


def send_objection_notification(user_email, app_id, reason, requested_docs):
    """Send objection notification email to user"""
    subject = f"📋 Document Resubmission Required - Application {app_id}"
    apply_link = "http://127.0.0.1:5001/apply.html" # This could also be moved to config
    
    message = f"""
    Dear Applicant,
    We have reviewed your loan application {app_id} and require additional information.
    OBJECTION DETAILS: {reason}
    REQUESTED DOCUMENTS: {requested_docs}
    Please visit the portal to resubmit: {apply_link}
    """
    
    html_content = create_html_email_template(
        title=f"Action Required for Application {app_id}",
        content=f"""We have reviewed your loan application and require additional information to proceed.
        
        <strong style="color: #92400e;">Reason for Objection:</strong><br>{reason}
        <br><br>
        <strong style="color: #0c4a6e;">Requested Documents:</strong><br>{requested_docs}
        
        Please log in to your dashboard to upload the required documents and resubmit your application.
        """,
        cta_text="Access Application Portal",
        cta_link=apply_link,
        alert_type="warning"
    )
    
    return send_email_notification(user_email, subject, message, 'objection', html_content)