import dns.resolver
from email_validator import validate_email

def is_valid_email(email):
    email = email.strip()
    try:
        # Check syntax
        valid = validate_email(email, check_deliverability=False)
        domain = valid.domain
        # Check MX Record (DNS)
        dns.resolver.resolve(domain, 'MX', lifetime=1)
        return email
    except:
        return None
