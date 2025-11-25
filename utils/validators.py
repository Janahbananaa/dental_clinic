import re
from typing import Tuple

class Validators:
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True, "Valid email"
        return False, "Invalid email format"
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        pattern = r'^[0-9\-\+\(\)\s]{10,}$'
        if re.match(pattern, phone):
            return True, "Valid phone"
        return False, "Invalid phone format"
    
    @staticmethod
    def validate_date(date: str) -> Tuple[bool, str]:
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        if re.match(pattern, date):
            return True, "Valid date"
        return False, "Invalid date format (use YYYY-MM-DD)"
    
    @staticmethod
    def validate_time(time: str) -> Tuple[bool, str]:
        pattern = r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
        if re.match(pattern, time):
            return True, "Valid time"
        return False, "Invalid time format (use HH:MM)"
    
    @staticmethod
    def validate_not_empty(value: str) -> Tuple[bool, str]:
        if value.strip():
            return True, "Valid"
        return False, "Field cannot be empty"
