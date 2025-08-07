# AI-Powered Banking Portal with Watson Integration

This is a comprehensive banking portal featuring Watson AI-powered loan assessment, SMTP email notifications, document management, and admin verification workflows.

## 🚀 Features

- **🤖 LoanBot Chatbot**: AI-powered conversational interface for banking queries and support
- **💼 Comprehensive Loan Application**: Advanced multi-step loan application with real-time validation
- **👩‍💼 Staff Portal**: Secure administrative dashboard for loan review and management
- **Watson AI Integration**: Intelligent loan eligibility assessment with real-time analysis
- **SMTP Email System**: Professional HTML email notifications for all application statuses
- **Document Management**: Secure file upload and verification system
- **User Dashboard**: Real-time application tracking and document upload
- **Multi-Authentication**: Separate login systems for users and administrators
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🎯 Application Structure

### 1. **LoanBot Interface** (`/` - index.html)
- AI-powered chatbot for banking queries
- Quick action buttons for common questions  
- Real-time chat with Watson AI integration
- Navigation to other application sections

### 2. **Loan Application Portal** (`/apply` - apply.html)
- User registration and authentication
- Comprehensive loan application form
- Real-time AI eligibility assessment
- Document upload capabilities
- Application status tracking

### 3. **Staff Administration** (`/staff` - staff.html)
- Secure staff login portal
- Application review and approval workflow
- Document verification interface
- Email notification management
- Analytics and reporting dashboard

## 📁 Project Structure

```
IBM_Bank_Agent/
├── backend/
│   ├── agent.py              # Flask server with Watson AI and SMTP
│   ├── requirements.txt      # Python dependencies
│   └── .env                  # Environment configuration (create from template)
├── frontend/
│   ├── index.html            # LoanBot - AI chatbot interface
│   ├── staff.html            # Staff login and admin portal
│   ├── apply.html            # Loan application form
├── .env.template            # SMTP configuration template
├── WATSON_AI_GUIDE.md      # Complete implementation guide
└── ReadMe.md               # This file
```

## 🛠️ Setup Instructions

### 1. Prerequisites

- Python 3.8 or newer
- Git
- Email account with SMTP access (Gmail, Outlook, Yahoo, etc.)

### 2. Clone the Repository

```bash
git clone <your-repository-url>
cd IBM_Bank_Agent
```

### 3. Backend Setup

#### a. Navigate to backend directory:
```bash
cd backend
```

#### b. Create and activate virtual environment:

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

#### c. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. SMTP Email Configuration

#### a. Copy the environment template:
```bash
cp ../.env.template .env
```

#### b. Edit the `.env` file with your email settings:

**For Gmail:**
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
BANK_EMAIL=your-bank-email@gmail.com
BANK_NAME=AI Banking Portal
```

**Gmail Setup Steps:**
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password: [Gmail App Passwords](https://support.google.com/accounts/answer/185833)
3. Use the App Password (not your regular password) in `SMTP_PASSWORD`

**For Outlook/Hotmail:**
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your-email@outlook.com
SMTP_PASSWORD=your-password
```

**For Yahoo:**
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USERNAME=your-email@yahoo.com
SMTP_PASSWORD=your-app-password
```

### 5. Start the Application

```bash
python agent.py
```

The application will be available at: `http://127.0.0.1:5001/`

## 🎯 How to Use

### For Loan Applicants:

1. **Register/Login**: Create an account or login with existing credentials
2. **Complete Application**: Fill out the comprehensive loan application form
3. **Watson AI Assessment**: Get instant AI-powered eligibility assessment
4. **Upload Documents**: Submit required documents based on AI recommendations
5. **Track Progress**: Monitor application status in your dashboard
6. **Email Notifications**: Receive HTML email updates on application progress

### For Administrators:

1. **Admin Login**: Access the staff portal with admin credentials
2. **Review Applications**: View all pending loan applications with documents
3. **Watson AI Insights**: See AI assessment results and recommendations
4. **Make Decisions**: Approve, reject, or request revisions
5. **Send Notifications**: Automatic HTML email notifications to applicants

## 📧 Email System Features

