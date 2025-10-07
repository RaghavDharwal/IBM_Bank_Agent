#!/usr/bin/env python3
"""
Test script for Bank Loan Portal Backend API
Run this script to test all API endpoints
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5001"
API_BASE = f"{BASE_URL}/api"

# Test data
test_user = {
    "fullName": "Test User",
    "email": "test@example.com",
    "phone": "9876543210",
    "aadhaar": "123456789012",
    "password": "testpassword123"
}

test_loan_application = {
    "personal": {
        "name": "Test User",
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
        "submittedAt": datetime.now().isoformat() + "Z",
        "applicationId": f"LOAN-{int(time.time())}-TEST123",
        "source": "loan-advisor-dashboard"
    }
}

def print_response(response, description):
    """Print formatted response"""
    print(f"\n{'='*50}")
    print(f"TEST: {description}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_health_check():
    """Test health check endpoint"""
    try:
        response = requests.get(f"{API_BASE}/health")
        print_response(response, "Health Check")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_user_registration():
    """Test user registration"""
    try:
        response = requests.post(
            f"{API_BASE}/auth/register",
            json=test_user,
            headers={'Content-Type': 'application/json'}
        )
        print_response(response, "User Registration")
        return response.status_code == 201
    except Exception as e:
        print(f"Registration failed: {e}")
        return False

def test_user_login():
    """Test user login and return token"""
    try:
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        response = requests.post(
            f"{API_BASE}/auth/login",
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        print_response(response, "User Login")
        
        if response.status_code == 200:
            return response.json().get('token')
        return None
    except Exception as e:
        print(f"Login failed: {e}")
        return None

def test_loan_application_submission(token):
    """Test loan application submission"""
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        response = requests.post(
            f"{API_BASE}/loan-applications",
            json=test_loan_application,
            headers=headers
        )
        print_response(response, "Loan Application Submission")
        
        if response.status_code == 201:
            return response.json().get('application', {}).get('id')
        return None
    except Exception as e:
        print(f"Loan application submission failed: {e}")
        return None

def test_get_loan_applications(token):
    """Test getting loan applications"""
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(
            f"{API_BASE}/loan-applications",
            headers=headers
        )
        print_response(response, "Get Loan Applications")
        return response.status_code == 200
    except Exception as e:
        print(f"Get loan applications failed: {e}")
        return False

def test_get_specific_loan_application(token, application_id):
    """Test getting specific loan application"""
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(
            f"{API_BASE}/loan-applications/{application_id}",
            headers=headers
        )
        print_response(response, f"Get Loan Application {application_id}")
        return response.status_code == 200
    except Exception as e:
        print(f"Get specific loan application failed: {e}")
        return False

def test_unauthorized_access():
    """Test unauthorized access"""
    try:
        response = requests.get(f"{API_BASE}/loan-applications")
        print_response(response, "Unauthorized Access Test")
        return response.status_code == 401
    except Exception as e:
        print(f"Unauthorized access test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Starting Bank Loan Portal Backend API Tests")
    print(f"Testing against: {BASE_URL}")
    
    results = {}
    
    # Test 1: Health Check
    results['health_check'] = test_health_check()
    
    if not results['health_check']:
        print("\n❌ Backend is not running! Please start the Flask server first.")
        print("Run: python app.py")
        return
    
    # Test 2: User Registration
    results['registration'] = test_user_registration()
    
    # Test 3: User Login
    token = test_user_login()
    results['login'] = token is not None
    
    if not token:
        print("\n❌ Login failed! Cannot proceed with authenticated tests.")
        return
    
    # Test 4: Loan Application Submission
    application_id = test_loan_application_submission(token)
    results['loan_submission'] = application_id is not None
    
    # Test 5: Get Loan Applications
    results['get_applications'] = test_get_loan_applications(token)
    
    # Test 6: Get Specific Loan Application
    if application_id:
        results['get_specific_application'] = test_get_specific_loan_application(token, application_id)
    else:
        results['get_specific_application'] = False
    
    # Test 7: Unauthorized Access
    results['unauthorized_test'] = test_unauthorized_access()
    
    # Print Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = 0
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
        if passed_test:
            passed += 1
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the backend implementation.")
    
    print(f"\nBackend is running at: {BASE_URL}")
    print("API Documentation:")
    print("- POST /api/auth/register - Register new user")
    print("- POST /api/auth/login - User login")
    print("- POST /api/loan-applications - Submit loan application")
    print("- GET /api/loan-applications - Get user's applications")
    print("- GET /api/loan-applications/<id> - Get specific application")
    print("- GET /api/health - Health check")

if __name__ == "__main__":
    main()
