# backend/app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    
    # Session Cookie Settings
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour

    # IBM Watsonx API
    API_KEY = os.getenv("API_KEY")
    AGENT_ENDPOINT = os.getenv("AGENT_ENDPOINT")
    IAM_ENDPOINT = "https://iam.cloud.ibm.com/identity/token"

    # SMTP Email Configuration
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USERNAME)
    FROM_NAME = os.getenv("FROM_NAME", "AI Banking Portal")

    # CSV File Paths
    CSV_DIR = "data"
    STAFF_CSV = os.path.join(CSV_DIR, "staff.csv")
    LOAN_APPLICATIONS_CSV = os.path.join(CSV_DIR, "loan_applications.csv")
    COMPREHENSIVE_LOANS_CSV = os.path.join(CSV_DIR, "comprehensive_loans.csv")
    USERS_CSV = os.path.join(CSV_DIR, "users.csv")
    CHAT_LOGS_CSV = os.path.join(CSV_DIR, "chat_logs.csv")

    # ... other settings
    OBJECTIONS_CSV = os.path.join(CSV_DIR, "objections.csv")