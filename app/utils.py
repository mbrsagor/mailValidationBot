import asyncio
import aiosmtplib
import aiodns
from email_validator import validate_email
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Initialize shared resolver - MOVED inside functions to avoid "no event loop" error at import time
# resolver = aiodns.DNSResolver() 

def is_valid_email(email):
    # Wrapper for sync calls if needed, but we should prefer async for bulk
    # For backward compatibility with single check view if any
    try:
        return asyncio.run(async_validate_email(email))
    except Exception as e:
        logger.error(f"Global error for {email}: {e}")
        return None

async def async_validate_email(email, resolver=None):
    email = email.strip()
    
    # Create resolver if not provided (inefficient for bulk, efficient for single)
    if resolver is None:
        resolver = aiodns.DNSResolver()
        
    try:
        # 1. Check syntax
        valid = validate_email(email, check_deliverability=False)
        domain = valid.domain
        
        # 2. Get MX Record (Async)
        mx_record = None
        try:
            records = await resolver.query(domain, 'MX')
            mx_record = str(sorted(records, key=lambda r: r.priority)[0].host)
        except Exception as e:
            logger.debug(f"MX lookup failed for {email}: {e}")
            # Fallback to A record
            try:
                await resolver.query(domain, 'A')
                mx_record = domain
            except Exception as e:
                logger.debug(f"A lookup failed for {email}: {e}")
                return None

        # 3. SMTP Conversation (Async)
        mx_host = mx_record.rstrip('.')
        
        # Connect
        # Disable STARTTLS for speed and to avoid certificate errors on dev machines
        smtp = aiosmtplib.SMTP(hostname=mx_host, port=25, timeout=5, start_tls=False, use_tls=False)
        try:
            await smtp.connect()
        except Exception as e:
            # Fallback: If we have an MX record but can't connect (likely Port 25 block), 
            # assume the email is valid based on the domain.
            logger.warning(f"SMTP Connect failed for {email} ({mx_host}): {e}. Accepting based on valid domain.")
            return email
            
        try:
            # HELO - aiosmtplib converts this automatically during connect, but checking just in case
            # await smtp.helo('localhost') 
            
            # MAIL FROM
            sender = settings.VERIFIER_EMAIL
            await smtp.mail(sender)
            
            # RCPT TO
            code, message = await smtp.rcpt(email)
            
            await smtp.quit()
            
            if code == 250:
                return email
            return None
            
        except Exception as e:
            logger.error(f"SMTP Error for {email}: {e}")
            return None
            
    except Exception as e:
        logger.error(f"General Error for {email}: {e}")
        return None
