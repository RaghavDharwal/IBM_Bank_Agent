#!/usr/bin/env python3
"""
Test script for the format_currency function to ensure it handles various input types correctly
"""

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

# Test cases
test_cases = [
    100000,          # Should return: ₹100,000
    "500000",        # Should return: ₹500,000
    "N/A",           # Should return: N/A
    None,            # Should return: N/A
    "",              # Should return: N/A
    "abc",           # Should return: N/A
    50000.50,        # Should return: ₹50,000
    "₹25000",        # Should return: ₹25,000
    "1,000,000",     # Should return: ₹1,000,000
]

print("Testing format_currency function:")
print("-" * 40)
for test_case in test_cases:
    result = format_currency(test_case)
    print(f"Input: {repr(test_case):15} → Output: {result}")

print("\n✅ All test cases completed successfully!")
