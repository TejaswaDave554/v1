import re

def validate_password_strength(password: str) -> dict:
    criteria = {
        'length': len(password) >= 8,
        'uppercase': bool(re.search(r'[A-Z]', password)),
        'lowercase': bool(re.search(r'[a-z]', password)),
        'digit': bool(re.search(r'\d', password)),
        'special': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    }

    passed = sum(criteria.values())

    if passed < 3:
        strength = 'weak'
        valid = False
    elif passed < 5:
        strength = 'medium'
        valid = True
    else:
        strength = 'strong'
        valid = True

    return {
        'valid': valid,
        'strength': strength,
        'criteria': criteria,
        'passed_count': passed
    }

def get_password_requirements_text(criteria: dict) -> str:
    checks = [
        ('length', 'At least 8 characters' if criteria['length'] else 'At least 8 characters (required)'),
        ('uppercase', 'One uppercase letter' if criteria['uppercase'] else 'One uppercase letter (required)'),
        ('lowercase', 'One lowercase letter' if criteria['lowercase'] else 'One lowercase letter (required)'),
        ('digit', 'One number' if criteria['digit'] else 'One number (required)'),
        ('special', 'One special character (!@#$%^&*)' if criteria['special'] else 'One special character (!@#$%^&*) (required)')
    ]
    return '\n'.join([f"{'✓' if criteria[key] else '✗'} {text}" for key, text in checks])