- **HTML Email Templates**: Professional, responsive email design
- **Application Status Updates**: Automatic notifications for all status changes
- **Document Requests**: Specific instructions for missing documents
- **Admin Notifications**: Alerts for new applications and uploads
- **Secure SMTP**: SSL/TLS encryption for email transmission
- **Fallback Logging**: Emails logged when SMTP is not configured

## 🔧 Configuration Options

### Environment Variables (.env file):

```env
# SMTP Email Settings
SMTP_SERVER=your-smtp-server
SMTP_PORT=587
SMTP_USERNAME=your-email@domain.com
SMTP_PASSWORD=your-app-password
BANK_EMAIL=bank@domain.com
BANK_NAME=Your Bank Name

# Watson AI Settings (optional)
WATSON_API_KEY=your-watson-key
WATSON_URL=your-watson-url
```

### Default Credentials:

- **Admin Login**: admin@bank.com / admin123
- **Test User**: user@test.com / password123

## 🔍 Troubleshooting

### SMTP Issues:

1. **Gmail "Less secure apps"**: Use App Passwords instead of regular password
2. **Outlook authentication**: Ensure 2FA is enabled and use app-specific password
3. **Port issues**: Try port 465 with SSL if 587 with STARTTLS doesn't work
4. **Firewall**: Ensure outgoing SMTP ports are not blocked

### Application Issues:

1. **Port already in use**: Change the port in agent.py or kill existing process
2. **Dependencies**: Ensure all packages in requirements.txt are installed
3. **CSV files**: Application creates necessary CSV files automatically
4. **File uploads**: Ensure proper permissions for file upload directory

## 🎨 Customization

- **Bank Name**: Update `BANK_NAME` in .env file
- **Email Templates**: Modify `create_html_email_template()` function in agent.py
- **UI Theme**: Edit CSS styles in frontend files
- **Watson AI Rules**: Customize assessment logic in `assess_loan_eligibility()` function

## 📋 Database Schema

The application uses CSV files for data storage:

- `users.csv`: User authentication and profile data
- `comprehensive_loans.csv`: Loan application details
- `document_uploads.csv`: File upload tracking
- `user_alerts.csv`: User notification system
- `admin_alerts.csv`: Administrator notifications
- `notifications.csv`: Email notification log

## 🔒 Security Features

- Password hashing with bcrypt
- Session-based authentication
- File upload validation
- SQL injection prevention
- CSRF protection
- Secure email transmission with SSL/TLS

## 📈 Watson AI Assessment

The system includes intelligent loan assessment based on:

- Income-to-loan ratio analysis
- Credit score evaluation
- Employment stability check
- Debt-to-income ratio
- Loan-to-value ratio for secured loans
- Age and experience factors

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For support and questions:

1. Check the troubleshooting section
2. Review the WATSON_AI_GUIDE.md for detailed implementation info
3. Create an issue in the repository
4. Contact the development team

---

**Note**: This application is designed for educational and demonstration purposes. For production use, implement additional security measures, use a proper database, and follow banking compliance requirements.

On Windows:

python -m venv venv
.\venv\Scripts\activate

On macOS / Linux:

python3 -m venv venv
source venv/bin/activate

Your terminal prompt should now show (venv) at the beginning.

c. Install Python dependencies:

pip install -r requirements.txt

d. Create the environment variables file:
Create a new file named .env inside the backend folder. This file will store your secret credentials. Add the following content to it:

API_KEY="your-real-ibm-cloud-api-key"
AGENT_ENDPOINT="your-watsonx-agent-deployment-url"

Important: Replace the placeholder text with your actual IBM Cloud API Key and your Watsonx Agent's deployment URL.

3. Running the Application
To run the application, you need to start both the backend server and the frontend interface.

a. Start the Backend Server:
Make sure you are in the backend directory and your virtual environment is activated. Then, run the following command:

python agent.py

The server will start, and you should see output indicating it's running on http://127.0.0.1:5000. Keep this terminal window open.

b. Launch the Frontend:
Open a new terminal or use your computer's file explorer to navigate to the frontend directory. Double-click the index.html file. This will open the chat application in your default web browser.

You can now start chatting with your virtual banking assistant!
# thank you