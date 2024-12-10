# EIN Validation Guidelines

## Overview
The Employer Identification Number (EIN) is a unique nine-digit number assigned by the IRS to business entities operating in the United States.

## Validation Rules
1. Must be exactly 9 digits
2. Can be formatted as XX-XXXXXXX
3. First two digits must be valid IRS prefixes
4. Must be verified against IRS database
5. Cannot contain all zeros or all ones

## Validation Process
1. Remove any hyphens or special characters
2. Check length and format
3. Verify against IRS database through API
4. Return validation status and any error messages

## Common Issues
- Invalid format
- Non-existent EIN
- Expired/inactive EIN
- Mismatched business name