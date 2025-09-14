"""Generic validation service for custom data validation rules"""
from typing import Dict, Any, Optional
import re

class ValidationService:
    """
    Extensible validation service for custom validation rules.
    Users can add their own validation methods as needed.
    """
    
    async def validate_email(self, email: str) -> bool:
        """Validate email format"""
        if not email:
            return True
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    async def validate_phone(self, phone: str) -> bool:
        """Validate phone number (basic international format)"""
        if not phone:
            return True
        # Remove spaces, dashes, parentheses
        clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
        # Check if it's digits with optional + at start
        pattern = r'^\+?\d{7,15}$'
        return bool(re.match(pattern, clean_phone))
    
    async def validate_url(self, url: str) -> bool:
        """Validate URL format"""
        if not url:
            return True
        pattern = r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)$'
        return bool(re.match(pattern, url))
    
    async def validate_custom_id(self, id_value: str, pattern: str = r'^\d{9}$') -> bool:
        """
        Generic ID validation with customizable pattern
        Default pattern: 9 digits
        Users can override with their own patterns
        """
        if not id_value:
            return True
        clean_id = re.sub(r'[\-\s]', '', id_value)
        return bool(re.match(pattern, clean_id))
    
    async def validate_data(self, data: Dict[str, Any], rules: Dict[str, str]) -> Dict[str, bool]:
        """
        Validate multiple fields with custom rules
        
        Args:
            data: Dictionary of field names and values
            rules: Dictionary of field names and validation types
        
        Returns:
            Dictionary of field names and validation results
        """
        results = {}
        
        for field, value in data.items():
            if field not in rules:
                continue
                
            rule = rules[field]
            
            if rule == "email":
                results[field] = await self.validate_email(value)
            elif rule == "phone":
                results[field] = await self.validate_phone(value)
            elif rule == "url":
                results[field] = await self.validate_url(value)
            elif rule.startswith("pattern:"):
                # Custom pattern validation
                pattern = rule.replace("pattern:", "")
                results[field] = await self.validate_custom_id(value, pattern)
            else:
                # Unknown rule, default to True
                results[field] = True
        
        return results
