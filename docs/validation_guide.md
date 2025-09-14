# Data Validation Guide

## Overview
The RAG System includes a flexible validation framework that can be customized for any data validation needs.

## Built-in Validation Rules

### Email Validation
Validates standard email format:
- Required: @ symbol
- Valid domain extension
- Proper character usage

Example: `user@example.com`

### Phone Validation
Validates international phone numbers:
- Optional country code (+XX)
- 7-15 digits
- Handles common separators (spaces, dashes)

Example: `+1-234-567-8900`

### URL Validation
Validates web addresses:
- Protocol required (http/https)
- Valid domain format
- Optional path and parameters

Example: `https://example.com/path`

### Custom Pattern Validation
Define your own regex patterns:
- Flexible pattern matching
- Custom validation rules
- Extensible for any format

## API Usage

### Validation Endpoint
```
POST /validate
{
    "data": {
        "email": "user@example.com",
        "phone": "+1234567890",
        "custom_id": "ABC123"
    },
    "rules": {
        "email": "email",
        "phone": "phone",
        "custom_id": "pattern:^[A-Z]{3}\\d{3}$"
    }
}
```

### Response Format
```json
{
    "valid": true,
    "details": {
        "email": true,
        "phone": true,
        "custom_id": true
    },
    "timestamp": "2025-09-13T22:00:00"
}
```

## Extending Validation

You can easily add custom validation rules by:
1. Extending the ValidationService class
2. Adding new validation methods
3. Registering custom patterns

## Examples

### Product SKU Validation
Pattern: `^PROD-\d{4}-[A-Z]{2}$`
Example: `PROD-1234-AB`

### License Plate Validation
Pattern: `^[A-Z]{2}\d{2} [A-Z]{3}$`
Example: `AB12 CDE`

### Postal Code Validation
Pattern: `^\d{5}(-\d{4})?$`
Example: `12345` or `12345-6789`

## Best Practices

1. **Use specific patterns** for better validation accuracy
2. **Document your rules** for team understanding
3. **Test edge cases** to ensure reliability
4. **Handle errors gracefully** with clear messages
5. **Keep patterns simple** and maintainable
