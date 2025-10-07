# Bank Loan Portal Backend

A Flask-based REST API backend for the Government Bank Loan Portal application.

## Features

- **User Authentication**: Registration and login with JWT tokens
- **Loan Applications**: Submit and manage loan applications
- **Database Integration**: SQLAlchemy with SQLite/PostgreSQL/MySQL support
- **Security**: Password hashing, JWT authentication, CORS protection
- **Validation**: Input validation for all forms and data
- **Government Compliance**: Designed for official government banking portals

## Tech Stack

- **Framework**: Flask 2.3.3
- **Database**: SQLAlchemy (SQLite for development, PostgreSQL/MySQL for production)
- **Authentication**: Flask-JWT-Extended
- **Security**: Flask-Bcrypt, Werkzeug
- **CORS**: Flask-CORS
- **Environment**: python-dotenv

## Installation & Setup

### 1. Clone and Navigate
```bash
cd Backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
cp .env.example .env
# Edit .env file with your configuration
```

### 5. Run the Application
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login

### Loan Applications (Requires Authentication)
- `POST /api/loan-applications` - Submit new loan application
- `GET /api/loan-applications` - Get user's loan applications
- `GET /api/loan-applications/<id>` - Get specific loan application

### Utility
- `GET /api/health` - Health check endpoint

## Database Schema

### Users Table
- `id` - Primary key
- `full_name` - User's full name
- `email` - Email address (unique)
- `phone` - Mobile number
- `aadhaar` - Aadhaar number (unique)
- `password_hash` - Hashed password
- `created_at` - Registration timestamp
- `updated_at` - Last update timestamp

### Loan Applications Table
- `id` - Primary key
- `user_id` - Foreign key to users table
- `application_id` - Unique application identifier
- `name`, `age`, `gender`, `location`, `contact` - Personal information
- `employment_status`, `monthly_income`, `credit_score` - Employment details
- `loan_type`, `loan_amount`, `loan_tenure` - Loan requirements
- `status` - Application status (pending, approved, rejected, under_review)
- `submitted_at` - Application submission time
- `created_at`, `updated_at` - Timestamps

## Request/Response Examples

### User Registration
```bash
POST /api/auth/register
Content-Type: application/json

{
  "fullName": "John Doe",
  "email": "john@example.com",
  "phone": "9876543210",
  "aadhaar": "123456789012",
  "password": "securepassword"
}
```

### User Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword"
}
```

### Submit Loan Application
```bash
POST /api/loan-applications
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "personal": {
    "name": "John Doe",
    "age": 30,
    "gender": "male",
    "location": "Mumbai",
    "contact": "9876543210"
  },
  "employment": {
    "status": "salaried",
    "income": 75000,
    "creditScore": 750
  },
  "loan": {
    "type": "home",
    "amount": 2500000,
    "tenure": "20 years"
  },
  "metadata": {
    "submittedAt": "2025-09-09T10:30:00Z",
    "applicationId": "LOAN-1693908600-ABC123",
    "source": "loan-advisor-dashboard"
  }
}
```

## Security Features

- **Password Hashing**: Bcrypt for secure password storage
- **JWT Authentication**: Secure token-based authentication
- **Input Validation**: Comprehensive validation for all inputs
- **CORS Protection**: Configured for frontend domain
- **SQL Injection Prevention**: SQLAlchemy ORM protections

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | Required |
| `JWT_SECRET_KEY` | JWT signing secret | Required |
| `DATABASE_URL` | Database connection string | `sqlite:///bank_loan_portal.db` |
| `FLASK_ENV` | Flask environment | `development` |
| `FLASK_DEBUG` | Debug mode | `True` |
| `FRONTEND_URL` | Frontend URL for CORS | `http://localhost:3000` |

## Development

### Database Management
The application automatically creates tables on first run. For manual database operations:

```python
from app import app, db

with app.app_context():
    # Create all tables
    db.create_all()
    
    # Drop all tables (caution!)
    db.drop_all()
```

### Adding New Features
1. Define models in `app.py`
2. Add routes with proper validation
3. Update documentation
4. Test endpoints

## Production Deployment

### 1. Use Production Database
Update `DATABASE_URL` in `.env` to use PostgreSQL or MySQL:
```
DATABASE_URL=postgresql://user:password@localhost/bank_loan_portal
```

### 2. Security Configuration
- Change `SECRET_KEY` and `JWT_SECRET_KEY`
- Set `FLASK_ENV=production`
- Set `FLASK_DEBUG=False`
- Use HTTPS in production
- Configure proper CORS origins

### 3. Process Manager
Use Gunicorn for production:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Error Handling

The API returns consistent error responses:
```json
{
  "message": "Error description",
  "error": "Technical details (in development)"
}
```

## Compliance

This backend is designed for government banking applications with:
- Secure user authentication
- Comprehensive audit trails
- Data validation and sanitization
- Privacy-focused data handling
- Scalable architecture for high traffic

## Support

For technical support or feature requests, please check the documentation or contact the development team.
