# backend/app/utils/helpers.py file
from datetime import datetime


# Safely formats a given value into a standard currency string.
def format_currency(amount, currency_symbol="₹"):
    """Safely format currency amounts, handling non-numeric values"""
    if amount is None or amount == '' or str(amount).lower() in ['n/a', 'na', 'none']:
        return 'N/A'
    
    try:
        # Convert to string and remove any currency symbols or spaces
        amount_str = str(amount).replace(currency_symbol, '').replace(',', '').strip()
        
        # Check if it's a valid number
        if amount_str.replace('.', '').isdigit():
            amount_num = float(amount_str)
            return f"{currency_symbol}{int(amount_num):,}"
        else:
            return 'N/A'
    except (ValueError, TypeError):
        return 'N/A'


# It takes the list of all loan applications and calculates the summary statistics for the admin dashboard.
def calculate_analytics(applications):
    """Calculate analytics data for the dashboard"""
    total_applications = len(applications)
    approved_count = 0
    pending_count = 0
    rejected_count = 0
    loan_types = {}
    total_amount = 0
    valid_amounts = 0
    
    for app in applications:
        # Count status
        status = app.get('status', 'pending').lower()
        if status in ['approved', 'eligibility_assessed']:
            approved_count += 1
        elif status == 'rejected':
            rejected_count += 1
        else:
            pending_count += 1
        
        # Count loan types
        loan_type = app.get('loan_type', app.get('loanType', 'Other'))
        if not loan_type or loan_type.strip() == '':
            loan_type = 'Other'
        loan_types[loan_type] = loan_types.get(loan_type, 0) + 1
        
        # Calculate average amount
        amount = app.get('loan_amount', app.get('loanAmount', ''))
        if amount and str(amount).strip() and str(amount).strip() != 'N/A':
            try:
                amount_val = float(str(amount).replace(',', '').replace('$', '').replace('₹', ''))
                total_amount += amount_val
                valid_amounts += 1
            except (ValueError, TypeError):
                pass
    
    # Calculate average amount
    avg_amount = format_currency(total_amount / valid_amounts if valid_amounts > 0 else 0)
    
    return {
        'total_applications': total_applications,
        'approved_count': approved_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
        'loan_types': loan_types,
        'avg_amount': avg_amount
    }


# It's used to calculate an applicant's age to send to the AI for the eligibility check.
def calculate_age_from_dob(dob_str):
    """Calculate age from date of birth string"""
    try:
        if not dob_str:
            return "Unknown"
        
        from datetime import datetime
        dob = datetime.strptime(dob_str, '%Y-%m-%d')
        today = datetime.now()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    except:
        return "Unknown"
    

def rule_based_eligibility_assessment(loan_data):
    """Rule-based eligibility assessment when Watson AI is not available"""
    try:
        annual_income = float(loan_data.get('annual-income', 0))
        loan_amount = float(loan_data.get('loan-amount', 0))
        cibil_score = int(loan_data.get('cibil-score', 0)) if loan_data.get('cibil-score', '').isdigit() else 0
        age = calculate_age_from_dob(loan_data.get('date-of-birth', ''))
        
        # Basic eligibility rules
        reasons = []
        status = 'APPROVED'
        
        # Age check
        if isinstance(age, int):
            if age < 21:
                reasons.append('Applicant below minimum age of 21 years')
                status = 'REJECTED'
            elif age > 65:
                reasons.append('Applicant above maximum age of 65 years')
                status = 'REJECTED'
        
        # Income check
        if annual_income < 300000:  # Minimum 3 LPA
            reasons.append('Annual income below minimum requirement of ₹3,00,000')
            status = 'REJECTED'
        
        # Loan amount to income ratio
        if annual_income > 0 and (loan_amount / annual_income) > 5:
            reasons.append('Loan amount exceeds 5 times annual income')
            status = 'CONDITIONALLY_APPROVED'
        
        # CIBIL score check
        if cibil_score < 650:
            reasons.append('CIBIL score below 650')
            if cibil_score < 550:
                status = 'REJECTED'
            else:
                status = 'CONDITIONALLY_APPROVED'
        
        # Determine documents based on loan type and employment
        documents = []
        loan_type = loan_data.get('loan-type', '').lower()
        employment_type = loan_data.get('employment-type', '').lower()
        
        # Common documents
        documents.extend(['Aadhaar Card', 'PAN Card', 'Passport Size Photos', 'Bank Statements (6 months)'])
        
        # Employment specific documents
        if 'salaried' in employment_type:
            documents.extend(['Salary Slips (3 months)', 'Employment Certificate', 'Form 16'])
        else:
            documents.extend(['Business Registration', 'ITR (2 years)', 'Profit & Loss Statement', 'Balance Sheet'])
        
        # Loan type specific documents
        if 'home' in loan_type:
            documents.extend(['Property Documents', 'Sale Agreement', 'Approved Building Plan'])
        elif 'car' in loan_type:
            documents.extend(['Vehicle Quotation', 'Insurance Details'])
        elif 'education' in loan_type:
            documents.extend(['Admission Letter', 'Fee Structure', 'Academic Records'])
        
        # Prepare recommendations
        recommendations = []
        if status == 'REJECTED':
            recommendations.append('Improve CIBIL score and reapply after 6 months')
            recommendations.append('Consider applying for a smaller loan amount')
        elif status == 'CONDITIONALLY_APPROVED':
            recommendations.append('Additional verification required')
            recommendations.append('Co-applicant may be required')
        else:
            recommendations.append('Please submit all required documents for final approval')
        
        return {
            'status': status,
            'reason': '; '.join(reasons) if reasons else 'All eligibility criteria met',
            'documents': ', '.join(documents),
            'recommendations': '; '.join(recommendations)
        }
        
    except Exception as e:
        print(f"Rule-based assessment error: {e}")
        return {
            'status': 'PENDING_REVIEW',
            'reason': 'Manual review required due to assessment error',
            'documents': 'Identity Proof, Income Proof, Address Proof',
            'recommendations': 'Please contact bank for manual assessment'
        }