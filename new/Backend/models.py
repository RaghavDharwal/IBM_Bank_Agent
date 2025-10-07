from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    aadhaar = db.Column(db.String(12), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships with explicit foreign keys to avoid ambiguity
    loan_applications = db.relationship('LoanApplication', 
                                      foreign_keys='LoanApplication.user_id',
                                      backref='user', lazy=True)
    reviewed_applications = db.relationship('LoanApplication',
                                           foreign_keys='LoanApplication.reviewed_by',
                                           backref='reviewer', lazy=True)

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'aadhaar': self.aadhaar,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class LoanApplication(db.Model):
    __tablename__ = 'loan_applications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    application_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    employment_status = db.Column(db.String(50), nullable=False)
    monthly_income = db.Column(db.Integer, nullable=False)
    credit_score = db.Column(db.Integer, nullable=False)
    loan_type = db.Column(db.String(50), nullable=False)
    loan_amount = db.Column(db.Integer, nullable=False)
    loan_tenure = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='pending')
    admin_notes = db.Column(db.Text, nullable=True)  # Admin comments
    documents_required = db.Column(db.Text, nullable=True)  # Documents admin requested
    documents_uploaded = db.Column(db.Boolean, default=False)  # Whether user uploaded docs
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Admin who reviewed
    reviewed_at = db.Column(db.DateTime, nullable=True)
    submitted_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'application_id': self.application_id,
            'user_id': self.user_id,
            'personal': {
                'name': self.name,
                'age': self.age,
                'gender': self.gender,
                'location': self.location,
                'contact': self.contact
            },
            'employment': {
                'status': self.employment_status,
                'income': self.monthly_income,
                'credit_score': self.credit_score
            },
            'loan': {
                'type': self.loan_type,
                'amount': self.loan_amount,
                'tenure': self.loan_tenure
            },
            'status': self.status,
            'admin_notes': self.admin_notes,
            'documents_required': self.documents_required,
            'documents_uploaded': self.documents_uploaded,
            'reviewed_by': self.reviewed_by,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
