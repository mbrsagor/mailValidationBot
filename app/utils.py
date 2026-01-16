import smtplib
import socket
import dns.resolver
from email_validator import validate_email

def is_valid_email(email):
    email = email.strip()
    try:
        # 1. Check syntax
        valid = validate_email(email, check_deliverability=False)
        domain = valid.domain
        
        # 2. Get MX Record
        try:
            records = dns.resolver.resolve(domain, 'MX')
            mx_record = str(sorted(records, key=lambda r: r.preference)[0].exchange)
        except Exception:
            # Fallback to A record if MX missing (rare but possible per RFC)
            # But for "active webmail" often strict MX is safer. Let's try A record just in case.
            try:
                dns.resolver.resolve(domain, 'A')
                mx_record = domain
            except:
                return None

        # 3. SMTP Conversation (Existence Check)
        # Connect to the mail server
        server = smtplib.SMTP(timeout=5)
        server.set_debuglevel(0)
        
        # MX record might end with a dot
        mx_host = mx_record.rstrip('.')
        
        try:
            code, message = server.connect(mx_host)
            if code != 220:
                server.quit()
                return None
        except (socket.timeout, socket.error):
            return None

        # HELO
        server.helo('localhost') # Ideally use a valid FQDN here
        
        # MAIL FROM
        from django.conf import settings
        sender = settings.VERIFIER_EMAIL
        code, message = server.mail(sender)
        if code != 250:
            server.quit()
            return None
        
        # RCPT TO - This is the real check
        code, message = server.rcpt(email)
        server.quit()
        
        if code == 250:
            return email
        else:
            return None
            
    except Exception as e:
        # If any unexpected error occurs, assume invalid or unverifiable
        return None
