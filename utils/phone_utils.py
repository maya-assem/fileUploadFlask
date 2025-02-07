import re

def standardize_phone_number(phone):
    """Standardize phone numbers to a consistent format"""
    if not isinstance(phone, str):
        return phone
    
    # Remove any text in angle brackets (like "<142>")
    phone = re.sub(r'<[^>]+>', '', phone)
    
    # Remove all non-digit characters
    phone = re.sub(r'\D', '', phone)
    
    # Handle Egyptian numbers
    if phone.startswith('2') and len(phone) == 12:
        return phone
    elif len(phone) == 11 and phone.startswith('01'):
        return '2' + phone
    
    return phone
