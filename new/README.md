# 🏦 Bank of India Loan Portal

A comprehensive loan management system built with Flask (Backend) and Next.js (Frontend), featuring modern UI, admin dashboard, and production-ready deployment configurations.

![Bank Portal](https://img.shields.io/badge/Status-Production%20Ready-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Node.js](https://img.shields.io/badge/Node.js-18+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🏛️ Project Overview

This is a comprehensive Bank Loan Portal application for the Government of India's Bank of India, designed to:

- Provide citizens with easy access to government loan schemes
- Streamline the loan application process
- Offer AI-powered suggestions and recommendations
- Maintain security and compliance with government standards
- Support multiple loan types (MUDRA, PMEGP, Education, Home, etc.)

## 🏗️ Architecture

```
Bank-Loan-Portal/
├── AI-agent-Frontend/     # Next.js Frontend Application
│   ├── app/              # Next.js 13+ App Router
│   ├── components/       # React Components
│   ├── public/          # Static Assets
│   └── styles/          # CSS Styles
└── Backend/             # Flask REST API Backend
    ├── app.py           # Main Flask Application
    ├── requirements.txt # Python Dependencies
    └── test_api.py      # API Testing Script
```

## 🚀 Quick Start

### Prerequisites
- **Node.js 18+** for frontend
- **Python 3.7+** for backend
- **pnpm** (recommended) or npm for frontend package management

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Bank-Loan-Portal
```

### 2. Start Backend (Terminal 1)
```bash
cd Backend
chmod +x start.sh
./start.sh
```

Or manually:
```bash
cd Backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The backend will start at `http://localhost:5001`

### 3. Start Frontend (Terminal 2)
```bash
cd AI-agent-Frontend
chmod +x start.sh
./start.sh
```

Or manually:
```bash
cd AI-agent-Frontend
pnpm install
pnpm dev
```

The frontend will start at `http://localhost:3000`

### 4. Test the Application
```bash
cd Backend
python test_api.py
```

## 📱 Application Features

### Frontend Features
- **Modern UI/UX**: Government-compliant design with professional styling
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Multi-step Forms**: Progressive loan application process
- **AI Suggestions**: Real-time recommendations based on user data
- **Authentication**: Secure login/registration system
- **Loan Schemes**: Comprehensive overview of government loan programs

### Backend Features
- **RESTful API**: Clean, documented API endpoints
- **User Authentication**: JWT-based secure authentication
- **Database Integration**: SQLAlchemy with SQLite (development) / PostgreSQL (production)
- **Input Validation**: Comprehensive data validation and sanitization
- **Security**: Password hashing, CORS protection, SQL injection prevention
- **Scalable Architecture**: Designed for high-traffic government applications

## 🔐 Authentication Flow

1. **Registration**: User creates account with personal details and Aadhaar
2. **Login**: User authenticates with email/password
3. **JWT Token**: Backend provides secure token for API access
4. **Protected Routes**: Frontend protects application pages
5. **Logout**: Clean session termination

## 📊 Database Schema

### Users Table
- Personal information (name, email, phone, Aadhaar)
- Secure password storage
- Account timestamps

### Loan Applications Table
- Complete application data
- User relationship
- Application status tracking
- Audit timestamps

## 🛡️ Security Features

- **Password Hashing**: Bcrypt for secure password storage
- **JWT Authentication**: Stateless token-based authentication
- **Input Validation**: Server-side validation for all inputs
- **CORS Protection**: Configured for specific origins
- **SQL Injection Prevention**: SQLAlchemy ORM protection
- **Government Compliance**: Designed for official government portals

## 🤖 AI Features

- **Smart Suggestions**: Context-aware recommendations
- **Eligibility Checks**: Real-time eligibility validation
- **Scheme Matching**: Automatic government scheme recommendations
- **Credit Score Analysis**: Personalized advice based on credit scores
- **Income-based Suggestions**: Tailored loan options

## 📋 Government Loan Schemes

1. **MUDRA Loan** - Up to ₹10 Lakhs for small businesses
2. **PMEGP Scheme** - Up to ₹25 Lakhs for entrepreneurs
3. **Education Loan** - Up to ₹1.5 Crores for studies
4. **PM Awas Yojana** - Up to ₹12 Lakhs for housing
5. **Kisan Credit Card** - Agricultural loans for farmers
6. **Stand-Up India** - ₹10 Lakhs - ₹1 Crore for inclusive growth

## 🔧 Development

### Frontend Development
```bash
cd AI-agent-Frontend
pnpm dev          # Start development server
pnpm build        # Build for production
pnpm lint         # Run linting
```

### Backend Development
```bash
cd Backend
python app.py     # Start development server
python test_api.py # Run API tests
```

### Database Management
```python
# In Python shell
from app import app, db
with app.app_context():
    db.create_all()  # Create tables
    db.drop_all()    # Drop tables (caution!)
```

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### Loan Applications (Authenticated)
- `POST /api/loan-applications` - Submit application
- `GET /api/loan-applications` - Get user's applications
- `GET /api/loan-applications/<id>` - Get specific application

### Utility
- `GET /api/health` - Health check

## 📦 Dependencies

### Frontend
- **Next.js 15.2.4** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Radix UI** - Accessible components
- **React Hook Form** - Form management
- **Zod** - Schema validation

### Backend
- **Flask 2.3.3** - Web framework
- **SQLAlchemy** - Database ORM
- **Flask-JWT-Extended** - JWT authentication
- **Flask-Bcrypt** - Password hashing
- **Flask-CORS** - Cross-origin requests

## 🚀 Production Deployment

### Frontend Deployment
1. Build the application: `pnpm build`
2. Deploy to Vercel, Netlify, or similar platform
3. Configure environment variables
4. Set backend API URL

### Backend Deployment
1. Use production database (PostgreSQL/MySQL)
2. Set environment variables
3. Use Gunicorn for WSGI server
4. Configure reverse proxy (Nginx)
5. Set up SSL certificates

### Environment Variables

#### Backend (.env)
```
SECRET_KEY=your-production-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=postgresql://user:password@host/database
FLASK_ENV=production
```

#### Frontend
```
NEXT_PUBLIC_API_URL=https://your-backend-domain.com
```

## 🧪 Testing

### Backend Testing
```bash
cd Backend
python test_api.py
```

### Frontend Testing
```bash
cd AI-agent-Frontend
pnpm test  # If test suite is configured
```

## 📞 Support & Documentation

### User Journey
1. **Home Page**: Overview of loan schemes and portal information
2. **Registration**: Create new citizen account
3. **Login**: Authenticate with credentials
4. **Application**: Complete multi-step loan application
5. **AI Assistance**: Receive personalized recommendations
6. **Submission**: Submit application and receive confirmation

### Troubleshooting
- **Backend not starting**: Check Python version and dependencies
- **Frontend not loading**: Verify Node.js version and run `pnpm install`
- **API errors**: Check backend logs and test endpoints
- **Authentication issues**: Verify JWT token and user data

### Contact
For technical support or questions about this government portal application, please refer to the documentation in each module or contact the development team.

## 🏛️ Government Compliance

This application is designed to meet government standards for:
- **Security**: Industry-standard encryption and authentication
- **Accessibility**: WCAG 2.1 AA compliance
- **Performance**: Optimized for high traffic and government infrastructure
- **Audit Trail**: Complete logging and data tracking
- **Privacy**: Secure handling of citizen data

---

**Built for the Government of India's Digital India Initiative**
**Bank of India - Ministry of Finance Loan Portal**
